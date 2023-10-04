package endpoints

import (
	"context"
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping"
	"github.com/go-kit/kit/endpoint"
)

// Endpoints holds all Go kit endpoints
type Endpoints struct {
	ServiceStatus  endpoint.Endpoint
	CreateShipping endpoint.Endpoint
	FindShipping   endpoint.Endpoint
	GetAllShipping endpoint.Endpoint
}

// MakeServerEndpoints initializes all Go kit endpoints
func MakeServerEndpoints(s shipping.Service) Endpoints {
	return Endpoints{
		ServiceStatus:  makeServiceStatusEndpoint(s),
		CreateShipping: makeCreateShippingEndpoint(s),
		FindShipping:   makeFindShippingEndpoint(s),
		GetAllShipping: makeGetAllShippingEndpoint(s),
	}
}

func makeServiceStatusEndpoint(s shipping.Service) endpoint.Endpoint {
	return func(ctx context.Context, request interface{}) (interface{}, error) {
		_ = request.(ServiceStatusRequest)
		err := s.ServiceStatus(ctx)
		if err != nil {
			return ServiceStatusResponse{Err: err.Error()}, nil
		}
		return ServiceStatusResponse{}, nil
	}
}

func makeCreateShippingEndpoint(s shipping.Service) endpoint.Endpoint {
	return func(ctx context.Context, request interface{}) (interface{}, error) {
		req := request.(CreateShippingRequest)
		trackingId, err := s.CreateShipping(ctx, shipping.ShippingOrderRequest{
			Address:     req.Address,
			Country:     req.Country,
			TotalAmount: req.TotalAmount,
			OrderId:     req.OrderId,
		})
		if err != nil {
			return CreateShippingResponse{Err: err.Error()}, nil
		}
		return CreateShippingResponse{
			TrackingId: trackingId,
		}, nil
	}
}

func makeFindShippingEndpoint(s shipping.Service) endpoint.Endpoint {
	return func(ctx context.Context, request interface{}) (interface{}, error) {
		req := request.(FindShippingRequest)
		shippingOrder, err := s.GetShipping(ctx, req.TrackingId)
		if err != nil {
			return FindShippingResponse{Err: err.Error()}, nil
		}
		return FindShippingResponse{
			ShippingOrder: shippingOrder,
		}, nil
	}
}

func makeGetAllShippingEndpoint(s shipping.Service) endpoint.Endpoint {
	return func(ctx context.Context, request interface{}) (interface{}, error) {
		_ = request.(GetAllShippingRequest)
		shippingOrders, err := s.GetAllShipping(ctx)
		if err != nil {
			return GetAllShippingResponse{Err: err.Error()}, nil
		}
		return GetAllShippingResponse{
			ShippingOrders: shippingOrders,
		}, nil
	}
}

// errors
//func (r ServiceStatusResponse) Error() error  { return r.Error() }
//func (r CreateShippingResponse) Error() error { return r.Error() }
//func (r FindShippingResponse) Error() error   { return r.Error() }
//func (r GetAllShippingResponse) Error() error { return r.Error() }
