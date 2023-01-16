from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from bot.utils.loader import dp, db, bot
from bot.states.states import AddChannel


@dp.message_handler(CommandStart(), chat_type='private')
async def bot_start(message: types.Message):
    await db.add_user(message.chat.id, message.chat.username)
    await message.answer('Добро пожаловать!')
