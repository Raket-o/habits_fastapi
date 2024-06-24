import aiohttp
import json

from config_data.config import BOT_TOKEN

async def send_message_tg():
# async def send_message_tg(habit_id: int, chat_id: int):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    habit_id = 1
    callback_data_habit_id = f"habit_id{habit_id}"

    kb = {
        "inline_keyboard": [
            [
                {
                    "text": "да",
                    "callback_data": callback_data_habit_id
                },
                {
                    "text": "нет",
                    "callback_data": "register_hand_1"
                },
            ]
        ]
    }

    kb = json.dumps(kb)
    kb = kb.replace(' ', '')

    params = {
        "chat_id": 5203073246,
        "text": "Test",
        "reply_markup": kb
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}", params=params) as response:
            print(await response.json())
