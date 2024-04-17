from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import resources

current_data = datetime.now().strftime("%d-%m")
end_data = (datetime.now() + timedelta(7)).strftime("%d-%m")
current_year = (datetime.now() + timedelta(7)).strftime("%Y")
interval_time = f"{current_data}_{end_data}"


def find_films() -> list:
    url = f"https://www.afisha.ru/kemerovo/events/{interval_time}/movies/"
    print(url)
    page = requests.get(url)

    if page.status_code != 200:
        return []

    soup = BeautifulSoup(page.text, "html.parser")
    block_films = soup.findAll("div", class_="QWR1k")
    films = []

    for film in block_films:
        name_link = film.find("a", class_="CjnHd y8A5E nbCNS yknrM")
        name = name_link.text
        link = f"https://www.afisha.ru{name_link['href']}"

        genre = film.find("div", class_="S_wwn").text.split(", ")[-1]
        date = "-".join(link.split("/")[-2].split("-")[::-1])

        films.append({
            "name": name,
            "genre": genre,
            "link": link,
            "datetime": date
        })
    return films


def find_concerts() -> list:
    url = f"https://www.afisha.ru/kemerovo/events/{interval_time}/concerts/"
    page = requests.get(url)

    if page.status_code != 200:
        return []

    soup = BeautifulSoup(page.text, "html.parser")
    block_concerts = soup.findAll("div", class_="QWR1k")
    concerts = []

    for concert in block_concerts:
        name_link = concert.find("a", class_="CjnHd y8A5E nbCNS yknrM")
        name = name_link.text
        link = f"https://www.afisha.ru{name_link['href']}"

        genre = concert.find("div", class_="S_wwn").text

        date_place = concert.find("div", class_="_JP4u").text.split(", ")
        date, place = date_place[0].split(' '), date_place[1]
        date[1] = resources.months[date[1]]
        date = f"{current_year}-{date[1]}-{date[0]} {date[3]}"

        concerts.append({
            "name": name,
            "genre": genre,
            "link": link,
            "date": date,
            "place": place
        })
    return concerts


def find_performances() -> list:
    url = f"https://www.afisha.ru/kemerovo/events/{interval_time}/performances/"
    page = requests.get(url)

    if page.status_code != 200:
        return []

    soup = BeautifulSoup(page.text, "html.parser")
    block_performances = soup.findAll("div", class_="QWR1k")
    performances = []

    for performance in block_performances:
        name_link = performance.find("a", class_="CjnHd y8A5E nbCNS yknrM")
        name = name_link.text
        link = f"https://www.afisha.ru{name_link['href']}"

        genre = performance.find("div", class_="S_wwn").text

        date_place = performance.find("div", class_="_JP4u").text.split(", ")
        date, place = date_place[0].split(' '), date_place[1]
        date[1] = resources.months[date[1]]
        date = f"{current_year}-{date[1]}-{date[0]} {date[3]}"

        performances.append({
            "name": name,
            "genre": genre,
            "link": link,
            "date": date,
            "place": place
        })
    return performances


print(find_films())
