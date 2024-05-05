import datetime
from enum import StrEnum
import dateparser
from bs4 import BeautifulSoup
from tqdm import tqdm

from adapters.utils import get_page
from domain.event import Event, TimeSlot, EventTypes


class PosterEventTypes(StrEnum):
    Movie = 'movies'
    Concerts = 'concerts'
    Performances = 'performances'


class PosterParser:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_movies(self, start_date: datetime.datetime, end_date: datetime.datetime) -> list[Event]:
        uri = self.build_uri_for_main_page(start_date=start_date, end_date=end_date, event_type=PosterEventTypes.Movie)
        url = self.build_url(uri)
        page = get_page(url)

        page_parser = BeautifulSoup(page, "html.parser")

        block_movies = page_parser.find("div", class_="S52Wl")
        block_movies_children = block_movies.findAll("div", class_="oP17O")
        movies = []

        for movie in tqdm(block_movies_children, colour="green", desc="Parsing movies"):
            name_url = movie.find("a", class_="CjnHd y8A5E nbCNS yknrM")

            if not name_url:
                continue

            name = name_url.text
            url_movie = self.build_url(name_url['href'])
            genre = movie.find("div", class_="S_wwn").text
            formatted_genre = genre.split()[-1]

            date_string = url_movie.split('/')[-2]
            date_object = datetime.datetime.strptime(date_string, "%d-%m-%Y")

            time_slots = self.get_time_slots_film(url=url_movie, date=date_object)

            movies.append(Event(
                name=name,
                genre=formatted_genre,
                event_type=EventTypes.Movie,
                url=url_movie,
                time_slots=time_slots
            ))

        return movies

    @staticmethod
    def get_time_slots_film(url: str, date: datetime.datetime) -> list[TimeSlot]:
        page = get_page(url)
        page_parser = BeautifulSoup(page, "html.parser")

        block_places = page_parser.find("div", class_="S52Wl")
        if not block_places:
            return []
        block_places_children = block_places.findAll("div", class_="PqAdz")

        time_slots = []
        for place_time_slot in block_places_children:
            place = place_time_slot.find("a", class_="CjnHd y8A5E MnbCM")
            if not place:
                continue
            formatted_place = place.text

            block_time_slots = place_time_slot.find("div", class_="bOvGC k15XR")
            time_slots_place = block_time_slots.findAll("div", class_="KS9_D")

            for time_slot in time_slots_place:
                price = time_slot.find("div", class_="ImmXK")
                if price is None:
                    continue
                price = price.text.split()
                if len(price) < 2 or not price[1].isdigit():
                    continue
                formatted_price = float(price[1])

                start_time = time_slot.find("div", class_="WVR9s").text
                start_date = date.strftime("%Y-%m-%d")
                start_datetime = datetime.datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")

                time_slots.append(TimeSlot(
                    start_date=start_datetime,
                    price=formatted_price,
                    place=formatted_place
                ))
        return time_slots

    def get_concerts_performances(self, start_date: datetime.datetime, end_date: datetime.datetime,
                                  event_type: PosterEventTypes) -> list[Event]:
        uri = self.build_uri_for_main_page(start_date=start_date, end_date=end_date,
                                           event_type=event_type)
        url = self.build_url(uri)
        page = get_page(url)

        page_parser = BeautifulSoup(page, "html.parser")

        block_events = page_parser.find("div", class_="S52Wl")
        block_events_children = block_events.findAll("div", class_="oP17O")
        events = []

        for event in tqdm(block_events_children, colour="green", desc=f"Parsing {event_type}"):
            name_url = event.find("a", class_="CjnHd y8A5E nbCNS yknrM")
            if not name_url:
                continue

            name = name_url.text
            url_event = self.build_url(name_url['href'])

            price = event.find("a", class_="CjnHd y8A5E L_ilg tCbLK faVCW")
            if price is None:
                continue
            price = price.text.split()
            if len(price) < 2 or not price[1].isdigit():
                continue
            formatted_price = float(price[1])

            genre = event.find("div", class_="S_wwn").text
            date_place = event.find("div", class_="_JP4u").text.split(", ")
            formatted_start_date = dateparser.parse(date_place[0])

            if formatted_start_date.hour == 0:
                continue
            place = date_place[1]

            event_types = {
                PosterEventTypes.Concerts: EventTypes.Concert,
                PosterEventTypes.Performances: EventTypes.Performance
             }

            time_slot = TimeSlot(
                start_date=formatted_start_date,
                price=formatted_price,
                place=place
            )
            events.append(Event(
                name=name,
                genre=genre,
                event_type=event_types[event_type],
                url=url_event,
                time_slots=[time_slot]
            ))
        return events

    def build_url(self, uri: str) -> str:
        return f"{self.base_url}{uri}"

    @staticmethod
    def build_uri_for_main_page(start_date: datetime, end_date: datetime, event_type: PosterEventTypes):
        start_date_str = start_date.strftime("%d-%m")
        end_date_str = end_date.strftime("%d-%m")
        url = f"/kemerovo/events/{start_date_str}_{end_date_str}/{event_type}/"
        return url


if __name__ == '__main__':
    parser = PosterParser('https://www.afisha.ru')
    current_date = datetime.datetime.now()
    finish_date = datetime.datetime.now() + datetime.timedelta(days=7)

    parsed_movies = parser.get_movies(start_date=current_date, end_date=finish_date)
    parsed_concerts = parser.get_concerts_performances(start_date=current_date, end_date=finish_date, event_type=PosterEventTypes.Concerts)
    parsed_performances = parser.get_concerts_performances(start_date=current_date, end_date=finish_date, event_type=PosterEventTypes.Performances)

    print(f"Фильмы: \n{parsed_movies}")
    print(f"Концерты: \n{parsed_concerts}")
    print(f"Спектакли: \n{parsed_performances}")
