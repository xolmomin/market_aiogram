from typing import Optional

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, JOIN_TRANSITION
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, ChatMemberUpdated
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from bot.buttons import MY_REFERRALS, HELP, WELCOME_TEXT
from bot.utils import register_user
from database import User, CartItem

menu_router = Router()

#
# @menu_router.my_chat_member()
# async def welcome_bot_with_deeplink(message: ChatMemberUpdated) -> None:
#     result = JOIN_TRANSITION.check(old=message.old_chat_member, new=message.new_chat_member)
#     print(result)


@menu_router.message(CommandStart(True, True))
async def welcome_bot_with_deeplink(message: Message, command: Command) -> None:
    data = command.args
    if '_' in data:
        product_id = data.removeprefix('product_')
        user = await register_user(message)
        await User.add_cart(user.id, int(product_id))
        await message.answer("Cartga qoshildi")
    else:
        if data.isdigit():
            await welcome_bot(message, int(data))
        else:
            await welcome_bot(message)


@menu_router.message(CommandStart())
async def welcome_bot(message: Message, parent_user_id: Optional[int] = None) -> None:
    user = await register_user(message, parent_user_id)
    markup = [
        [KeyboardButton(text='Categories')],
        [KeyboardButton(text=HELP), KeyboardButton(text='My cart 🛒'), KeyboardButton(text=MY_REFERRALS)],
        [KeyboardButton(text='Settings')]
    ]
    if user.is_admin:
        markup[-1].append(KeyboardButton(text='Admin'))
    rkm = ReplyKeyboardBuilder(markup)
    await message.answer(_(WELCOME_TEXT), reply_markup=rkm.as_markup())


@menu_router.message(F.text == 'My cart 🛒')
async def show_my_carts(message: Message) -> None:
    cart_items = await CartItem.get_by_user_cart(message.from_user.id)
    if cart_items:
        ikm = InlineKeyboardBuilder()
        for cart in cart_items:
            ikm.row(
                InlineKeyboardButton(text=cart.product.name, callback_data=f"12345678"),
                InlineKeyboardButton(text="➕", callback_data=f'product_add_cart_{cart.product_id}'),
                InlineKeyboardButton(text="➖", callback_data=f'product_remove_cart_{cart.product_id}'),

            )
        await message.answer('My cart items', reply_markup=ikm.as_markup())
    else:
        await message.answer('No cart items')
