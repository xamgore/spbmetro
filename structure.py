import re
from typing import List, Dict, Iterator, Set

alex_nevsky = re.compile(r'(ст\.?|ст[а-я]+)?\s*(пл[а-я]+|пл\.?)?\s*(ал\.?|алекс[а-я]*)\s*не\.?[а-я]*\s*-?', re.U)
pl_muzhestva = re.compile(r'(ст\.?|ст[а-я]+)?\s*(пл[а-я]+|пл\.?)?\s*(муж[а-я]*)\s*-?', re.U)
pl_vosstan = re.compile(r'(ст\.?|ст[а-я]+)?\s*(пл[а-я]+|пл\.?)?\s*(восст[а-я]*)\s*-?', re.U)
pl_lenina = re.compile(r'(ст\.?|ст[а-я]+)?\s*(пл[а-я]+|пл\.?)?\s*(лени[а-я]*)\s*-?', re.U)
pl_sennaya = re.compile(r'(ст\.?|ст[а-я]+)?\s*(сенн[а-я]*)\s*(пл[а-я]*|пл\.?)?', re.U)
st_st = re.compile(r'ст\.\s*ст\.', re.U)
# невский проспект, невский пр- гостиный
# ул.дыбенко, пр.ветеранов, станции гражданский пр. -девяткино открыты

time_re = re.compile(r"([01]\d|\d|2[0-3])[:\-.]([0-5]\d)")


class Event:
    def __init__(self, name, data) -> None:
        self.name: str = name
        self.time: str = data.get('время', None)
        self.open: str = data.get('открыта', None)
        self.reason: str = data.get('причина', None)


class Message:
    def __init__(self, data) -> None:
        self._data = data
        self.message_id: int = data['message_id']
        self.date: int = data['date']
        self.status: Dict[str, Event] = {k: Event(k, v) for k, v in data.get('status', {}).items()}

        self.original_text: str = data['text']

        t = self.original_text.lower().rstrip('. \n')
        t = t.replace('станция', ' ст. ')
        t = re.sub(time_re, " \\1:\\2 ", t)
        t = re.sub(alex_nevsky, " ст. площадь александра невского ", t)
        t = re.sub(pl_muzhestva, " ст. площадь мужества ", t)
        t = re.sub(pl_vosstan, " ст. площадь восстания ", t)
        t = re.sub(pl_lenina, " ст. площадь ленина ", t)
        t = re.sub(pl_sennaya, " сенная площадь ", t)
        t = re.sub(st_st, " ст. ", t)
        t = t.replace('ин-т', ' институт ')
        self.text = t


class History:
    def __init__(self, messages: List) -> None:
        self.messages: Dict[int, Message] = {int(m.message_id): m for m in map(Message, messages)}


    def __iter__(self) -> Iterator[Message]:
        return iter(self.messages.values())


    @staticmethod
    def load(path: str = 'history.json'):
        with open(path or 'history.json') as f:
            import json
            return History(json.load(f))


class Station:
    def __init__(self, name: str, line, vestibules: int = 1):
        self.name: str = name
        self.line: Line = line
        self.vestibules_number: int = vestibules
        self.transfers: Set[Station] = set()


class Line:
    def __init__(self, number: int, data: Dict):
        self.number: int = number
        self.alias: str = data['alias']
        self.color: str = data['color']
        self.stations: Dict[str, Station] = {st: Station(st, self) for st in data['stations']}


class Subway:
    def __init__(self, data) -> None:
        self.lines: List[Line] = [Line(num, data) for num, data in data['lines'].items()]

        self.stations: Dict[str, Station] = \
            {st.name: st for line in self.lines for st in line.stations.values()}

        for bunch in data.get('transfers', []):
            for idx, station in enumerate(self.stations[st] for st in bunch):
                station.transfers = set(bunch[:idx] + bunch[idx + 1:])

        for station, number in data.get('vestibules', {}).items():
            self.stations[station].vestibules_number = number


    @staticmethod
    def load(path: str = None):
        with open(path or 'metro.json') as f:
            import json
            return Subway(json.load(f))
