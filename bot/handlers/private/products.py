from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import User, Category, Product

product_router = Router()


@product_router.message(F.text == 'Categories')
async def welcome_bot_with_deeplink(message: Message) -> None:
    categories = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    if len(categories):
        for category in categories:
            ikm.row(InlineKeyboardButton(text=category.name, callback_data=F"category_{category.id}"))
        ikm.adjust(2)
        await message.answer('Categories', reply_markup=ikm.as_markup())
    else:
        await message.answer('No categories')


def make_product(product):
    ikm = InlineKeyboardBuilder()
    ikm.row(InlineKeyboardButton(text=f"{product.name} ({product.price} 💵)", callback_data=F"product_{product.id}"))
    ikm.row(
        InlineKeyboardButton(text='⏪Previous', callback_data=F"product_previous_{product.id}_{product.category_id}"),
        InlineKeyboardButton(text='Add to Cart 🛒', callback_data=F"product_add_cart_{product.id}"),
        InlineKeyboardButton(text='Next ⏩️', callback_data=F"product_next_{product.id}_{product.category_id}"),
    )
    if product.image:
        file = FSInputFile(product.image['url'])
    else:
        file = "https://cdn.vectorstock.com/i/500p/46/50/missing-picture-page-for-website-design-or-mobile-vector-27814650.jpg"
    caption = (f"<b>Name</b>: {product.name}\n"
               f"<b>Price</b>: {product.price} usd\n"
               f"<b>Description</b>: {product.description}")
    return file, caption, ikm.as_markup()


@product_router.callback_query(F.data.startswith('category_'))
async def welcome_bot(callback: CallbackQuery, bot: Bot) -> None:
    category_id = callback.data.removeprefix('category_')
    product = await Product.get_next_product_by_category_id(int(category_id), 0)
    if product:
        await callback.message.delete()
        file, caption, ikm = make_product(product)
        await callback.message.answer_photo(file, caption, reply_markup=ikm, parse_mode=ParseMode.HTML)
    else:
        await callback.answer('No Product', show_alert=True)


@product_router.callback_query(F.data.startswith('product_next_'))
async def welcome_bot(callback: CallbackQuery) -> None:
    product_id, category_id = map(int, callback.data.removeprefix('product_next_').split('_'))
    product = await Product.get_next_product_by_category_id(category_id, product_id)
    if product is None:
        await callback.answer('This is last Product', show_alert=True)
        return
    file, caption, ikm = make_product(product)
    await callback.message.edit_media(InputMediaPhoto(media=file, caption=caption, parse_mode=ParseMode.HTML),
                                      callback.inline_message_id, reply_markup=ikm)
    # await callback.message.answer_photo(file, caption, reply_markup=ikm, parse_mode=ParseMode.HTML)


@product_router.callback_query(F.data.startswith('product_previous_'))
async def welcome_bot(callback: CallbackQuery) -> None:
    product_id, category_id = map(int, callback.data.removeprefix('product_previous_').split('_'))
    product = await Product.get_prev_product_by_category_id(category_id, product_id)
    if product is None:
        await callback.answer('This is first Product', show_alert=True)
    file, caption, ikm = make_product(product)
    await callback.message.edit_media(InputMediaPhoto(media=file, caption=caption, parse_mode=ParseMode.HTML),
                                      callback.inline_message_id, reply_markup=ikm)


@product_router.callback_query(F.data.startswith('product_add_cart_'))
async def welcome_bot(callback: CallbackQuery) -> None:
    product_id = int(callback.data.removeprefix('product_add_cart_'))
    await User.add_cart(callback.from_user.id, product_id)
    await callback.answer('Added to Cart', show_alert=True)


@product_router.callback_query(F.data.startswith('product_remove_cart_'))
async def welcome_bot(callback: CallbackQuery) -> None:
    product_id = int(callback.data.removeprefix('product_remove_cart_'))
    has_deleted = await User.remove_cart(callback.from_user.id, product_id)
    if has_deleted:
        await callback.message.delete()
        await callback.answer('Remove from Cart', show_alert=True)
    else:
        await callback.answer('No cart items', show_alert=True)
