"""create tables

Revision ID: d3446f3a3862
Revises: 
Create Date: 2021-11-09 10:03:18.998295

"""
from alembic import op
from sqlalchemy import (
    Column, ForeignKey, Integer,
    String, Text
)


# revision identifiers, used by Alembic.
revision = 'd3446f3a3862'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'moods',
        Column('mood_id', Integer, primary_key=True),
        Column('name', String, unique=True),
        Column('description', String)
    )
    op.create_table(
        'genres',
        Column('genre_id', Integer, primary_key=True),
        Column('name', String, unique=True)
    )
    op.create_table(
        'movies',
        Column('movie_id', Integer, primary_key=True),
        Column('title', String),
        Column('year', String),
        Column('length', String),
        Column('IMDb rating', String),
        Column('director', String),
        Column('description', Text),
    )
    op.create_table(
        'movies_genres',
        Column('movie_id', Integer, ForeignKey('movies.movie_id')),
        Column('genre_id', Integer, ForeignKey('genres.genre_id'))
    )
    op.create_table(
        'movies_moods',
        Column('movie_id', Integer, ForeignKey('movies.movie_id')),
        Column('mood_id', Integer, ForeignKey('moods.mood_id'))
    )


def downgrade():
    op.drop_table('moods')
    op.drop_table('genres')
    op.drop_table('movies')
    op.drop_table('movies_genres')
    op.drop_table('movies_moods')
