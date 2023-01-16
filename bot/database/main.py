from bot.utils.now_date import get_time
import aiosqlite
from  ..data import config


class Database:
    async def create_tables(self):
        async with aiosqlite.connect(config.db_path) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS "users" (
                            	"id"	INTEGER NOT NULL,
                            	"user_id"	INTEGER,
                            	"admin"	INTEGER,
                            	"reg_time"	TEXT,
                            	PRIMARY KEY("id"))''')
                                
            await db.execute('''CREATE TABLE IF NOT EXISTS "channels" (
                            	"id"	INTEGER NOT NULL,
                            	"channel_id"	INTEGER,
                            	"time"	INTEGER,
                            	"view"	INTEGER,
                            	PRIMARY KEY("id"))''')

    async def add_user(self, user_id, username):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            if not await ex.fetchone():
                now = get_time().strftime("%d.%m.%Y %H:%M")
                await db.execute("INSERT INTO `users` ('user_id', 'username', 'admin', 'reg_time') VALUES (?,?,?)", (user_id, username, 0, now))
                await db.commit()
            else:
                await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
                await db.commit()

    async def is_admin(self, user_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT admin FROM users WHERE user_id = ?", (user_id,))
            return await ex.fetchone()
            

    async def add_channel(self, channel_id, username, good_views, view_check, time_check):
        async with aiosqlite.connect(config.db_path) as db:
            await db.execute("INSERT INTO `channels` ('channel_id', 'username', 'good_views', 'view_check', 'time_check') VALUES (?,?,?,?,?)", (channel_id, username, good_views, view_check, time_check))
            await db.commit()
            
    async def channel_in_database(self, channel_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT id FROM channels WHERE channel_id = ?", (channel_id,))
            return 

    async def add_tracked_post(self, channel_id, post_id, view):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT * FROM tracked_posts WHERE channel_id = ? AND post_id = ?", (channel_id, post_id))
            if not await ex.fetchone():
                a = await db.execute("INSERT INTO `tracked_posts` ('channel_id', 'post_id', 'view') VALUES (?,?,?)", (channel_id, post_id, view))
                await db.commit()
                return a.lastrowid
            else:
                print('Не сохр', channel_id, post_id, view)


    async def get_all_tracked_post_channel(self, channel_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT id, post_id FROM tracked_posts WHERE channel_id = ?", (channel_id, ))
            return await ex.fetchall()

    async def is_tracked_post(self, channel_id, post_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT id FROM tracked_posts WHERE channel_id = ? AND post_id = ?", (channel_id, post_id))
            return await ex.fetchone()

    async def update_view_tracked_post(self, channel_id, post_id, view):
        async with aiosqlite.connect(config.db_path) as db:
            await db.execute("UPDATE tracked_posts SET view = ? WHERE channel_id = ? AND post_id = ?", (view, channel_id, post_id))
            await db.commit()


    async def del_view_tracked_post(self, channel_id, post_id):
        async with aiosqlite.connect(config.db_path) as db:
            await db.execute("DELETE FROM tracked_posts WHERE channel_id = ? AND post_id = ?", (channel_id, post_id))
            await db.commit()

    async def get_view_tracked_post(self, channel_id, post_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT id, view FROM tracked_posts WHERE channel_id = ? AND post_id = ?", (channel_id, post_id))
            return await ex.fetchone()

    async def get_view_check_channel(self, channel_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT view_check FROM channels WHERE channel_id = ?", (channel_id, ))
            return await ex.fetchone()

    async def get_all_channel(self):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT channel_id, good_views FROM channels")
            return await ex.fetchall()

    async def get_all_tracked_posts(self):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT id, channel_id, post_id FROM tracked_posts")
            return await ex.fetchall()

    async def get_time_check_channel(self, channel_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT time_check FROM channels WHERE channel_id = ?", (channel_id, ))
            return await ex.fetchone()

    async def get_all_info_channels(self):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT channel_id, username, good_views, view_check, time_check FROM channels")
            return await ex.fetchall()

    async def is_channel_in_db(self, channel_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT id FROM channels WHERE channel_id = ? ", (channel_id, ))
            return await ex.fetchone()

    async def del_channel(self, channel_id):
        async with aiosqlite.connect(config.db_path) as db:
            await db.execute("DELETE FROM channels WHERE channel_id = ?", (channel_id, ))
            await db.commit()

    async def get_all_tracked_posts_channel(self, channel_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT id, channel_id, post_id FROM tracked_posts WHERE channel_id = ? ", (channel_id, ))
            return await ex.fetchall()

    async def is_user_in_db(self, user_id):
        async with aiosqlite.connect(config.db_path) as db:
            ex = await db.execute("SELECT id FROM users WHERE user_id = ? OR username = ?", (user_id, user_id))
            return await ex.fetchone()

    async def add_admin(self, user_id):
        async with aiosqlite.connect(config.db_path) as db:
            await db.execute("UPDATE users SET admin = 1 WHERE user_id = ? OR username = ?", (user_id, user_id))
            await db.commit()

    async def del_admin(self, user_id):
        async with aiosqlite.connect(config.db_path) as db:
            await db.execute("UPDATE users SET admin = 0 WHERE user_id = ? OR username = ?", (user_id, user_id))
            await db.commit()