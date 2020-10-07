from flask import Flask, jsonify
import requests
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'star_wars_server',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379',
    'CACHE_DEFAULT_TIMEOUT': '3600' 
})

STAR_API_URL = "https://swapi.dev/api/films/"
@app.route('/')
def index():
    return "<h1> This is Star War API <h1>"

def response_value(data,status,error):
    response = {
        'data': data,
        'status': status,
        'error': error
    }
    return jsonify(response)

@app.route('/films', methods=['POST'])
def films():
    data,status,error= None,None,None
    if not cache.get('films'):
        get_films()
    data = cache.get('films')
    if data == None:
        status = 404
        error = "Error: data doesn't exist"
    else:
        status = 200
    return response_value(data, status, error)

@app.route('/characters/<int:filmID>', methods=['POST'])
def characters(filmID):
    try:
        data,status,error = None,None,None
        if not cache.get(str(filmID)):
            if not cache.get('characters'):
                get_films()
            characters_value = cache.get('characters')
            if filmID in characters_value:
                get_characters(filmID, characters_value)
                data = cache.get(str(filmID))
                status = 200
            else:
                status = 404
                error = "FilmID is not valid"
        else:
            data = cache.get(str(filmID))
            status = 200
        return response_value(data, status, error)
    except Exception as err:
        return response_value(None, 404, "Error")

def get_films():
    try:
        response_films = requests.get(STAR_API_URL)
        films_values = response_films.json()
        fm_result = []
        char_result = {}
        for count in range(films_values['count']):
            fm_result.append({'id': count, 'title': films_values['results'][count]['title'], 'release_date': films_values['results'][count]['release_date']})
            char_result[count] = films_values['results'][count]['characters']
        cache.set('films', fm_result)
        cache.set('characters', char_result)
    except Exception as err:
        print(str(err))

def get_characters(filmID, char_value):
    try:
        characters_list = char_value[filmID]
        result_list = []
        count = 0
        for actor in characters_list:
            result = {}
            response_actor = requests.get(actor)
            actor_value = response_actor.json()
            result['name'] = actor_value['name']
            result['id'] = count
            count+=1
            result_list.append(result)
        cache.set(str(filmID), result_list)
    except Exception as err:
        print(str(err))

if __name__ == "__name__":
    app.run(debug=True)