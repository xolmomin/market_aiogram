from aiogram import Router

from bot.handlers.private.menu import menu_router
from bot.handlers.private.refferal import referral_router
from bot.handlers.private.products import product_router
from bot.handlers.private.settings import settings_router
from bot.handlers.private.admin import admin_product, admin_menu

main_router = Router()

main_router.include_routers(
    *[
        menu_router,
        referral_router,
        product_router,
        settings_router,
        admin_menu,
        admin_product,
    ]
)
