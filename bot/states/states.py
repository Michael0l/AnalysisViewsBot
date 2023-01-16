from aiogram.dispatcher.filters.state import StatesGroup, State



class AddChannel(StatesGroup):
    channel = State()
    good_views = State()
    time_check = State()
    view_check = State()

class AddAdmin(StatesGroup):
    user_id = State()


class DelChannel(StatesGroup):
    channel_id = State()

class DelAdmin(StatesGroup):
    user_id = State()

