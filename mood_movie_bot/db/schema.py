from sqlalchemy import (
    Column, ForeignKey, Integer,
    MetaData, String, Text, Table
)


convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),

    # Именование индексов
    'ix': 'ix__%(table_name)s__%(all_column_names)s',

    # Именование уникальных индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',

    # Именование CHECK-constraint-ов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',

    # Именование внешних ключей
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',

    # Именование первичных ключей
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


moods_table = Table(
    'moods',
    metadata,
    Column('mood_id', Integer, primary_key=True),
    Column('name', String, unique=True),
    Column('description', String)
)

genres_table = Table(
    'genres',
    metadata,
    Column('genre_id', Integer, primary_key=True),
    Column('name', String, unique=True)
)

movies_table = Table(
    'movies',
    metadata,
    Column('movie_id', Integer, primary_key=True),
    Column('title', String),
    Column('year', String),
    Column('length', String),
    Column('IMDb rating', String),
    Column('director', String),
    Column('description', Text),
)

movies_genres = Table(
    'movies_genres',
    metadata,
    Column('movie_id', ForeignKey('movies.movie_id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)

movies_moods = Table(
    'movies_moods',
    metadata,
    Column('movie_id', ForeignKey('movies.movie_id')),
    Column('mood_id', ForeignKey('moods.mood_id'))
)
