import time

import json
from pyrogram import Client, Message
from pyrogram.api.errors import FloodWait

app = Client("igor_main")

messages = []  # List that will contain all the messages of the target chat
offset_id = 0  # ID of the last message of the chunk
target = "@spbmetro"

if __name__ == '__main__':
    app.start()

    while True:
        try:
            h = app.get_history(target, offset_id=offset_id)
        except FloodWait as e:
            # For very large chats the method call can raise a FloodWait
            print(f"waiting {e.x}")
            time.sleep(e.x)  # Sleep X seconds before continuing
            continue

        if not h.messages:
            break

        keys = ('message_id', 'date', 'text')
        with_text = (m for m in h.messages if m.text is not None)
        messages += [{k: getattr(m, k) for k in keys} for m in with_text]

        offset_id = h.messages[-1].message_id
        print(f"Messages: {len(messages)}")

    app.stop()

    with open('history.json', 'w') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)
