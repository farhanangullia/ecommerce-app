package endpoints

import (
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping"
)

type ServiceStatusRequest struct{}

type ServiceStatusResponse struct {
	Err string `json:"err,omitempty"`
}

type CreateShippingRequest struct {
	Address     string  `json:"address,omitempty"`
	Country     string  `json:"country,omitempty"`
	TotalAmount float32 `json:"totalAmount,omitempty"`
	OrderId     string  `json:"orderId,omitempty"`
}

type CreateShippingResponse struct {
	TrackingId string `json:"trackingId,omitempty"`
	Err        string `json:"err,omitempty"`
}

type FindShippingRequest struct {
	TrackingId string `json:"trackingId,omitempty"`
}

type FindShippingResponse struct {
	ShippingOrder shipping.ShippingOrder `json:"shippingOrder,omitempty"`
	Err           string                 `json:"err,omitempty"`
}

type GetAllShippingRequest struct{}

type GetAllShippingResponse struct {
	ShippingOrders []shipping.ShippingOrder `json:"shippingOrders,omitempty"`
	Err            string                   `json:"err,omitempty"`
}
