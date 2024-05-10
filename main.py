import datetime
from src.adapters.parsers.poster_parser import PosterParser, PosterEventTypes


parser = PosterParser('https://www.afisha.ru')
current_date = datetime.datetime.now()
finish_date = datetime.datetime.now() + datetime.timedelta(days=7)

# parsed_movies = parser.get_movies(start_date=current_date, end_date=finish_date)
parsed_concerts = parser.get_concerts_performances(start_date=current_date, end_date=finish_date, event_type=PosterEventTypes.Concerts)
parsed_performances = parser.get_concerts_performances(start_date=current_date, end_date=finish_date, event_type=PosterEventTypes.Performances)
parsed_events = parsed_concerts + parsed_performances

# print(f"Фильмы: \n{parsed_movies}")
# print(f"Концерты: \n{parsed_concerts}")
# print(f"Спектакли: \n{parsed_performances}")
