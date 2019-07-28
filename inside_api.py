from bottle import get, post, delete, request, response
from mysql_adapter import MySQLAdapter
import json

error_response_codes = {
    "Category already exists": 200,
    "Name parameter is missing": 400,
    "Category not found": 404,
    "Product not found": 404,
    "Internal error": 500,
    "Missing parameters": 400,
}


def get_response_code(db_response, default_success_code):
    if db_response["STATUS"] == "SUCCESS":
        return default_success_code
    else:
        return error_response_codes.get(db_response["MSG"]) or 500


@post('/category')
def create_category():
    db_response = db.create_category(request.forms.get('name'))
    response.status = get_response_code(db_response, 201)
    db_response['CAT_ID'] = db_response.pop('DATA')
    return json.dumps(db_response)


@delete('/category/<id>')
def delete_category(id):
    db_response = db.delete_category(id)
    response.status = get_response_code(db_response, 201)
    return json.dumps(db_response)


@get('/categories')
def list_categories():
    db_response = db.list_categories()
    response.status = get_response_code(db_response, 200)
    db_response['CATEGORIES'] = db_response.pop('DATA')
    return db_response


@post('/product')
def add_or_edit_product():
    db_response = db.add_or_edit_product(request.forms)
    response.status = get_response_code(db_response, 201)
    return db_response


@get('/product/<id>')
def get_product(id):
    db_response = db.get_product(id)
    response.status = get_response_code(db_response, 201)
    if db_response["STATUS"] == "SUCCESS":
        db_response["PRODUCT"] = db_response.pop("DATA")
        db_response["PRODUCT"]["category"] = db_response["PRODUCT"].pop(
            "category_id")
    return json.dumps(db_response)


@delete('/product/<id>')
def delete_product(id):
    db_response = db.delete_product(id)
    response.status = get_response_code(db_response, 201)
    return json.dumps(db_response)


@get('/products')
def list_products():
    db_response = db.list_products()
    response.status = get_response_code(db_response, 200)
    if db_response["STATUS"] == "SUCCESS":
        db_response["PRODUCTS"] = db_response.pop("DATA")
        for prod in db_response["PRODUCTS"]:
            prod["category"] = prod.pop(
                "category_id")
    return json.dumps(db_response)


@get('/category/<id>/products')
def get_products_by_category(id):
    db_response = db.get_products_by_category(id)
    response.status = get_response_code(db_response, 200)
    if db_response["STATUS"] == "SUCCESS":
        db_response["PRODUCTS"] = db_response.pop("DATA")
        for prod in db_response["PRODUCTS"]:
            prod["category"] = prod.pop(
                "category_id")
    return json.dumps(db_response)

db = MySQLAdapter()
