from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from ..data import config
from bot.database.main import Database
from ..user_bot.UserBot import UserBot
from ..scheduler.Scheduler import Scheduler




bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db = Database()

sched = Scheduler()

user_bot = UserBot(config.account, config.api_id, config.api_hash)
