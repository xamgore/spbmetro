from datetime import datetime

from history import History

if __name__ == '__main__':
    failed = False

    for msg in History.load('history.json'):
        for name, event in msg.status.items():
            if not event.time: continue
            time: datetime = datetime.strptime(event.time, "%H:%M")

            contains = (time.strftime("%-H:%M") in msg.original_text) or \
                       (time.strftime("%-H-%M") in msg.original_text) or \
                       (time.strftime("%-H.%M") in msg.original_text)

            if not contains:
                failed = True
                print(msg)

    if not failed:
        print('ok')
