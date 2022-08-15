import json
import sqlite3
import sql as sql
import flask


def get_connect_from_db(sql):
    """
    Подключение к базе данных
    :param sql: netflix
    :return: result
    """
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()
        return result


def get_value_by_title(title):
    """
    Поиск по названию.
    :param title: Фильтр по title
    :return: Возврат одного последнего фильма
    """
    sql = f"""
          SELECT title, country, release_year, listed_in AS genre, description
          FROM netflix
          WHERE title = '{title}'
          ORDER BY release_year DESC
          LIMIT 1    
"""
    result = get_connect_from_db(sql)
    for item in result:
        return dict(item)


def get_two_actors(name1="Rose McIver", name2="Ben Lamb"):
    """
    Шаг 5: Написать функцию, которая получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз.
    :param name1: Rose McIver
    :param name2: Ben Lamb
    :return: Список
    """
    sql = f"""
                      SELECT title, "cast", country, release_year, listed_in AS genre, description
                      FROM netflix
                      WHERE "cast" LIKE '%{name1}%' and "cast" LIKE '%{name2}%'
            """
    result = get_connect_from_db(sql)

    res = []
    names_dict = {}
    for item in result:
        names = set(dict(item).get("cast").split(", ")) - set([name1, name2])

        for name in names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1

    for key, value in names_dict.items():
        if value > 2:
            res.append(key)
    return res


def step_6(typ, year, genre):
    """
    Напишите функцию, с помощью которой можно будет передавать **тип** картины (фильм или сериал),
    **год выпуска** и ее **жанр** и получать на выходе список названий картин с их описаниями в JSON.
    Сперва напишите SQL запрос, затем напишите функцию, которая принимала бы `тип, год, жанр`
    :param typ: тип
    :param year: год
    :param genre: жанр
    :return:
    """

    sql = f"""
              SELECT *
              FROM netflix
              WHERE "type" = '{typ}'
              AND release_year = '{year}'
              AND listed_in LIKE '%{genre}%'
"""

    result = get_connect_from_db(sql)

    res = []
    for item in result:
        res.append(dict(item))

    return json.dumps(res,
                            ensure_ascii=False,
                            indent=4
                            )


    #print(get_two_actors()) Тест 5 шага
    #print(step_6(typ='TV Show', year=2020, genre='Dramas')) Тест 6 шага
