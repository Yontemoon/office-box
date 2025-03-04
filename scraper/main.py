import requests
from bs4 import BeautifulSoup
from utils import stringToInt
import json
from datetime import date, timedelta
from utils import uuidToString
from server import supabase

def get_daily_bo(date: str):
    url = f"https://www.boxofficemojo.com/date/{date}/?ref_=bo_da_nav"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    movie_tables = soup.find("div", class_="a-section imdb-scroll-table-inner")
    tables = movie_tables.find("table")

    movie_rows = tables.find_all("tr")
    rows_without_header = movie_rows[1:]

    for movie in rows_without_header:
        table_data = movie.find_all("td")
        title = table_data[2].text
        uuidId = uuidToString(title)
        daily_bo = stringToInt(table_data[3].text)
        theaters = stringToInt(table_data[6].text)
        to_date_bo = stringToInt(table_data[8].text)
        days_in_theaters = stringToInt(table_data[9].text)

        daily_bo_data = {
            "movie_id": uuidId,
            "title": title,
            "daily_bo": daily_bo,
            "theaters": theaters,
            "to_date": to_date_bo,
            "days_in_theaters": days_in_theaters
        }
        movies.append(daily_bo_data)
    print("Movies scrapped")
    return movies

def main():
    today = date.today()

    for index in range(10, 0, -1):
        current_date = today - timedelta(days=index)
        print("current date", current_date)
        movieInfo = get_daily_bo(current_date)

        with open(f"data/{current_date}.json", "w") as f:
            json.dump(movieInfo, f, indent=2)
            print("Generated JSON file for", current_date)

    print("Successfully added data!")



if __name__ == "__main__":
    main()