from structure import History, Subway

subway = Subway.load()

# checks the station name is mentioned in the metro.json
if __name__ == '__main__':
    failed = False

    for msg in History.load():
        for station in msg.status.keys():
            if station not in subway.stations:
                print(msg.message_id, station)
                failed = True

    if not failed:
        print('ok')
