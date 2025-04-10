from aiogram import Router, F
from aiogram.types import Message, KeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.handlers.private.menu import welcome_bot

settings_router = Router()


@settings_router.message(F.text == 'Settings')
async def welcome_bot_with_deeplink(message: Message) -> None:
    markup = [
        [
            KeyboardButton(text='Change language 🇬🇧 🇺🇿'),
            KeyboardButton(text='Notification')
        ],
        [
            KeyboardButton(text='Back ⬅️')
        ]
    ]
    rkm = ReplyKeyboardBuilder(markup)
    await message.answer(_('Settings'), reply_markup=rkm.as_markup())


@settings_router.message(F.text == 'Back ⬅️')
async def welcome_bot_with_deeplink(message: Message) -> None:
    await welcome_bot(message)
