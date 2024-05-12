from datetime import datetime, timedelta
from pathlib import Path

from src.adapters.parsers.poster_parser import PosterParser, PosterEventTypes
from src.adapters.repos.event_repo import EventRepo

current_date = datetime.now()
finish_date = datetime.now() + timedelta(days=7)

file_path = Path(__file__).parent.parent / 'data' / 'events.json'


def main() -> None:
    parser = PosterParser('https://www.afisha.ru')

    parsed_movies = parser.get_movies(start_date=current_date, end_date=finish_date)
    parsed_concerts = parser.get_concerts_performances(start_date=current_date, end_date=finish_date,
                                                       event_type=PosterEventTypes.Concerts)
    parsed_performances = parser.get_concerts_performances(start_date=current_date, end_date=finish_date,
                                                           event_type=PosterEventTypes.Performances)
    parsed_events = parsed_movies + parsed_concerts + parsed_performances

    for i, event in enumerate(parsed_events):
        event.id = i

    event_repo = EventRepo(file_path)
    event_repo.add_events(parsed_events)
    event_repo.save()


if __name__ == '__main__':
    main()
