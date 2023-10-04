
import grpc
from app.domain.ports.repository import ShippingRepository
from app.pb import shipping_pb2, shipping_pb2_grpc

class ShippingException(Exception):
    def __init__(self, message="Error occured during shipping order creation"):
        self.message = message
        super().__init__(self.message)

class GrpcShippingRepository(ShippingRepository):
    def __init__(self, service_url: str) -> None:
        self.service_url = service_url

    def create_shipping(
        self, address: str, country: str, total_amount: float, order_id: str
    ) -> str:
        with grpc.insecure_channel(self.service_url) as channel:
            stub = shipping_pb2_grpc.ShippingServiceStub(channel)
            response = stub.ShippingOrder(
                shipping_pb2.ShippingOrderRequest(
                    address=address,
                    country=country,
                    total_amount=total_amount,
                    order_id=order_id,
                )
            )
            if response:
                if response.err or response.err != "":
                    raise ShippingException(response.err)
                return response.tracking_id