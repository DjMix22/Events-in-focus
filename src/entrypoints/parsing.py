from src.adapters.repos.event_repo import EventRepo
from datetime import datetime, timedelta
from pathlib import Path
from src.adapters.parsers.poster_parser import PosterParser, PosterEventTypes


current_date = datetime.now()
finish_date = datetime.now() + timedelta(days=7)

file_path = Path(__file__).parent.parent.parent / 'data' / 'events.json'


def main():
    parser = PosterParser('https://www.afisha.ru')

    parsed_movies = parser.get_movies(start_date=current_date, end_date=finish_date)
    parsed_concerts = parser.get_concerts_performances(start_date=current_date, end_date=finish_date,
                                                       event_type=PosterEventTypes.Concerts)
    parsed_performances = parser.get_concerts_performances(start_date=current_date, end_date=finish_date,
                                                           event_type=PosterEventTypes.Performances)
    parsed_events = parsed_movies + parsed_concerts + parsed_performances

    event_repo = EventRepo(file_path)
    event_repo.add_events(parsed_events)
    event_repo.save()


if __name__ == '__main__':
    main()
