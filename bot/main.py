from aiogram.utils import executor
from aiogram import Dispatcher

from .utils.loader import dp, db, sched

from bot.utils.set_bot_commands import set_default_commands
from bot import handlers


async def on_start_up(dp: Dispatcher):
    await set_default_commands(dp)
    await db.create_tables()
    await sched.run_channel_viewing()
    await sched.uploading_cheating_post_to_timer_from_db()


def start_bot():
    executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)
