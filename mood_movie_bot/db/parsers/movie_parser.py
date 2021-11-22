import requests
from imdb import IMDb
from bs4 import BeautifulSoup

from typing import Dict, List


def get_movie_id(title) -> str:
    ia = IMDb()
    movie = ia.search_movie(title)
    movie_id = movie[0].movieID
    return movie_id


def get_movie_info(movie_id) -> List[Dict]:
    response = requests.get(f'https://www.imdb.com/title/tt{movie_id}/')
    soup = BeautifulSoup(response.text, 'lxml')
    title_meta_data = soup.find("ul", class_="ipc-inline-list ipc-inline-list--show-dividers TitleBlockMetaData__MetaDataList-sc-12ein40-0 dxizHm baseAlt")
    rating_data = soup.find("div", class_="AggregateRatingButton__Rating-sc-1ll29m0-2 bmbYRW")
    try:
        title = soup.find("div", class_="OriginalTitle__OriginalTitleText-jz9bzr-0 llYePj").text
    except:
        title = soup.find("h1", class_="TitleHeader__TitleText-sc-1wu6n3d-0 dxSWFG").text
    year = title_meta_data.find_all("a")[0].text
    length = title_meta_data.find_all("li")[2].text
    rating = rating_data.find("span", class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV").text
    try:
        hero_meta_data = soup.find("div", class_="Hero__MetaContainer__Video-kvkd64-4 kNqsIK")
        hero_meta_data_genres = hero_meta_data.find("div", class_="ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL")
        hero_meta_data_director = hero_meta_data.find_all("li")[0]
        genre = list()
        for i in hero_meta_data_genres.find_all("span"):
            genre.append(i.text)
        director = hero_meta_data_director.find("li", class_="ipc-inline-list__item").text
        description = hero_meta_data.find("span", class_="GenresAndPlot__TextContainerBreakpointXL-cum89p-2 gCtawA").text
    except:
        hero_meta_data = soup.find("div", class_="Hero__MetaContainer__NoVideo-kvkd64-8 TqBgz")
        hero_meta_data_genres = hero_meta_data.find("div", class_="ipc-chip-list GenresAndPlot__OffsetChipList-cum89p-5 dMcpOf")
        hero_meta_data_director = hero_meta_data.find_all("li")[0]
        genre = list()
        for i in hero_meta_data_genres.find_all("span"):
            genre.append(i.text)
        director = hero_meta_data_director.find("li", class_="ipc-inline-list__item").text
        description = hero_meta_data.find("span", class_="GenresAndPlot__TextContainerBreakpointL-cum89p-1 gwuUFD").text

    data = [{
        "title": title,
        "year": year,
        "length": length,
        "IMDb rating": rating,
        "director": director,
        "description": description,
    },
    {
        "genre_id": genre
    }]

    return data
