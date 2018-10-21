from datetime import datetime

from structure import History

# checks the time is mentioned in the original message
if __name__ == '__main__':
    failed = False

    for msg in History.load():
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
