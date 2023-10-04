package adapters

import (
	"context"
	"errors"
	"fmt"
	"github.com/farhanangullia/ecommerce-app/shipping-service/internal/app/shipping"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"time"
)

type ShippingOrder struct {
	TrackingId  string    `gorm:"primary_key" json:"trackingId"`
	DateCreated time.Time `gorm:"not null" json:"dateCreated"`
	Status      string    `gorm:"not null" json:"status"`
	Address     string    `gorm:"not null" json:"address"`
	Country     string    `gorm:"not null" json:"country"`
	TotalAmount float32   `gorm:"not null" json:"totalAmount"`
	OrderId     string    `gorm:"not null" json:"orderId"`
}

func (ShippingOrder) TableName() string {
	return "shippingorders"
}

type ShippingPgsqlRepository struct {
	client *gorm.DB
}

var (
	ErrorItemNotFound = errors.New("no matching item found in database")
)

// returns a concrete repository backed by Gorm Postgres
func NewShippingPgsqlRepository(host string, dbUser string, password string, dbName string, port string) (shipping.ShippingRepository, error) {
	dsn := fmt.Sprintf("host=%s port=%s user=%s dbname=%s password=%s sslmode=disable",
		host,
		port,
		dbUser,
		dbName,
		password,
	)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})

	if err != nil {
		return nil, err
	}

	err = db.AutoMigrate(&ShippingOrder{})
	if err != nil {
		return nil, err
	}

	return &ShippingPgsqlRepository{
		client: db,
	}, nil
}

func (s ShippingPgsqlRepository) Store(ctx context.Context, shippingOrder *shipping.ShippingOrder) error {
	so := ShippingOrder{
		TrackingId:  shippingOrder.TrackingId,
		DateCreated: shippingOrder.DateCreated,
		Status:      string(shippingOrder.Status),
		Address:     shippingOrder.Address,
		Country:     shippingOrder.Country,
		TotalAmount: shippingOrder.TotalAmount,
		OrderId:     shippingOrder.OrderId,
	}

	if err := s.client.WithContext(ctx).Create(&so).Error; err != nil {
		return err
	}

	return nil
}

func (s ShippingPgsqlRepository) Find(ctx context.Context, trackingId string) (*shipping.ShippingOrder, error) {
	var so ShippingOrder
	if err := s.client.WithContext(ctx).First(&so, "tracking_id = ?", trackingId).Error; err != nil {
		return nil, err
	}
	result := shipping.ShippingOrder{
		TrackingId:  so.TrackingId,
		DateCreated: so.DateCreated,
		Status:      shipping.Status(so.Status),
		Address:     so.Address,
		Country:     so.Country,
		TotalAmount: so.TotalAmount,
		OrderId:     so.OrderId,
	}
	return &result, nil
}

func (s ShippingPgsqlRepository) FindAll(ctx context.Context) (*[]shipping.ShippingOrder, error) {
	var shippingOrders []ShippingOrder
	if err := s.client.WithContext(ctx).Find(&shippingOrders).Error; err != nil {
		return nil, err
	}

	var result []shipping.ShippingOrder
	for _, so := range shippingOrders {
		result = append(result, shipping.ShippingOrder{
			TrackingId:  so.TrackingId,
			DateCreated: so.DateCreated,
			Status:      shipping.Status(so.Status),
			Address:     so.Address,
			Country:     so.Country,
			TotalAmount: so.TotalAmount,
			OrderId:     so.OrderId,
		})
	}

	return &result, nil
}
