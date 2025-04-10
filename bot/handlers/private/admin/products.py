from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy_file import File

from bot.filters import IsAdminFilter
from bot.handlers.private.menu import welcome_bot
from bot.states import AddCategory, ChangeCategory, AddProduct
from database import Category, Product

admin_product = Router()

admin_product.message.filter(IsAdminFilter())
admin_product.callback_query.filter(IsAdminFilter())


@admin_product.message(F.text == 'Add product')
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    await state.set_state(AddProduct.name)
    rkm = ReplyKeyboardRemove()
    await message.answer('product nameni kiriting', reply_markup=rkm)


@admin_product.message(AddProduct.name)
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.description)
    await message.answer('product descriptionni kiriting')


@admin_product.message(AddProduct.description)
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(AddProduct.price)
    await message.answer('product priceni kiriting')


@admin_product.message(AddProduct.price, F.text.isdigit())
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    await state.update_data(price=int(message.text))
    await state.set_state(AddProduct.quantity)
    await message.answer('product quantityni kiriting')


@admin_product.message(AddProduct.quantity, F.text.isdigit())
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    await state.update_data(quantity=int(message.text))
    await state.set_state(AddProduct.image)
    await message.answer('product imageni kiriting')


@admin_product.message(and_f(AddProduct.image, F.content_type.in_({ContentType.PHOTO})))
async def welcome_bot_with_deeplink(message: Message, bot: Bot, state: FSMContext) -> None:
    await state.update_data(file_id=message.photo[-1].file_id)
    await state.set_state(AddProduct.category_id)
    categories = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    for category in categories:
        ikm.row(InlineKeyboardButton(text=category.name, callback_data=f'add_category_{category.id}'))

    await message.answer('malumotlar kiritildi', reply_markup=ikm.as_markup())


@admin_product.callback_query(AddProduct.category_id, F.data.startswith('add_category_'))
async def welcome_bot_with_deeplink(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    category_id = callback.data.removeprefix('add_category_')
    await state.update_data(category_id=int(category_id))
    data = await state.get_data()
    data.pop('locale')
    file_obj = await bot.download(data.pop('file_id'))
    file = File(file_obj.read(), content_type='image/jpeg')
    await Product.create(image=file, **data)
    await state.clear()
    await callback.answer('Product qoshildi', show_alert=True)
    await welcome_bot(callback.message)
    await callback.message.delete()


@admin_product.message(F.text == 'Add category')
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    await state.set_state(AddCategory.name)
    rkm = ReplyKeyboardRemove()
    await message.answer('category nomini kiriting', reply_markup=rkm)


@admin_product.message(AddCategory.name)
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    category_name = message.text
    await Category.create(name=category_name)
    await state.clear()
    rkm = ReplyKeyboardRemove()
    await message.answer('category yaratildi !', reply_markup=rkm)
    await welcome_bot(message)


@admin_product.message(F.text == 'Show category')
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    await state.set_state(ChangeCategory.choice)
    categories = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    for category in categories:
        ikm.row(
            InlineKeyboardButton(text=f"{category.name} ✏️", callback_data=f'change_category_{category.id}'),
            InlineKeyboardButton(text=f"❌️", callback_data=f'delete_category_{category.id}'),
        )

    await message.answer("o'zgartiriladigan category ni tanlang", reply_markup=ikm.as_markup())


@admin_product.callback_query(ChangeCategory.choice, F.data.startswith('delete_category_'))
async def welcome_bot_with_deeplink(callback: CallbackQuery, state: FSMContext) -> None:
    category_id = callback.data.removeprefix('delete_category_')
    await Category.delete(_id=int(category_id))
    await state.clear()
    rkm = ReplyKeyboardRemove()
    await callback.message.answer('category ochirildi!', reply_markup=rkm)
    await welcome_bot(callback.message)
    await callback.message.delete()


@admin_product.callback_query(ChangeCategory.choice, F.data.startswith('change_category_'))
async def welcome_bot_with_deeplink(callback: CallbackQuery, state: FSMContext) -> None:
    category_id = callback.data.removeprefix('change_category_')
    await state.update_data(category_id=int(category_id))
    await state.set_state(ChangeCategory.name)
    rkm = ReplyKeyboardRemove()
    await callback.message.answer('category uchun yangi nom kiriting!', reply_markup=rkm)
    await callback.message.delete()


@admin_product.message(ChangeCategory.name)
async def welcome_bot_with_deeplink(message: Message, state: FSMContext) -> None:
    category_name = message.text
    data = await state.get_data()
    category_id = data.pop('category_id')
    await Category.update(_id=category_id, name=category_name)
    print('updated category')
    await state.clear()
    rkm = ReplyKeyboardRemove()
    await message.answer('category ozgartildi !', reply_markup=rkm)
    await welcome_bot(message)
