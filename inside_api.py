from bottle import get, post, delete, request, response
from mysql_adapter import MySQLAdapter
import json

db = MySQLAdapter()


@post('/category')
def create_category():
    db_response = db.create_category(request.forms.get('name'))
    if db_response["STATUS"] == "ERROR":
        if db_response["MSG"] == "Category already exist":
            response.status = 200
        if db_response["MSG"] == "Name parameter is missing":
            response.status = 400
        if db_response["MSG"] == "Internal error":
            response.status = 500
    else:
        response.status = 201
    db_response['CATEGORIES'] = db_response.pop('DATA')
    return json.dumps(db_response)


@delete('/category/<id>')
def delete_category(id):
    db_response = db.delete_category(id)
    if db_response["MSG"] == "Category not found":
        response.status = 404
    if db_response["MSG"] == "Internal error":
        response.status = 500
    else:
        response.status = 201
    return json.dumps(db_response)


@get('/categories')
def list_categories():
    db_response = db.list_categories()
    if db_response["STATUS"] == "ERROR":
        response.status = 500
    return db_response


@post('/product')
def add_or_edit_product():
    db_response = db.add_or_edit_product(request.json)
    if db_response["STATUS"] == "ERROR":
        response.status = 500
    return db_response


@get('product/<id>')
def get_product():
    pass


@delete('product/<id>')
def delete_product(id):
    pass


@get('products')
def list_products():
    pass


@get('category/<id>/products')
def get_products_by_category():
    pass
