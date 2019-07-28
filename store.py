from bottle import run, template, static_file, get, post, delete, request
from sys import argv
import json
from inside_api import *


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


if __name__ == "__main__":
    run(host='0.0.0.0', port=7000, debug=True, reloader=True)
