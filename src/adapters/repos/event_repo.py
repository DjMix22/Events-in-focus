import json
from pydantic.json import pydantic_encoder
from pathlib import Path

from src.domain.event import Event


class EventRepo:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.items = []

    def add_event(self, event: Event):
        self.items.append(event)

    def add_events(self, events: list[Event]):
        self.items += events

    def save(self) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file_events:
            json.dump(self.items, file_events, default=pydantic_encoder, ensure_ascii=False, indent=4)

    def load(self) -> list[Event]:
        with open(self.file_path, 'r', encoding='utf-8') as file_events:
            events = json.load(file_events)

        events_obj = [Event.model_validate(event) for event in events]
        file_events.close()
        return events_obj
