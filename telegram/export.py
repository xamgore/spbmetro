import json
import os
from pathlib import Path
from pyrogram import Client
from pyrogram.api.errors import FloodWait

from preprocess import fix_text, spell_dict
import time

os.chdir(os.path.dirname(os.path.realpath(__file__)))
app = Client("igor_main")

messages = []  # List that will contain all the messages of the target chat
offset_id = 0  # ID of the last message of the chunk
target = "@spbmetro"

if __name__ == '__main__':
    app.start()

    while True:
        try:
            chat = app.get_history(target, offset_id=offset_id)
        except FloodWait as e:
            # For very large chats the method call can raise a FloodWait
            print(f"waiting {e.x}")
            time.sleep(e.x)  # Sleep X seconds before continuing
            continue

        if not chat.messages:
            break

        for m in chat.messages:
            if m.text is not None:
                messages.append({
                    'message_id': m.message_id,
                    'date':       m.date,
                    'original':   m.text,
                    'text':       fix_text(m.text, spell_dict()),
                })

        offset_id = chat.messages[-1].message_id
        print(f"Messages: {len(messages)}")

    app.stop()

    content = json.dumps(messages, ensure_ascii=False, indent=2)
    Path('../history.json').write_text(content)

# # display fixed texts:
# from structure import History
# if __name__ == '__main__':
#     for m in History.load().messages.values():
#         if m.original_text != m.text:
#             print(f'{m.text}\n{m.original_text}\n')
