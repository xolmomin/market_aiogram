from sqlalchemy import Float, String, Integer, ForeignKey, BigInteger, select
from sqlalchemy.orm import mapped_column, Mapped, relationship, selectinload
from sqlalchemy_file import ImageField

from database.base import BaseModel, TimeBasedModel, db


class Category(BaseModel):
    name: Mapped[str] = mapped_column(String)
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')


class Product(TimeBasedModel):
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    image: Mapped[str] = mapped_column(ImageField(thumbnail_size=(128, 128)), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    category: Mapped['Category'] = relationship('Category', back_populates='products')
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('categories.id', ondelete='CASCADE'))
    cart_items: Mapped[list['CartItem']] = relationship('CartItem', back_populates='product')
    order_items: Mapped[list['OrderItem']] = relationship('OrderItem', back_populates='product')

    @classmethod
    async def filter_startswith(cls, query: str):
        return (await db.execute(select(cls).where(cls.name.istartswith(query)))).scalars().all()

    @classmethod
    async def get_products_by_category_id(cls, category_id: int):
        return (
            await db.execute(select(cls).where(cls.category_id == category_id).order_by(cls.id.asc()))).scalars().all()

    @classmethod
    async def get_next_product_by_category_id(cls, category_id: int, product_id: int):
        """
        select *
        from products
        where category_id = 1
          and id > 1
        order by id
        limit 1;
        """
        return (
            await db.execute(
                select(cls).where(cls.category_id == category_id, cls.id > product_id).order_by(cls.id.asc()))).scalar()

    @classmethod
    async def get_prev_product_by_category_id(cls, category_id: int, product_id: int):
        """
        select *
        from products
        where category_id = 1
          and id < 4
        order by id desc
        limit 1;
        """
        return (
            await db.execute(select(cls).where(cls.category_id == category_id, cls.id < product_id).order_by(
                cls.id.desc()))).scalar()


class Cart(BaseModel):
    user: Mapped['User'] = relationship('User', back_populates='carts')
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), unique=True)

    cart_items: Mapped[list['CartItem']] = relationship('CartItem', back_populates='cart')


class CartItem(BaseModel):
    product: Mapped['Product'] = relationship('Product', back_populates='cart_items')
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] = mapped_column(Integer)
    cart: Mapped['Cart'] = relationship('Cart', back_populates='cart_items')
    cart_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('carts.id', ondelete='CASCADE'))

    @classmethod
    async def get_by_user_cart(cls, user_id: int):
        query = (
            select(cls)
            .join(Cart)
            .options(selectinload(cls.product), selectinload(cls.cart))
            .where(Cart.user_id == user_id)
        )
        return (await db.execute(query)).scalars().all()
