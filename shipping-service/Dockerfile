## BUILD STAGE
FROM golang:1.20-alpine as builder

ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64 \
    GOPROXY=https://goproxy.io,direct

WORKDIR /app/shipping

COPY . .

RUN go build -o app ./cmd/shipping

## DISTRIBUTION
FROM gcr.io/distroless/base:nonroot-amd64

COPY --from=builder /app/shipping/configs/* .
COPY --from=builder /app/shipping/app .

CMD ["./app"]
