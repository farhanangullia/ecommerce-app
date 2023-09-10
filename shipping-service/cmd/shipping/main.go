package main

import (
	"fmt"
	"net"
	"net/http"
	"os"
	"os/signal"
	"shipping-service/internal/app/shipping"
	"shipping-service/internal/app/shipping/endpoints"
	"shipping-service/internal/app/shipping/transport"
	"syscall"

	"github.com/go-kit/log"
	"github.com/go-kit/log/level"
)

const (
	defaultHTTPPort = "920"
	//defaultGRPCPort = "8082"
)

func main() {
	var (
		logger   log.Logger
		httpAddr = net.JoinHostPort("0.0.0.0", envString("HTTP_PORT", defaultHTTPPort))
		//grpcAddr = net.JoinHostPort("0.0.0.0", envString("GRPC_PORT", defaultGRPCPort))
	)

	//TODO: Add config mgmt https://github.com/spf13/viper
	logger = log.NewLogfmtLogger(log.NewSyncWriter(os.Stderr))
	logger = log.With(logger,
		"svc", "shipping-service",
		"ts", log.DefaultTimestampUTC,
		"caller", log.DefaultCaller,
	)

	level.Info(logger).Log("msg", "service started")
	defer level.Info(logger).Log("msg", "service ended")

	// Create shipping Service
	var s shipping.Service
	{
		level.Info(logger).Log("msg", "initializing Postgres")
		// shippingRepository := adapters.NewShippingPgsqlDbRepository(db)
		// s = shipping.NewService(shippingRepository)
	}

	// Create Go kit endpoints for the Service
	var e endpoints.Endpoints
	{
		e = endpoints.MakeServerEndpoints(s)
	}

	var h http.Handler
	{
		h = transport.NewHTTPHandler(e, logger)
	}

	errs := make(chan error)
	go func() {
		c := make(chan os.Signal, 1)
		signal.Notify(c, syscall.SIGINT, syscall.SIGTERM)
		errs <- fmt.Errorf("%s", <-c)
	}()

	go func() {
		level.Info(logger).Log("transport", "HTTP", "addr", httpAddr)
		errs <- http.ListenAndServe(httpAddr, h)
	}()

	level.Error(logger).Log("exit", <-errs)
}

func envString(env, fallback string) string {
	e := os.Getenv(env)
	if e == "" {
		return fallback
	}
	return e
}
