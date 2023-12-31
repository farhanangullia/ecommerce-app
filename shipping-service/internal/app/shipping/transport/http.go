package transport

import (
	"context"
	"encoding/json"
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping/endpoints"
	"net/http"

	kittransport "github.com/go-kit/kit/transport"
	kithttp "github.com/go-kit/kit/transport/http"
	kitlog "github.com/go-kit/log"
	"github.com/gorilla/mux"
)

func NewHTTPHandler(ep endpoints.Endpoints, logger kitlog.Logger) http.Handler {
	r := mux.NewRouter()

	options := []kithttp.ServerOption{
		kithttp.ServerErrorHandler(kittransport.NewLogErrorHandler(logger)),
		kithttp.ServerErrorEncoder(encodeError),
	}

	// Configure routes with Gorilla Mux package
	r.Methods("GET").Name("HealthCheck").Path("/healthz").Handler(kithttp.NewServer(
		ep.ServiceStatus,
		decodeServiceStatus,
		encodeResponse,
		options...,
	))

	return r
}

func decodeServiceStatus(_ context.Context, r *http.Request) (request interface{}, err error) {
	var req endpoints.ServiceStatusRequest
	if r.ContentLength == 0 {
		return req, nil
	}

	err = json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		return nil, err
	}
	return req, nil
}

// Errorer is implemented by all concrete response types that may contain
// errors. It allows us to change the HTTP response code without needing to
// trigger an endpoint (transport-level) error.
type Errorer interface {
	Error() error
}

func encodeResponse(ctx context.Context, w http.ResponseWriter, response interface{}) error {
	if e, ok := response.(Errorer); ok && e.Error() != nil { // Not a Go kit transport error, but a business-logic error.
		// Provide those as HTTP errors.
		encodeError(ctx, e.Error(), w)
		return nil
	}
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	return json.NewEncoder(w).Encode(response)
}

func encodeError(_ context.Context, err error, w http.ResponseWriter) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	switch err {
	default:
		w.WriteHeader(http.StatusInternalServerError)
	}
	json.NewEncoder(w).Encode(map[string]interface{}{
		"error": err.Error(),
	})
}
