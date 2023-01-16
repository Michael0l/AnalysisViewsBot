from pyrogram import Client
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid
import logging
import asyncio

import bot.utils.loader as loader
from bot.data import config


class UserBot():
    def __init__(self, account, api_id=None, api_hash=None):
        self.app: Client = Client(account, api_id=api_id, api_hash=api_hash)
        self.app.start()

    async def check_recent_posts(self, channel_id, good_views, limit):
        logging.warning(f'Канал {channel_id} - проверка {limit} постов')
        lst_media_group = []
        try:
            async for post in self.app.get_chat_history(channel_id, limit):
                await asyncio.sleep(0.1)

                if post.media_group_id:
                    if post.media_group_id not in lst_media_group:
                        lst_media_group.append(post.media_group_id)
                    else:
                        continue
                        
                if not await loader.db.is_tracked_post(channel_id, post.id):
                    if post.views and post.views > good_views:
                        logging.warning(f'Канал {channel_id} - подозрительный пост {post.id}, просмотры {post.views}, превышения {good_views}')

                        interval_seconds = await loader.db.get_time_check_channel(channel_id)
                        tracked_id = await loader.db.add_tracked_post(channel_id, post.id, post.views)
                        await loader.sched.set_timer_check_post_cheating(tracked_id, channel_id, post.id, interval_seconds[0])
                else:
                    continue

            for tracked_id, post_id in await loader.db.get_all_tracked_post_channel(channel_id):
                if post_id < post.id:
                    logging.warning(f'Канал {channel_id} - удален {post_id} пост - последний {post.id} задача {tracked_id}')
                    
                    loader.sched.sched.remove_job(str(tracked_id))
                    await loader.db.del_view_tracked_post(channel_id, post_id)
                    
        except ChannelInvalid:
            logging.warning(f'Канал {channel_id} - ошибка получения постов')

    async def check_post_cheating(self, channel_id, post_id):
        tracked_id, last_view = await loader.db.get_view_tracked_post(channel_id, post_id)
        view_check = await loader.db.get_view_check_channel(channel_id)
        post = await self.app.get_messages(channel_id, post_id)

        if last_view and post.views - last_view > view_check[0]:
            logging.warning(f'Канал {channel_id} - Перепубликация поста {post_id}, просмотры {post.views}, порошлые {last_view}, превышает {view_check[0]} - { post.views - last_view}')
            await self.resending_message(channel_id, post, tracked_id, channel_id)
        else:
            logging.warning(f'Канал {channel_id} - обновление поста {post_id} - {post.views} просмотров')
            await loader.db.update_view_tracked_post(channel_id, post_id, post.views)

    async def resending_message(self, channel_id, post, tracked_id, chat_id='me'):
        await loader.bot.copy_message(chat_id, post.sender_chat.id, post.id)
        await loader.bot.delete_message(channel_id, post.id)
        loader.sched.sched.remove_job(str(tracked_id))
        await loader.db.del_view_tracked_post(channel_id, post.id)
