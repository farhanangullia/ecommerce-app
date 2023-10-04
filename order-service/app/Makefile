pb-compile:
	python -m grpc_tools.protoc -I../../shipping-service/pb --python_out=pb/ --pyi_out=pb/ --grpc_python_out=pb/ ../../shipping-service/pb/shipping.proto
	cd pb && sed -i '' 's/^\(import.*pb2\)/from . \1/g' *.py # due to import bug (ref: https://github.com/protocolbuffers/protobuf/issues/1491)

.PHONY: pb-compile 