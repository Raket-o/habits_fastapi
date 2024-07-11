"""queue manager module"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime, timezone, timedelta

from app.database.transactions import get_habits_by_time_db, remove_old_habits_db
from app.utils.send_message import send_message_tg

from config_data.config import LOCAL_UTC


async def schedule_job():
    """queue function"""
    current_datetime = datetime.now(timezone.utc)
    region_datetime = current_datetime

    try:
        if LOCAL_UTC:
            if LOCAL_UTC[0] == "+":
                region_datetime = current_datetime + timedelta(hours=int(LOCAL_UTC[1]))

            elif LOCAL_UTC[0] == "-":
                region_datetime = current_datetime - timedelta(hours=int(LOCAL_UTC[1]))
    except ValueError:
        pass

    region_time = region_datetime.time()
    region_time = region_time.replace(second=0, microsecond=0)

    if region_time.hour == 0 and region_time.minute == 0:
        await remove_old_habits_db()

    habits = await get_habits_by_time_db(region_time)
    if habits:
        for habit in habits:
            telegram_id = habit[1].telegram_id
            habit_id = habit[0].id
            habit_name = habit[0].habit_name
            await send_message_tg(telegram_id, habit_id, habit_name)


schedule = AsyncIOScheduler()
schedule.add_job(schedule_job, "interval", minutes=1)
schedule.start()
