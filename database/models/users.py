from enum import Enum

from sqlalchemy import String, Enum as SqlAlchemyEnum, BigInteger, ForeignKey, select, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database.base import TimeBasedModel, db
from database.models.shops import Cart, CartItem


class User(TimeBasedModel):
    class Type(Enum):
        ADMIN = 'admin'
        USER = 'user'

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True, unique=True)

    phone_number: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    type: Mapped[SqlAlchemyEnum] = mapped_column(SqlAlchemyEnum(Type), default=Type.USER)
    carts: Mapped[list['Cart']] = relationship('Cart', back_populates='user')
    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')

    parent_user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    parent_user: Mapped['User'] = relationship('User', remote_side='User.id', back_populates='referrals')
    referrals: Mapped[list['User']] = relationship('User', back_populates='parent_user')

    async def referral_count(self):
        query = select(func.count(self.__class__.id)).where(User.parent_user_id == self.id)
        return (await db.execute(query)).scalar()

    @property
    def is_admin(self):
        return self.type == self.Type.ADMIN

    @classmethod
    async def add_cart(cls, user_id: int, product_id: int, quantity: int = 1) -> None:
        cart = (await Cart.filter(user_id=user_id)).first()
        if cart is None:
            cart = await Cart.create(user_id=user_id)
        cart_item = (await CartItem.filter(cart_id=cart.id, product_id=product_id)).first()
        if cart_item is not None:
            cart_item.quantity += quantity
            await cart_item.save_model()
        else:
            await CartItem.create(cart_id=cart.id, product_id=product_id, quantity=quantity)

    @classmethod
    async def remove_cart(cls, user_id: int, product_id: int):
        cart = (await Cart.filter(user_id=user_id)).first()
        if not cart:
            return False

        query = select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
        cart_item = (await db.execute(query)).scalar_one_or_none()

        if not cart_item:
            return False

        if cart_item.quantity < 2:
            await db.delete(cart_item)
        else:
            cart_item.quantity -= 1
            db.add(cart_item)

        await CartItem.commit()
        return True
