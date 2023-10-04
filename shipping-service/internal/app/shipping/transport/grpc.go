package transport

import (
	"context"
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping/endpoints"
	"github.com/farhanangullia/ecommerce-app/shipping-service/pb"
	kittransport "github.com/go-kit/kit/transport"
	kitgrpc "github.com/go-kit/kit/transport/grpc"
	kitlog "github.com/go-kit/log"
)

type grpcServer struct {
	serviceStatus  kitgrpc.Handler
	shippingOrder  kitgrpc.Handler
	findShipping   kitgrpc.Handler
	getAllShipping kitgrpc.Handler
	pb.UnimplementedShippingServiceServer
}

// NewGRPCServer initializes a new gRPC server
func NewGRPCServer(ep endpoints.Endpoints, logger kitlog.Logger) pb.ShippingServiceServer {
	options := []kitgrpc.ServerOption{
		kitgrpc.ServerErrorHandler(kittransport.NewLogErrorHandler(logger)),
	}

	return &grpcServer{
		serviceStatus: kitgrpc.NewServer(
			ep.ServiceStatus,
			decodeServiceStatusRequest,
			encodeServiceStatusResponse,
			options...,
		),
		shippingOrder: kitgrpc.NewServer(
			ep.CreateShipping,
			decodeCreateShippingRequest,
			encodeCreateShippingResponse,
			options...,
		),
		findShipping: kitgrpc.NewServer(
			ep.FindShipping,
			decodeFindShippingRequest,
			encodeFindShippingResponse,
			options...,
		),
		getAllShipping: kitgrpc.NewServer(
			ep.GetAllShipping,
			decodeGetAllShippingRequest,
			encodeGetAllShippingResponse,
			options...,
		),
	}
}

func (s *grpcServer) ServiceStatus(ctx context.Context, r *pb.ServiceStatusRequest) (*pb.ServiceStatusReply, error) {
	_, rep, err := s.serviceStatus.ServeGRPC(ctx, r)
	if err != nil {
		return nil, err
	}
	return rep.(*pb.ServiceStatusReply), nil
}

func (s grpcServer) ShippingOrder(ctx context.Context, req *pb.ShippingOrderRequest) (*pb.ShippingOrderReply, error) {
	_, resp, err := s.shippingOrder.ServeGRPC(ctx, req)
	if err != nil {
		return nil, err
	}

	return resp.(*pb.ShippingOrderReply), nil
}

func (s grpcServer) FindShipping(ctx context.Context, req *pb.FindShippingRequest) (*pb.FindShippingReply, error) {
	_, resp, err := s.findShipping.ServeGRPC(ctx, req)
	if err != nil {
		return nil, err
	}

	return resp.(*pb.FindShippingReply), nil
}

func (s grpcServer) GetAllShipping(ctx context.Context, req *pb.GetAllShippingRequest) (*pb.GetAllShippingReply, error) {
	_, resp, err := s.getAllShipping.ServeGRPC(ctx, req)
	if err != nil {
		return nil, err
	}

	return resp.(*pb.GetAllShippingReply), nil
}

func decodeServiceStatusRequest(_ context.Context, request interface{}) (interface{}, error) {
	return endpoints.ServiceStatusRequest{}, nil
}

func encodeServiceStatusResponse(ctx context.Context, reply interface{}) (interface{}, error) {
	r := reply.(endpoints.ServiceStatusResponse)
	if r.Err != "" {
		return &pb.ServiceStatusReply{Err: &r.Err}, nil
	}
	return &pb.ServiceStatusReply{}, nil
}

func decodeCreateShippingRequest(_ context.Context, request interface{}) (interface{}, error) {
	r := request.(*pb.ShippingOrderRequest)
	return endpoints.CreateShippingRequest{
		Address:     r.Address,
		Country:     r.Country,
		TotalAmount: r.TotalAmount,
		OrderId:     r.OrderId,
	}, nil
}

func encodeCreateShippingResponse(ctx context.Context, reply interface{}) (interface{}, error) {
	r := reply.(endpoints.CreateShippingResponse)
	if r.Err != "" {
		return &pb.ShippingOrderReply{Err: &r.Err}, nil
	}
	return &pb.ShippingOrderReply{TrackingId: &r.TrackingId}, nil
}

func decodeFindShippingRequest(_ context.Context, request interface{}) (interface{}, error) {
	r := request.(*pb.FindShippingRequest)
	return endpoints.FindShippingRequest{
		TrackingId: r.TrackingId,
	}, nil
}

func encodeFindShippingResponse(ctx context.Context, reply interface{}) (interface{}, error) {
	r := reply.(endpoints.FindShippingResponse)
	if r.Err != "" {
		return &pb.FindShippingReply{Err: &r.Err}, nil
	}
	return &pb.FindShippingReply{ShippingOrder: &pb.ShippingOrder{
		Address:     r.ShippingOrder.Address,
		Country:     r.ShippingOrder.Country,
		TotalAmount: r.ShippingOrder.TotalAmount,
		OrderId:     r.ShippingOrder.OrderId,
		DateCreated: r.ShippingOrder.DateCreated.String(),
		Status:      string(r.ShippingOrder.Status),
	}}, nil
}

func decodeGetAllShippingRequest(_ context.Context, request interface{}) (interface{}, error) {
	_ = request.(*pb.GetAllShippingRequest)
	return endpoints.GetAllShippingRequest{}, nil
}

func encodeGetAllShippingResponse(ctx context.Context, reply interface{}) (interface{}, error) {
	r := reply.(endpoints.GetAllShippingResponse)
	if r.Err != "" {
		return &pb.GetAllShippingReply{Err: &r.Err}, nil
	}

	var result []*pb.ShippingOrder
	for _, so := range r.ShippingOrders {
		result = append(result, &pb.ShippingOrder{
			Address:     so.Address,
			Country:     so.Country,
			TotalAmount: so.TotalAmount,
			OrderId:     so.OrderId,
			DateCreated: so.DateCreated.String(),
			Status:      string(so.Status),
		})
	}

	return &pb.GetAllShippingReply{
		ShippingOrders: result}, nil
}
