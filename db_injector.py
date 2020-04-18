import os

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, MetaData, Table
from bottle import HTTPError

path = "sqlite:///music.sqlite3"
Base = declarative_base()


class InvalidAlbum(HTTPError):
    pass


class BadRequest(InvalidAlbum):
    """ошибка 400"""
    pass


class Conflict(InvalidAlbum):
    """ошибка 409"""
    pass


class NotFound(InvalidAlbum):
    """ошибка 404"""
    pass


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


def valid_artist(albums_list):
    """
    Функция, в случае если список пуст
    поднимет пользовательскую ошибку NotFound
    """
    if not albums_list:
        raise NotFound()
    # если совпадения были, мы возвращаем True
    return True


def valid_album(album):
    """
    Функция выводит  True для try из модуля "server.py" и перехватывает ошибки 400 и 409 в случае необходимости
    """
    if album.year != None:
        # если year состоит из цифра а длинна строки не привышает 4-х символов
        if not album.year.isdigit() or len(album.year) > 4 or len(album.year) < 1:
            raise BadRequest(400, "Введите год цифрами, в формате - 2009")

    # условие выполняется если обект name пришел в виде None из-за отсутствия совпадений по введенному альбому
    name = db.query(Albums).filter(Albums.album == album.album).first()

    # вызываем ошибку Conflict если name не None
    if name:
        raise Conflict(409, "Альбом с таким именем уже существует")

    return True


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
