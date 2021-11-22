"""Requests to a database"""
import random
import os

from typing import Dict, List

from sqlalchemy import create_engine, select, join

from mood_movie_bot.db.schema import moods_table, genres_table, movies_table, movies_genres, movies_moods


engine = create_engine(
        os.getenv('TELEGRAM_DB_URL'), echo=True,
    )


def get_mood_names() -> List[str]:
    with engine.connect() as conn:
        result = conn.execute(select(moods_table.c.name))
    return [r[0] for r in result]
    
    
def exclude_movie_id(dic) -> Dict:
    return {k: v for k, v in dic.items() if k != 'movie_id'}


def get_movie_by_mood(mood) -> str:
    with engine.connect() as conn:
        mood_table_join = moods_table.join(movies_moods, movies_moods.c.mood_id==moods_table.c.mood_id)
        genre_table_join = genres_table.join(movies_genres, movies_genres.c.genre_id==genres_table.c.genre_id)
        result = conn.execute(select(
            movies_table).\
            select_from(movies_table.join(mood_table_join, movies_moods.c.movie_id==movies_table.c.movie_id)).\
            where(moods_table.c.name==mood))
        movie_list = [r for r in result.mappings().all()]
        random_movie = random.choice(movie_list)
        random_movie_genres = conn.execute(select(
            genres_table.c.name).\
            select_from(movies_table.join(genre_table_join, movies_genres.c.movie_id==movies_table.c.movie_id)).\
            where(movies_table.c.movie_id==random_movie['movie_id']))
        random_movie_genres_list = [str(r[0]) for r in random_movie_genres]
        random_movie_genres_str = 'genres: '
        for genre in random_movie_genres_list:
            random_movie_genres_str += genre + ' '
        random_movie_info = ''
        for key, info in exclude_movie_id(random_movie).items():
            random_movie_info += f'{key}: {info}\n\n'
    return f'{random_movie_info}{random_movie_genres_str}'
