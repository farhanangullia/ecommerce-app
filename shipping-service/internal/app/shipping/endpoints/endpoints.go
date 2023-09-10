package endpoints

import (
	"context"
	"shipping-service/internal/app/shipping"

	"github.com/go-kit/kit/endpoint"
)

// Endpoints holds all Go kit endpoints
type Endpoints struct {
	ServiceStatusRequest endpoint.Endpoint
}

// MakeServerEndpoints initializes all Go kit endpoints
func MakeServerEndpoints(s shipping.Service) Endpoints {
	return Endpoints{
		ServiceStatusRequest: makeServiceStatusRequestEndpoint(s),
	}
}

func makeServiceStatusRequestEndpoint(s shipping.Service) endpoint.Endpoint {
	return func(ctx context.Context, request interface{}) (interface{}, error) {
		_ = request.(ServiceStatusRequest)
		err := s.ServiceStatus(ctx)
		if err != nil {
			return ServiceStatusResponse{Err: err}, nil
		}
		return ServiceStatusResponse{}, nil
	}
}

// errors
func (r ServiceStatusResponse) Error() error { return r.Err }
