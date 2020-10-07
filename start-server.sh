#! /bin/sh
nohup redis-server &
flask run --host=0.0.0.0 --port=8080
