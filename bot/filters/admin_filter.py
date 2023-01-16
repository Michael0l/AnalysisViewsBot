from aiogram.dispatcher.filters import Filter
from bot.utils.loader import db


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message):
        is_admin = await db.is_admin(message.from_user.id)
        return is_admin[0]