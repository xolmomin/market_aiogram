from aiogram import Router
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.filters.admin import IsAdminFilter

admin_menu = Router()


@admin_menu.message(IsAdminFilter(text='Admin'))
async def welcome_bot_with_deeplink(message: Message) -> None:
    markup = [
        [KeyboardButton(text='Add product'), KeyboardButton(text='Show product')],
        [KeyboardButton(text='Add category'), KeyboardButton(text='Show category')],
        [KeyboardButton(text='Back ⬅️')]
    ]
    rkm = ReplyKeyboardBuilder(markup)
    await message.answer('Menyular', reply_markup=rkm.as_markup())
