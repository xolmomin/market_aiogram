from typing import Optional

from aiogram.types import Message

from database import User


async def register_user(message: Message, parent_user_id: Optional[int] = None) -> User:
    user = await User.get(message.from_user.id)
    if user is None:
        await User.create(
            **message.from_user.model_dump(include={'id', 'first_name', 'username'}) | {
                'parent_user_id': parent_user_id})
    return user
