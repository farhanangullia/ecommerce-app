package main

import (
	"fmt"
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping/adapters"
	"github.com/farhanangullia/ecommerce-app/shipping-service/pb"
	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	"google.golang.org/grpc/reflection"
	"net"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping"
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping/endpoints"
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping/transport"
	"github.com/go-kit/log"
	"github.com/go-kit/log/level"
	"github.com/spf13/viper"
	_ "go.uber.org/automaxprocs"
	healthgrpc "google.golang.org/grpc/health/grpc_health_v1"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"
)

const (
	defaultHTTPPort = "9200"
	defaultGRPCPort = "8082"
)

func init() {
	viper.SetConfigName("config")
	viper.SetConfigType("json")
	viper.AddConfigPath(".")
	viper.AddConfigPath("configs/")
	viper.AddConfigPath("shipping-service/configs/")
	viper.AddConfigPath("../../configs/")
	viper.AutomaticEnv()
	_ = viper.ReadInConfig()
}

func main() {
	var (
		logger                  log.Logger
		grpcHealthCheckInterval = time.Second * 5
		httpAddr                = net.JoinHostPort("0.0.0.0", getValue(viper.Get("HTTP_PORT"), defaultHTTPPort))
		grpcAddr                = net.JoinHostPort("0.0.0.0", getValue(viper.Get("GRPC_PORT"), defaultGRPCPort))
		dbHost                  = viper.GetString("DB_HOST")
		dbPort                  = viper.GetString("DB_PORT")
		dbUser                  = viper.GetString("DB_USER")
		dbName                  = viper.GetString("DB_NAME")
		dbPassword              = viper.GetString("DB_PASSWORD")
	)

	logger = log.NewLogfmtLogger(log.NewSyncWriter(os.Stderr))
	logger = log.With(logger,
		"svc", viper.Get("SERVICE_NAME"),
		"ts", log.DefaultTimestampUTC,
		"caller", log.DefaultCaller,
	)

	level.Info(logger).Log("msg", "service started")
	defer level.Info(logger).Log("msg", "service ended")

	// Create shipping Service
	var s shipping.Service
	{
		level.Info(logger).Log("msg", "initializing Postgres")
		shippingRepository, err := adapters.NewShippingPgsqlRepository(dbHost, dbUser, dbPassword, dbName, dbPort)

		if err != nil {
			level.Error(logger).Log("adapters", "postgres", "err", err)
			os.Exit(1)
		}

		s = shipping.NewService(shippingRepository)

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

	var g pb.ShippingServiceServer
	{
		g = transport.NewGRPCServer(e, logger)
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

	grpcListener, err := net.Listen("tcp", grpcAddr)
	if err != nil {
		level.Error(logger).Log("transport", "gRPC", "err", err)
		os.Exit(1)
	}

	grpcHealthCheck := health.NewServer()
	go func() {
		level.Info(logger).Log("transport", "GRPC", "addr", grpcAddr)
		baseServer := grpc.NewServer()
		healthgrpc.RegisterHealthServer(baseServer, grpcHealthCheck)
		pb.RegisterShippingServiceServer(baseServer, g)
		reflection.Register(baseServer)
		errs <- baseServer.Serve(grpcListener)
	}()

	go func() {
		grpcHealthCheck.SetServingStatus("", healthpb.HealthCheckResponse_SERVING)
		time.Sleep(grpcHealthCheckInterval)
	}()

	level.Error(logger).Log("msg", "graceful shutdown", "exit", <-errs)
}

func getValue(value interface{}, fallback string) string {
	if value == nil {
		return fallback
	}
	return fmt.Sprintf("%v", value)
}
