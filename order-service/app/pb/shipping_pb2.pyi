from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceStatusRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ServiceStatusReply(_message.Message):
    __slots__ = ["err"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    err: str
    def __init__(self, err: _Optional[str] = ...) -> None: ...

class ShippingOrderRequest(_message.Message):
    __slots__ = ["address", "country", "total_amount", "order_id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    address: str
    country: str
    total_amount: float
    order_id: str
    def __init__(self, address: _Optional[str] = ..., country: _Optional[str] = ..., total_amount: _Optional[float] = ..., order_id: _Optional[str] = ...) -> None: ...

class ShippingOrderReply(_message.Message):
    __slots__ = ["err", "tracking_id"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    TRACKING_ID_FIELD_NUMBER: _ClassVar[int]
    err: str
    tracking_id: str
    def __init__(self, err: _Optional[str] = ..., tracking_id: _Optional[str] = ...) -> None: ...

class ShippingOrder(_message.Message):
    __slots__ = ["address", "country", "total_amount", "order_id", "date_created", "status"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    DATE_CREATED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    address: str
    country: str
    total_amount: float
    order_id: str
    date_created: str
    status: str
    def __init__(self, address: _Optional[str] = ..., country: _Optional[str] = ..., total_amount: _Optional[float] = ..., order_id: _Optional[str] = ..., date_created: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class FindShippingRequest(_message.Message):
    __slots__ = ["tracking_id"]
    TRACKING_ID_FIELD_NUMBER: _ClassVar[int]
    tracking_id: str
    def __init__(self, tracking_id: _Optional[str] = ...) -> None: ...

class FindShippingReply(_message.Message):
    __slots__ = ["err", "shipping_order"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    SHIPPING_ORDER_FIELD_NUMBER: _ClassVar[int]
    err: str
    shipping_order: ShippingOrder
    def __init__(self, err: _Optional[str] = ..., shipping_order: _Optional[_Union[ShippingOrder, _Mapping]] = ...) -> None: ...

class GetAllShippingRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetAllShippingReply(_message.Message):
    __slots__ = ["err", "shipping_orders"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    SHIPPING_ORDERS_FIELD_NUMBER: _ClassVar[int]
    err: str
    shipping_orders: _containers.RepeatedCompositeFieldContainer[ShippingOrder]
    def __init__(self, err: _Optional[str] = ..., shipping_orders: _Optional[_Iterable[_Union[ShippingOrder, _Mapping]]] = ...) -> None: ...
