from typing import List, Dict, Iterator


class Event:
    def __init__(self, name, data) -> None:
        self.name: str = name
        self.time: str = data.get('время', None)
        self.open: str = data.get('открыта', None)
        self.reason: str = data.get('причина', None)


class Message:
    def __init__(self, data) -> None:
        self.message_id: int = data['message_id']
        self.date: int = data['date']
        self.text: str = data['text']
        self.status: Dict[str, Event] = {k: Event(k, v) for k, v in data.get('status', {}).items()}


class History:
    def __init__(self, messages: List) -> None:
        self.messages: List[Message] = list(map(Message, messages))

    def __iter__(self) -> Iterator[Message]:
        return iter(self.messages)

    @staticmethod
    def load(path):
        with open(path) as f:
            import json
            return History(json.load(f))
