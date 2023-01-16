from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.utils.loader import dp, db, sched
from bot.states.states import AddChannel, DelChannel, AddAdmin, DelAdmin
from bot.filters.admin_filter import IsAdmin


@dp.message_handler(IsAdmin(), commands=['add_channel'], chat_type='private')
async def add_channel(message: types.Message):
    await message.answer('Перешлите пост с канала, который нужно подключить')
    await AddChannel.channel.set()


@dp.message_handler(IsAdmin(), commands=['channels'], chat_type='private')
async def get_all_channels(message: types.Message):
    lst_channels = await db.get_all_info_channels()
    msg = 'Список подключенных каналов:\n1. ID канала\n2. username\n3. Cо скольки просмотров начать следить за постом\n4. Как часто проверять пост\n5. Сколько пост должен набрать за это время, для перепубликации\n\n'
    for channel_id, username, good_view, view_check, time_check in lst_channels:
        msg += f'{channel_id} @{username} - {good_view} - {time_check} - {view_check}\n'
    await message.answer(msg)


@dp.message_handler(IsAdmin(), commands=['del_channel'], chat_type='private')
async def del_channel(message: types.Message):
    await message.answer('Пришлите id канала для удаления')
    await DelChannel.channel_id.set()


@dp.message_handler(IsAdmin(), state=DelChannel.channel_id, chat_type='private')
async def get_id_to_del_channel_id(message: types.Message,  state: FSMContext):
    if await db.is_channel_in_db(message.text):
        await db.del_channel(message.text)
        lst_posts = await db.get_all_tracked_posts_channel(message.text)
        for tracked_id, channel_id, post_id in lst_posts:
            sched.sched.remove_job(str(tracked_id))
            await db.del_view_tracked_post(channel_id, post_id)
        await message.answer('Успешно')
    else:
        await message.answer('Канал не найден')
    await state.finish()


@dp.message_handler(IsAdmin(), commands=['add_admin'], chat_type='private')
async def add_admin(message: types.Message):
    await message.answer('Пришлите id или username пользователя')
    await AddAdmin.user_id.set()


@dp.message_handler(IsAdmin(), state=AddAdmin.user_id, chat_type='private')
async def get_id_add_admin(message: types.Message,  state: FSMContext):
    if await db.is_user_in_db(message.text):
        await db.add_admin(message.text)
        await message.answer('Успешно')
    else:
        await message.answer('Пользователь не найден')
    await state.finish()


@dp.message_handler(IsAdmin(), commands=['del_admin'], chat_type='private')
async def add_admin(message: types.Message):
    await message.answer('Пришлите id или username пользователя')
    await DelAdmin.user_id.set()


@dp.message_handler(IsAdmin(), state=DelAdmin.user_id, chat_type='private')
async def get_id_add_admin(message: types.Message, state: FSMContext):
    if await db.is_user_in_db(message.text):
        await db.del_admin(message.text)
        await message.answer('Успешно')
    else:
        await message.answer('Пользователь не найден')
    await state.finish()
