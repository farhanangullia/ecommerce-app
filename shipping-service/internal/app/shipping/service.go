package shipping

import (
	"context"
	"errors"
	"shipping-service/internal/app/shipping/common"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/google/uuid"
)

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

type ShippingRepository interface {)
}

type Service interface {
	ServiceStatus(ctx context.Context) error
}

type service struct {
	shippingRepository  ShippingRepository
}

func NewService(shippingRepository ShippingRepository) *service {
	return &service{
		shippingRepository:  shippingRepository,
	}
}

func (s *service) ServiceStatus(ctx context.Context) error {
	return nil
}
