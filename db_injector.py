import os

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, MetaData, Table

path = "sqlite:///music.sqlite3"
Base = declarative_base()


def create_db(path):
    """
    Функция которая создаёт файл базы "music" если он
    отсутствует в корневой деректории
    """
    metadata = sql.MetaData()
    artist_table = Table("albums", metadata,
                         sql.Column("id", Integer, primary_key=True),
                         sql.Column("year", Integer),
                         sql.Column("artist", String),
                         sql.Column("genre", String),
                         sql.Column("album", String),
                         )

    metadata.create_all(sql.create_engine(path))




def con_db(path):
    engine = sql.create_engine(path)
    sessions = sessionmaker(engine)
    session = sessions()
    return session


class Albums(Base):
    """
    Класс описывает базу данных  Albums
    """
    __tablename__ = "albums"
    id = sql.Column(sql.INTEGER, primary_key=True)

    year = sql.Column(sql.INTEGER)
    artist = sql.Column(sql.TEXT)
    genre = sql.Column(sql.TEXT)
    album = sql.Column(sql.TEXT)


def find(name):
    """
    функция для поиска в базе
    """
    artists = db.query(Albums).filter(Albums.artist == name).all()
    return artists


def commit(album):
    """
    функция добавляет новый альбом в базу
    """
    db.add(album)
    db.commit()
    b = db.query(Albums).all()
    for i in b:
        print(i.year, i.artist, i.genre, i.album)


db = con_db(path)

if not os.path.exists(path):
    create_db(path)