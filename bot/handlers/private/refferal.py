from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from bot.buttons.sub_menus import MY_REFERRALS
from database import User

referral_router = Router()


@referral_router.message(F.text == __(MY_REFERRALS))
async def welcome_bot(message: Message, bot: Bot) -> None:
    user = await User.get(message.from_user.id)

    link = await create_start_link(bot, str(message.from_user.id), encode=True)
    count = await user.referral_count()
    text = _('My referrals count: {n}\nMy referral link <a href="{link}">Qo\'shiling</a>'.format(n=count, link=link))
    rkm = ReplyKeyboardRemove()
    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=rkm)
