import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import FSMI18nMiddleware, I18n
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager

from bot.handlers import main_router
from bot.inlinemode import inline_router
from config import conf
from database.base import db


WEB_SERVER_HOST = "localhost"
WEB_SERVER_PORT = 8082

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "my-secret"
BASE_WEBHOOK_URL = conf.web.DOMAIN


async def startup(dispatcher: Dispatcher, bot: Bot) -> None:
    await db.create_all()
    # Configure Storage
    os.makedirs("./media/attachment", 0o777, exist_ok=True)
    container = LocalStorageDriver("./media").get_container("attachment")
    StorageManager.add_storage("default", container)
    base_url = f"https://{BASE_WEBHOOK_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(base_url, secret_token=WEBHOOK_SECRET)

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

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dispatcher, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

    # await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
