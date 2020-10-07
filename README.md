# Star_War_API

# Project Background
A flask server with redis caching capabilites wrapping the swapi api which has star wars data

# Requirement

OS - Linux, MacOS, Windows 10

Software - Python 3.6+, redis, Postman

Python package - redis, Flask, Flask-Caching, requests

# Installation & Running server
```bash
$ git clone https://github.com/AdityaMunot/Star_War_API.git
$ cd Star_War_API
$ export FLASK_APP=app
$ flask run
```

# Testing API
make a POST request in postman
 ```
 ~ http://localhost:8080/films

 ~ http://localhost:8080/characters/4
 ```

## Author

Managed by [Aditya Munot](https://github.com/AdityaMunot)