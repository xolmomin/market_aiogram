import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import FSMI18nMiddleware, I18n
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager

from bot.handlers import main_router
from bot.inlinemode import inline_router
from config import conf
from database.base import db


async def startup(dispatcher: Dispatcher, bot: Bot) -> None:
    await db.create_all()
    # Configure Storage
    os.makedirs("./media/attachment", 0o777, exist_ok=True)
    container = LocalStorageDriver("./media").get_container("attachment")
    StorageManager.add_storage("default", container)

    print('database yaratildi')


async def shutdown(dispatcher: Dispatcher, bot: Bot) -> None:
    await db.drop_all()
    print('database ochirildi')


async def main() -> None:
    bot = Bot(conf.bot.TOKEN)
    dispatcher = Dispatcher()
    dispatcher.startup.register(startup)
    # dispatcher.shutdown.register(shutdown)
    i18n = I18n(path="locales")
    dispatcher.update.outer_middleware(FSMI18nMiddleware(i18n))
    dispatcher.include_routers(*[
        main_router, inline_router
    ])
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
