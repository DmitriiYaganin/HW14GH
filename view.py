import json

import flask

from main import get_connect_from_db, get_value_by_title

app = flask.Flask(__name__)


"""
Делаем вьюшку по маршруту: /movie/<title>
"""
@app.get("/movie/<title>")
def view_title(title):
    result = get_value_by_title(title)
    return app.response_class(
        response=json.dumps(result,
                             ensure_ascii=False,
                             indent=4
                            ),
        status=200,
        mimetype="application/json"

    )


"""
Делаем вьюшку поиск по диапазону лет выпуска: /movie/year/to/year
"""
@app.get("/movie/<int:year1>/to/<int:year2>")
def qet_by_date(year1, year2):
    sql = f"""
          SELECT title, release_year
          FROM netflix
          WHERE release_year BETWEEN {year1} and {year2}
          LIMIT 100    
"""
    result = get_connect_from_db(sql)

    res = []
    for item in result:
        res.append(dict(item))

    return app.response_class(
        response=json.dumps(res,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )


"""
Делаем вьюшку поиск по рейтингу: /rating/rating
"""
@app.get("/rating/<rating>")
def get_by_rating(rating):
    my_dict = {
        "children": ("G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sql = f"""
              SELECT title, rating, description
              FROM netflix
              WHERE rating IN {my_dict.get(rating, ("G", "NC-17"))}   
    """

    result = get_connect_from_db(sql)

    res = []
    for item in result:
        res.append(dict(item))

    return app.response_class(
        response=json.dumps(res,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )


"""
Делаем вьюшку поиск по жанру: /genre/genre
"""
@app.get("/genre/<genre>")
def get_by_genre(genre):
    sql = f"""
                  SELECT title, description
                  FROM netflix
                  WHERE listed_in LIKE '%{genre}%' 
        """
    result = get_connect_from_db(sql)

    res = []
    for item in result:
        res.append(dict(item))

    return app.response_class(
        response=json.dumps(res,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )


if __name__ == '__main__':
    app.run(debug=True)