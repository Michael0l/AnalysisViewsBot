from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.utils.loader import dp, db, user_bot, bot
from bot.states.states import AddChannel
from bot.filters.admin_filter import IsAdmin


@dp.message_handler(IsAdmin(), state=AddChannel.channel, chat_type='private', content_types=types.ContentTypes.ANY)
async def add_request(message: types.Message, state: FSMContext):
    if message.forward_from_chat and message.forward_from_chat.type == 'channel':
        if not await db.channel_in_database(message.forward_from_chat.id):
            bot_info = await bot.get_me()
            bot_member = await bot.get_chat_member(message.forward_from_chat.id, bot_info.id)
            if bot_member.status == 'administrator':
                async with state.proxy() as data: 
                    data['channel_id'] = message.forward_from_chat.id
                    data['username'] = message.forward_from_chat.username
                await message.answer('Пришлите количество просмотров, с которого бот должен начать проверки')
                await AddChannel.good_views.set()
            else:
                await message.answer(f'Сначала добавьте бота в админы @{bot_info.username}')
                await state.finish()  
        else:
            await message.answer('Канал уже есть в базе. Отменено')
            await state.finish()
    else:
        await message.answer('Нужно переслать пост с канала!')
        await state.finish()


@dp.message_handler(IsAdmin(), state=AddChannel.good_views, chat_type='private')
async def add_request(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data: 
            data['good_views'] = int(message.text)

        await message.answer('Пришлите разницу по просмотрам')

        await AddChannel.view_check.set()
    else:
        await message.answer('Это не число')


@dp.message_handler(IsAdmin(), state=AddChannel.view_check, chat_type='private')
async def add_request(message: types.Message, state: FSMContext):
    if message.text.isdigit()and int(message.text) >= 10:
        async with state.proxy() as data:
            data['view_check'] = int(message.text)
        await message.answer('Пришлите частоту проверки поста в секундах')
        await AddChannel.time_check.set()
    else:
        await message.answer('Число должно быть больше >=10')


@dp.message_handler(IsAdmin(), state=AddChannel.time_check, chat_type='private')
async def add_request(message: types.Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) >= 10:
        async with state.proxy() as data: 
            data['time_check'] = int(message.text)
            await db.add_channel(**data)
        await state.finish()
        await message.answer('Канал успешно добавлен')
    else:
        await message.answer('Число должно быть  >=10')
