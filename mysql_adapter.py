import pymysql

# """ Commands used to create this Database on MYSQL server are on 'store.sql'


class MySQLAdapter:
    def __init__(self, *args, **kwargs):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='root',
                                          db='store',
                                          charset='utf8',
                                          cursorclass=pymysql.cursors.DictCursor,
                                          )

    def return_object(self, status, msg, data):
        return {
            "STATUS": status,
            "MSG": msg,
            "DATA": data
        }

    def create_category(self, name):
        if name == "":
            return self.return_object("ERROR", "Name parameter is missing", None)
        try:
            with self.connection.cursor() as c:
                if(c.execute(f'SELECT * FROM categories WHERE name = "{name}"') != 0):
                    return self.return_object("ERROR", "Category already exists", None)
                c.execute(f'INSERT INTO categories VALUES (null, "{name}")')
                self.connection.commit()
                return self.return_object("SUCCESS", None, c.lastrowid)
        except:
            return self.return_object("ERROR", "Internal error", None)

    def delete_category(self, id):
        try:
            with self.connection.cursor() as c:
                c.execute('DELETE FROM categories WHERE id = %s', (id))
                if c.rowcount == 0:
                    return self.return_object("ERROR", "Category not found", None)
                self.connection.commit()
                return self.return_object("SUCCESS", None, None)
        except:
            return self.return_object("ERROR", "Internal error", None)

    def list_categories(self):
        try:
            with self.connection.cursor() as c:
                c.execute('SELECT * FROM categories')
                return self.return_object("SUCCESS", None, c.fetchall())
        except:
            return self.return_object("ERROR", "Internal error", None)

    def add_or_edit_product(self, product_Data):
        if '' in[product_Data["title"],product_Data["price"]]:
            return self.return_object("ERROR", "Missing parameters", None)
        if "category" not in product_Data.keys():
            return self.return_object("ERROR", "Category not found", None)
        else:
            try:
                with self.connection.cursor() as c:
                    if(product_Data["id"] != ""):
                        c.execute('DELETE FROM products WHERE id = %s',
                                    product_Data["id"])
                    creation_query = """
                    INSERT INTO `products`
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    product_Data["favorite"] = 1 if "favorite" in product_Data.keys(
                    ) else 0
                    c.execute(creation_query, (None, product_Data["title"], product_Data["desc"], product_Data["price"],
                                                product_Data["img_url"], product_Data["category"], product_Data["favorite"]))
                    self.connection.commit()
                    return self.return_object("SUCCESS", None, c.lastrowid)
            except:
                return self.return_object("ERROR", "Internal error", None)

    def get_product(self, id):
        try:
            with self.connection.cursor() as c:
                c.execute('SELECT * FROM products WHERE id = %s', id)
                product = c.fetchone()
                if(product is None):
                    return self.return_object("ERROR", "Product not found", None)
                return self.return_object("SUCCESS", None, product)
        except:
                    return self.return_object("ERROR", "Internal error", None)

    def delete_product(self, id):
        try:
            with self.connection.cursor() as c:
                c.execute('DELETE FROM products WHERE id = %s', id)
                self.connection.commit()
                if c.rowcount == 0:
                    return self.return_object("ERROR", "Product not found", None)
                self.connection.commit()
                return self.return_object("SUCCESS", None, None)
        except:
            return self.return_object("ERROR", "Internal error", None)

    def list_products(self):
        try:
            with self.connection.cursor() as c:
                c.execute('SELECT * FROM products ORDER BY favorite DESC')
                products = c.fetchall()
                return self.return_object("SUCCESS", None, products)
        except:
            return self.return_object("ERROR", "Internal error", None)

    def get_products_by_category(self, id):
        with self.connection.cursor() as c:
            c.execute('SELECT * FROM products WHERE category_id = %s', id)
            product = c.fetchall()
            return self.return_object("SUCCESS", None, product)
