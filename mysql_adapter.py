import pymysql


""" Commands used to create this Database on MYSQL server:
CREATE DATABASE store;
USE store;
CREATE TABLE categories (
id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
name VARCHAR(30)  UNIQUE NOT NULL
);
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    title VARCHAR(30) UNIQUE NOT NULL,
    description VARCHAR(100),
    price FLOAT NOT NULL,
    img_url VARCHAR(150),
    category_id INT,
    FOREIGN KEY (category_id)
        REFERENCES categories (id),
    favorite BOOLEAN
);"""


class MySQLAdapter:
    def __init__(self, *args, **kwargs):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='root',
                                          db='imdb',
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          )
        try:
            with self.connection.cursor() as c:
                c.execute('USE store')
        except:
            print('could not use database store. does it even exist?')

    def return_object(self, status, msg, data):
        return {
            "STATUS": status,
            "MSG": msg,
            "DATA": data
        }

    def create_category(self, name):
        if name == "":
            return self.return_object("ERROR", "Name parameter is missing", None)
        # try:
        with self.connection.cursor() as c:
            if(c.execute(f'SELECT * FROM categories WHERE name = "{name}"') != 0):
                return self.return_object("ERROR", "Category already exists", None)
            c.execute(f'INSERT INTO categories VALUES (null, "{name}")')
            self.connection.commit()
            return self.return_object("SUCCESS", None, c.lastrowid)
        # except:
        #     return self.return_object("ERROR", "Internal error", None)

    def delete_category(self, id):
        try:
            with self.connection.cursor() as c:
                c.execute(f'DELETE FROM categories WHERE id = {id}')
                return self.return_object("SUCCESS", None, None)
        except:
            return self.return_object("ERROR", "Internal error", None)

    def list_categories(self):
        try:
            with self.connection.cursor() as c:
                c.execute('SELECT * FROM categories;')
                return self.return_object("SUCCESS", None, c.fetchall())
        except:
            return self.return_object("ERROR", "Internal error", None)

    def add_or_edit_product(self, product_Data):
        if product_Data["title"] == "":
            return self.return_object("ERROR", "Missing parameters", None)
        if product_Data["category"] == "":
            return self.return_object("ERROR", "Category not found", None)
        else:
            # try:
            with self.connection.cursor() as c:
                if(product_Data["id"] != ""):
                    c.execute('DELETE FROM products WHERE id = %s;', product_Data["id"] )
                creation_query = """
                INSERT INTO `products`
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                product_Data["favorite"] = 1 if (
                    "favorite" in product_Data.keys()) == "on" else 0
                c.execute(creation_query, (None, product_Data["title"], product_Data["desc"], product_Data["price"],
                                           product_Data["img_url"], product_Data["category"], product_Data["favorite"]))
                self.connection.commit()
                return self.return_object("SUCCESS", None, c.lastrowid)
            # except:
            #     return self.return_object("ERROR", "Internal error", None)

    def get_product(self, id):
        # try
        with self.connection.cursor() as c:
            c.execute('SELECT * FROM products WHERE id = %s', id)
            product = c.fetchone()
            if(product is None):
                return self.return_object("ERROR", "Product not found", None)
            return self.return_object("SUCCESS", None, product)
     # except:
            #     return self.return_object("ERROR", "Internal error", None)

    def delete_product(self, id):
        try:
            with self.connection.cursor() as c:
                c.execute('DELETE FROM products WHERE id = %s', id)
                return self.return_object("SUCCESS", None, None)
        except:
            return self.return_object("ERROR", "Internal error", None)

    def list_products(self):
        with self.connection.cursor() as c:
            c.execute('SELECT * FROM products')
            product = c.fetchall()
            return self.return_object("SUCCESS", None, product)

    def get_products_by_category(self, id):
        with self.connection.cursor() as c:
            c.execute('SELECT * FROM products WHERE category_id = %s', id)
            product = c.fetchall()
            return self.return_object("SUCCESS", None, product)
