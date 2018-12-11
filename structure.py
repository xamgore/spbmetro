from pathlib import Path
import re
from typing import List, Dict, Iterator, Set
import json


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
        self.original_text: str = data['original']
        self.text: str = data['text']

    def __repr__(self):
        return f'<Msg(id={self.message_id}, text="{self.text}")>'


class History:
    def __init__(self, messages: List) -> None:
        self.messages: Dict[int, Message] = {int(m.message_id): m for m in map(Message, messages)}


    def __iter__(self) -> Iterator[Message]:
        return iter(self.messages.values())


    def __repr__(self):
        return f'<History(messages={len(self.messages)})>'


    @staticmethod
    def load(path: str = 'history.json'):
        content = (Path(__file__).parent / (path or 'history.json')).read_text()
        return History(json.loads(content))


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
    def load(path: str = 'metro.json'):
        content = (Path(__file__).parent / (path or 'metro.json')).read_text()
        return Subway(json.loads(content))
