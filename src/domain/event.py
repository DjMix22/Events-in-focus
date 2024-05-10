from pydantic import BaseModel, Field
import datetime
import enum


class EventTypes(enum.StrEnum):
    Movie = 'movie'
    Concert = 'concert'
    Performance = 'performance'


class TimeSlot(BaseModel):
    start_date: datetime.datetime = Field(description="Время начала")
    price: float = Field(description="Цена")
    place: str = Field(description="Место")


class Event(BaseModel):
    id: int = Field(default=0, description="Уникальный идентификатор события")
    name: str = Field(description="Имя события")
    genre: str = Field(description="Жанр события")
    url: str = Field(description="Ссылка на событие")
    time_slots: list[TimeSlot] = Field(default=[], description="Временной слот")
    event_type: EventTypes = Field(description="Тип события")
