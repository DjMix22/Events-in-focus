from datetime import datetime, timedelta
from enum import StrEnum
from bs4 import BeautifulSoup
import dateparser

from adapters.utils import get_page
from domain.event import Event, TimeSlot, EventTypes


class AfishaEventsTypes(StrEnum):
    Films = 'movies'
    Concerts = 'concerts'
    Performances = 'performances'


class AfishaParser:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def get_films(self, start_date: datetime, end_date: datetime) -> list[Event]:
        uri = self.build_uri_for_main_page(start_date=start_date, end_date=end_date, event_type=AfishaEventsTypes.Films)
        url = self.build_url(uri)
        page = get_page(url)

        page_parser = BeautifulSoup(page, "html.parser")

        block_films = page_parser.find("div", class_="S52Wl")
        films = []

        for film in block_films:
            name_link = film.findAll("a", class_="CjnHd y8A5E nbCNS yknrM")

            if name_link:
                name = name_link[0].text
                url_film = f"https://www.afisha.ru{name_link[0]['href']}"

                genre = film.findAll("div", class_="S_wwn")[0].text.split(", ")[-1]
                date = "-".join(url_film.split("/")[-2].split("-")[::-1])

                time_slots = self.get_times_time_slots_for_films(url=url_film, date=date)
                films.append(Event(
                    name=name,
                    genre=genre,
                    event_type=EventTypes.Film.Film,
                    link=url_film,
                    time_slots=time_slots
                ))

        return films

    @staticmethod
    def get_times_time_slots_for_films(url: str, date: str) -> list[TimeSlot]:
        page = get_page(url)
        page_parser = BeautifulSoup(page, "html.parser")

        block_time_slots = page_parser.find("div", class_="S52Wl")

        if block_time_slots is None:
            return []

        time_slots = []
        for time_slot in block_time_slots:
            place_time_slot = time_slot.findAll("a", class_="CjnHd y8A5E MnbCM")

            if not place_time_slot:
                return []

            place_time_slot = place_time_slot[0].text
            block_time_slots = time_slot.findAll("div", class_="bOvGC k15XR")[0]
            price_time_slots = block_time_slots.findAll("div", class_="KS9_D")

            for elem in price_time_slots:
                price = elem.find("div", class_="ImmXK").text.split()
                start_date = f'{date} {elem.find("div", class_="WVR9s").text}:00'
                formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

                if len(price) < 2 or not (price[1].isdigit()):
                    return []

                formatted_price = float(price[1])

                time_slots.append(TimeSlot(
                    start_date=formatted_start_date,
                    price=formatted_price,
                    place=place_time_slot
                ))

        return time_slots

    def get_concerts(self, start_date: datetime, end_date: datetime):
        uri = self.build_uri_for_main_page(start_date=start_date, end_date=end_date, event_type=AfishaEventsTypes.Concerts)
        url = self.build_url(uri)
        page = get_page(url)

        page_parser = BeautifulSoup(page, "html.parser")
        block_concerts = page_parser.findAll("div", class_="oP17O")
        concerts = []

        for concert in block_concerts:
            name_link = concert.find("a", class_="CjnHd y8A5E nbCNS yknrM")
            name = name_link.text
            link = f"https://www.afisha.ru{name_link['href']}"
            price = concert.find("a", class_="CjnHd y8A5E L_ilg tCbLK faVCW")

            genre = concert.find("div", class_="S_wwn")
            if genre is None:
                genre = ''
            else:
                genre = genre.text

            if price is None:
                
        return concerts

    def build_url(self, uri: str) -> str:
        return f"{self.base_url}{uri}"

    @staticmethod
    def build_uri_for_main_page(start_date: datetime, end_date: datetime, event_type: AfishaEventsTypes):
        start_date_str = start_date.strftime("%d-%m")
        end_date_str = end_date.strftime("%d-%m")
        url = f"/kemerovo/events/{start_date_str}_{end_date_str}/{event_type}/"
        return url


if __name__ == '__main__':
    parser = AfishaParser('https://www.afisha.ru')
    current_date = datetime.now()
    end_date = datetime.now() + timedelta(days=7)
    films = parser.get_films(start_date=current_date, end_date=end_date)
    print(films)
