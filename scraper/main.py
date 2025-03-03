import requests
from bs4 import BeautifulSoup
from utils import stringToInt
import json
from datetime import date
from utils import uuidToString



def get_daily_bo(date):
    url = f"https://www.boxofficemojo.com/date/{date}/?ref_=bo_di_table_1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = []

    movie_elements = soup.find_all("tr", class_="mojo-annotation-isEstimated")

    for movie in movie_elements:
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
    print("Todays date:", today)
    movies = get_daily_bo(today)

    #Save in file
    with open("2025-03-02.json", "w") as f:
        json.dump(movies, f, indent=2)
    print("Successfully added data!")

if __name__ == "__main__":
    main()