from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, Enum as SqlAlchemyEnum, Integer, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import TimeBasedModel


class Order(TimeBasedModel):
    class Status(Enum):
        IN_PROGRESS = 'jarayonda'
        PAID = "to'langan"
        CANCELLED = "bekor qilingan"

    user: Mapped['User'] = relationship('User', back_populates='orders')
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    status: Mapped[str] = mapped_column(SqlAlchemyEnum(Status), default=Status.IN_PROGRESS)
    order_items: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='order')


class OrderItem(TimeBasedModel):
    order: Mapped['Order'] = relationship('Order', back_populates='order_items')
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Order.id, ondelete='CASCADE'))
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer)
    product: Mapped['Product'] = relationship('Product', back_populates='order_items')
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'))
