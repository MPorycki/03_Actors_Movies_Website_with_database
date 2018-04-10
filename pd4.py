from flask import Flask, request, g, jsonify, make_response
import sqlite3, datetime

pd4 = Flask(__name__)
database = 'bazadanych.db'

def get_db():
    global database
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db


@pd4.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@pd4.route('/')
def hello():
    return "Witamy w bazie danych filmow i aktorow"


@pd4.route('/cities', methods=['GET','POST'])
def handler():
    if request.method == 'GET':
        return get_cities()
    elif request.method == 'POST':
        return post_city()


def get_cities():
    db = get_db()
    c = db.cursor()
    data = []
    per_page = request.args.get('per_page')
    page = request.args.get('page')
    if per_page is None or page is None:
        for arg in request.args:
            if "country_name" in arg:
                country_name = request.args.get(arg)
                data = c.execute("select city from city c join country co on c.country_id = co.country_id "
                                 "where co.country = :country order by city collate nocase",
                                 {'country': country_name}).fetchall()
        if len(data) == 0:
            data = c.execute("select city from city order by city collate nocase asc").fetchall()
    else:
        for arg in request.args:
            if "country_name" in arg:
                country_name = request.args.get(arg)
                data = c.execute("select city from city c join country co on c.country_id = co.country_id "
                                 "where co.country = :country order by city collate nocase limit :page_limit offset :page",
                                 {'country': country_name, 'page_limit': per_page, 'page': (int(page) - 1) * int(per_page)}).fetchall()
        if len(data) == 0:
            data = c.execute("select city from city order by city collate nocase asc limit :page_limit offset :page",
                             {'page_limit': per_page, 'page': (int(page) - 1) * int(per_page)}).fetchall()
    result = []
    for item in data:
        result.append(item[0])
    json_result = jsonify(result)
    return json_result


def post_city():
    data = request.get_json()
    db = get_db()
    c = db.cursor()
    country_list = c.execute("select country_id from country").fetchall()
    city_list = c.execute("select city_id from city").fetchall()
    country_id = data.get('country_id')
    city_id = data.get('city_id')
    city_name = data.get('city_name')
    result = {}
    if (country_id,) not in country_list:
        result['error'] = 'Invalid country_id'
        response = jsonify(result)
        return make_response(response, 400)
    elif (city_id,) in city_list:
        result['error'] = 'City_id already exists'
        response = jsonify(result)
        return make_response(response,400)
    else:
        db.execute(
            'insert into city(city_id, city, country_id,last_update) values (?,?,?,?)',
            (city_id, city_name, country_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        )
        db.commit()
        result['city_id'] = city_id
        result['country_id'] = country_id
        result['city_name'] = city_name
        return jsonify(result)


@pd4.route('/lang_roles')
def get_lang():
    db = get_db()
    c = db.cursor()
    data = c.execute("select l.name, count(1)-1 from language l "
                     "left join film f on l.language_id = f.language_id "
                     "left join film_actor fa on fa.film_id = f.film_id "
                     "group by l.name").fetchall()
    json = jsonify(data)
    return json


if __name__ == '__main__':
    pd4.run(debug=True)
