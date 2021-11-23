"""This script manages database transactions"""
import asyncio
import os
import time
import random
import logging

from typing import List

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select, insert

from schema import moods_table, genres_table, movies_table, movies_genres

from mood_movie_bot.db.parsers.mood_parser import get_moods
from mood_movie_bot.db.parsers.genre_parser import get_genres
from mood_movie_bot.db.parsers.movie_parser import get_movie_id, get_movie_info


logging.basicConfig(level=logging.ERROR)

engine = create_async_engine(
        os.getenv('TELEGRAM_ASYNC_DB_URL'), echo=True,
    )


async def insert_genres(connection):
    genres = get_genres()
    for genre in genres:
        await connection.execute(insert(genres_table).values(name=genre['name']))


async def insert_moods(connection):
    moods = get_moods('parsers/moods.txt')
    for mood in moods:
        await connection.execute(insert(moods_table).values(name=mood['name'], description=mood['description']))


def create_movies_id_file():
    """Reads titles of movies from file, finds their ids on IMDb and writes them to new file"""
    with open('parsers/files/movie_titles.txt', 'r', encoding='utf-8') as movie_titles_file:
        with open('parsers/files/movies_id.txt', 'w', encoding='utf-8') as movies_id_file:
            for title in movie_titles_file:
                try:
                    movie_id = get_movie_id(title)
                except Exception as e:
                    logging.error(f'Couldn\'t find id for movie {title}')
                    continue
                movies_id_file.write(str(movie_id) + '\n')


def get_movies_info_list() -> List[List]:
    """Reads ids of movies from file and gets information about them on IMDb"""
    with open('parsers/files/movies_id.txt', 'r', encoding='utf-8') as movies_id_file:
        movies_info_list = list()
        for m_id in movies_id_file:
            try:
                movies_info_list.append(get_movie_info(m_id.strip()))
                time.sleep(random.randint(1, 6))
            except Exception as e:
                logging.error(f'Couldn\'t find information for the movie with id: {m_id}')
                continue
        return movies_info_list


async def insert_movies(connection, movies_info_list):
    for movie in movies_info_list:
        movie_result = await connection.execute(movies_table.insert(), movie[0])
        genres = movie[1].get('genre_id')
        for genre in genres:
            genre_result = await connection.execute(select(genres_table.c.genre_id).where(genres_table.c.name==genre))
            await connection.execute(
                insert(movies_genres).values(movie_id=movie_result.inserted_primary_key._mapping['movie_id'],
                genre_id=genre_result.fetchone()[0]))


async def async_main():
    async with engine.begin() as conn:
        await insert_genres(conn)
        await insert_moods(conn)
        await asyncio.to_thread(create_movies_id_file)
        movies_info = await asyncio.to_thread(get_movies_info_list)
        await insert_movies(conn, movies_info)

    await engine.dispose()


asyncio.run(async_main())
