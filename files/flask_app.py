from flask import Flask
import redis

app = Flask(__name__)


@app.route("/")
def hello_world():
    r = redis.Redis()
    r.incr("hello")
    return "Hello, World!"


@app.route("/count")
def count_hello():
    r = redis.Redis()
    return r.get("hello")
