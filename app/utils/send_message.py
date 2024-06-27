import aiohttp
import json

from config_data.config import BOT_TOKEN


async def send_message_tg(telegram_id: int, habit_id: int, habit_name: str) -> None:
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    txt = f"Вы выполнили свою привычку: {habit_name}?"

    kb = {
        "inline_keyboard": [
            [
                {
                    "text": "да",
                    "callback_data": f"completed_habit={habit_id}"
                },
                {
                    "text": "нет",
                    "callback_data": f"did_not_completed_habit={habit_id}"
                },
            ]
        ]
    }

    kb = json.dumps(kb)
    kb = kb.replace(' ', '')

    params = {
        "chat_id": telegram_id,
        "text": txt,
        "reply_markup": kb
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{url}", params=params) as response:
            print(await response.json())
