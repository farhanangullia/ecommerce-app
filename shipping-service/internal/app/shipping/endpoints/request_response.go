package endpoints

type ApiResponse struct {
	Code    int32  `json:"code,omitempty"`
	Type_   string `json:"type,omitempty"`
	Message string `json:"message,omitempty"`
}

type ServiceStatusRequest struct{}

type ServiceStatusResponse struct {
	Err error `json:"err,omitempty"`
}
