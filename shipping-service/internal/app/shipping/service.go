package shipping

import (
	"context"
	"errors"
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping/common"
	"github.com/google/uuid"
	"strings"
	"time"

	"github.com/go-playground/validator/v10"
)

type ShippingOrderRequest struct {
	Address string `json:"address,omitempty" validate:"required"`

	Country string `json:"country,omitempty" validate:"required"`

	TotalAmount float32 `json:"totalAmount,omitempty" validate:"required"`

	OrderId string `json:"orderId,omitempty" validate:"required"`
}

type ShippingOrder struct {
	TrackingId string `json:"trackingId,omitempty"`

	DateCreated time.Time `json:"dateCreated,omitempty"`

	Status Status `json:"status,omitempty"`

	Address string `json:"address,omitempty"`

	Country string `json:"country,omitempty"`

	TotalAmount float32 `json:"totalAmount,omitempty"`

	OrderId string `json:"orderId,omitempty"`
}

type Status string

const (
	Pending   Status = "Pending"
	Completed Status = "Completed"
	Failed    Status = "Failed"
)

var (
	ErrInvalidInput = errors.New("Invalid inputs provided")
)

var (
	validate = validator.New()
)

type ShippingRepository interface {
	Store(ctx context.Context, shippingOrder *ShippingOrder) error
	Find(ctx context.Context, trackingId string) (*ShippingOrder, error)
	FindAll(ctx context.Context) (*[]ShippingOrder, error)
}

type Service interface {
	ServiceStatus(ctx context.Context) error
	CreateShipping(ctx context.Context, shippingOrderRequest ShippingOrderRequest) (string, error)
	GetShipping(ctx context.Context, trackingId string) (ShippingOrder, error)
	GetAllShipping(ctx context.Context) ([]ShippingOrder, error)
}

type service struct {
	shippingRepository ShippingRepository
}

func NewService(shippingRepository ShippingRepository) *service {
	return &service{
		shippingRepository: shippingRepository,
	}
}

func (s *service) ServiceStatus(ctx context.Context) error {
	return nil
}

func (s *service) CreateShipping(ctx context.Context, shippingOrderRequest ShippingOrderRequest) (string, error) {
	dateCreated := time.Now()
	trackingId := strings.Split(strings.ToUpper(uuid.New().String()), "-")[0]
	err := common.ValidateStruct(*validate, shippingOrderRequest)
	if err != nil {
		return "", err
	}

	// create shipping order
	so := &ShippingOrder{
		TrackingId:  trackingId,
		DateCreated: dateCreated,
		Status:      Pending,
		Address:     shippingOrderRequest.Address,
		Country:     shippingOrderRequest.Country,
		TotalAmount: shippingOrderRequest.TotalAmount,
		OrderId:     shippingOrderRequest.OrderId,
	}

	err = s.shippingRepository.Store(ctx, so)

	if err != nil {
		return "", err
	}

	return trackingId, nil
}

func (s *service) GetShipping(ctx context.Context, trackingId string) (ShippingOrder, error) {
	err := common.ValidateVar(*validate, trackingId, "required")
	if err != nil {
		return ShippingOrder{}, ErrInvalidInput
	}

	so, err := s.shippingRepository.Find(ctx, trackingId)

	if err != nil {
		return ShippingOrder{}, err
	}

	return *so, nil
}

func (s *service) GetAllShipping(ctx context.Context) ([]ShippingOrder, error) {

	sos, err := s.shippingRepository.FindAll(ctx)

	if err != nil {
		return nil, err
	}

	var result []ShippingOrder

	result = append(result, *sos...)

	return result, nil
}
