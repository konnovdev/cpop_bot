import json
import logging

import requests
from pyrogram.types import Message

base_url = "https://api.cng.tw/v1/"
messages_url = base_url + "messages?token=uiehJSeqwWRWEOVP31WQsfafh23F"


def save_message(message: Message):
    try:
        object_to_send = json.dumps(
            {
                "telegramSenderId": f"{str(message.from_user.id)}",
                "telegramChatId": f"{str(message.chat.id)}",
                "telegramMessageId": f"{str(message.message_id)}",
                "text": f"{str(message.text)}",
                "timestamp": f"{message.date}"
            }
        )
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'Connection': 'keep-alive'}
        logging.debug(f"body: {str(object_to_send)}")
        requests.post(messages_url, data=object_to_send, headers=headers)
    except:
        pass
