import datetime

def get_time(add_time=3):
        tz =  datetime.timezone(datetime.timedelta(hours=add_time), name='МСК')
        now = datetime.datetime.now(tz=tz)
        return now
