from typing import Optional

from aiogram.filters import Filter
from aiogram.types import Message

from database import User


class IsAdminFilter(Filter):

    def __init__(self, *, text: Optional[str] = None) -> None:
        self.text = text

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        user = await User.get(user_id)

        if self.text is not None:
            return user.is_admin and message.text == self.text
        return user.is_admin
