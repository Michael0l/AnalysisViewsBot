from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Перезапуск бота"),
            types.BotCommand("channels", "Подключенные каналы"),
            types.BotCommand("add_channel", "Добавить канал"),
            types.BotCommand("del_channel", "Удалить канал"),
            types.BotCommand("add_admin", "Добавить админа"),
            types.BotCommand("del_admin", "Удалить админа"),
        ]
    )
