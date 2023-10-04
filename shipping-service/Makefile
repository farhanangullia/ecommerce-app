GO_VER              ?= go

lint: golangci-lint

.PHONY: ensure-mod lint install-tools test run-local golangci-lint tools pb-compile

install-tools:
	@echo ">  Installing tools..."
	(cd /tmp && go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest)
	(cd /tmp && go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.28)
	(cd /tmp && go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.2)


golangci-lint:
	@echo "==> Checking source code with golangci-lint..."
	@golangci-lint run --out-format code-climate | jq -r '.[] | "\(.location.path):\(.location.lines.begin) \(.description)"'

test:
	@echo ">  Running tests..."
	go test -cover -race -v ./...

run-local: ensure-mod
	cd cmd/shipping && go run main.go

ensure-mod:
	go mod download

pb-compile:
	protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative pb/shipping.proto
