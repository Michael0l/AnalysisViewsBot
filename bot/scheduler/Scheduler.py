from apscheduler.schedulers.asyncio import AsyncIOScheduler

import bot.utils.loader as loader
import logging


class Scheduler:
    def __init__(self):
        self.sched = AsyncIOScheduler({'apscheduler.timezone': 'Europe/Moscow'})#, jobstores=job_stores)
        self.sched.start()

    async def run_channel_viewing(self):
        logging.warning(f'Запуск тайиера просмотра всех каналов')
        self.sched.add_job(self.all_channel_viewing, 'interval', seconds=10)

    async def all_channel_viewing(self):
        lst_channel = await loader.db.get_all_channel()
        for channel_id, good_views in lst_channel:
            await loader.user_bot.check_recent_posts(channel_id, good_views, 20)

    async def uploading_cheating_post_to_timer_from_db(self):
        logging.warning(f'Добавление тасков в таймер с бд')
        
        lst_tracked_posts = await loader.db.get_all_tracked_posts()
        for id, channel_id, post_id in lst_tracked_posts:
            interval_seconds = await loader.db.get_time_check_channel(channel_id)
            await loader.db.update_view_tracked_post(channel_id, post_id, 0)
            await loader.user_bot.check_post_cheating(channel_id, post_id)
            await self.set_timer_check_post_cheating(id, channel_id, post_id, interval_seconds[0])

    async def set_timer_check_post_cheating(self, tracked_id, channel_id, post_id, interval_seconds):
        self.sched.add_job(loader.user_bot.check_post_cheating, 'interval', id=str(tracked_id), seconds=interval_seconds, args=(channel_id, post_id))
