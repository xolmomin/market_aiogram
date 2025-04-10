from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton
from aiogram.utils.deep_linking import create_deep_link
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import Product

inline_router = Router()


@inline_router.inline_query()
async def get_inline_product_query(inline_query: InlineQuery) -> None:
    results = []
    if len(inline_query.query):
        products = await Product.filter_startswith(inline_query.query)
    else:
        products = await Product.get_all()
    bot_data = await inline_query.bot.me()

    for product in products:
        link = create_deep_link(bot_data.username, 'start', f"product_{product.id}", encode=True)
        ikm = InlineKeyboardBuilder()
        ikm.row(InlineKeyboardButton(text='Add to cart', url=link))

        results.append(
            InlineQueryResultArticle(
                id=str(product.id),
                title=f"{product.name}\n{product.price}﹩",
                description=product.description,
                input_message_content=InputTextMessageContent(
                    message_text=f"{product.name}\n{product.price}﹩",

                ),
                reply_markup=ikm.as_markup()
            )
        )
    await inline_query.answer(results, cache_time=1)
