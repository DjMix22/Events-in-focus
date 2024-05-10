import json
from pydantic.json import pydantic_encoder

from src.domain.event import Event


class EventRepo:
    def __init__(self, file_path):
        self.file_path = file_path

    def save(self, items) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file_events:
            json.dump(items, file_events, default=pydantic_encoder, ensure_ascii=False, indent=4)

    def load(self) -> list[Event]:
        with open(self.file_path, 'r', encoding='utf-8') as file_events:
            events = json.load(file_events)

        events_obj = [Event.model_validate(event) for event in events]
        return events_obj
