# Импортируем модуль работы с нашей базой
import db_injector

from bottle import run
from bottle import request
from bottle import route
from bottle import HTTPError

# обрабатываем путь и атрибут
@route('/albums/<artist>')
def albums(artist):
    """
    Ищем исполнителя по атрибуту и считаем количество его альбомов.
    после чего выводим количество и список альбомов в браузер
    """
    albums_list = db_injector.find(artist.title())
    if not albums_list:
        message = "Альбомов от исполнителя {} не найдено".format(artist.upper())
        result = HTTPError(404, message)
    else:

        albums_names = [album.album for album in albums_list]
        result = "Количество найденныйх альбомов {}: {} <br><br>".format(artist.upper(), len(albums_list))
        result += "<br>".join(albums_names)

    return result

# обрабатываем POST запрос
@route('/albums', method="POST")
def add_album():
    """
    Добавляем альбом в базу
    """
    album = db_injector.Albums(
        year=request.forms.get("year"),
        artist=request.forms.get("artist").title(),
        genre=request.forms.get("genre").title(),
        album=request.forms.get("album").title()
    )

    # создаём объект с первым попавшимся совпадением по альбомам! Если совпадений нет
    # объект возращается ввиде None
    name = db_injector.db.query(db_injector.Albums).filter(db_injector.Albums.album == album.album).first()

    # если year состоит из цифра а длинна строки не привышает 4-х символов
    if not album.year.isdigit() or len(album.year) > 4:
        result = HTTPError(415, "Введите год цифрами, в формате - 2009")

    # условие выполняется если обект name пришел в виде None
    elif not name:
        db_injector.commit(album)
        result = "Был добавлен новый альбом \nГод - {}\nИсполнитель - {} \nЖанр - {} \nАльбом - {}".format(album.year,
                                                                                                           album.artist,
                                                                                                           album.genre,
                                                                                                           album.album)
    else:
        message = "Альбом с таким именем уже существует"
        result = HTTPError(409, message)

    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)
