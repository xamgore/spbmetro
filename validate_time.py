import json
from datetime import datetime

from history import History

with open('history.json') as f:
    history = History(json.load(f))

# time_re = re.compile(r"(([01]\d|\d|2[0-3])[:-]([0-5]\d)|24[:-]00)")

if __name__ == '__main__':
    failed = False

    for msg in history:
        for name, event in msg.status.items():
            if not event.time: continue
            time: datetime = datetime.strptime(event.time, "%H:%M")

            contains = (time.strftime("%-H:%M") in msg.text) or \
                       (time.strftime("%-H-%M") in msg.text)

            if not contains:
                failed = True
                print(msg)

    if not failed:
        print('ok')
