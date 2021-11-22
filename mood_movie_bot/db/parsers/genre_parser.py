import requests
from bs4 import BeautifulSoup

from typing import Dict, List


def get_genres() -> List[Dict]:
    genres = list()
    response = requests.get("https://www.imdb.com/feature/genre/?ref_=nv_ch_gr")
    soup = BeautifulSoup(response.text, 'lxml')
    side_bar = soup.find_all("div", class_="aux-content-widget-2")
    top_by_grenre = side_bar[3].find_all("div", class_="table-cell primary")
    for genre in top_by_grenre:
        genres.append({"name": genre.text.strip()})
    return genres