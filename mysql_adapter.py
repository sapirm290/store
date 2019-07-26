import pymysql


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
        try:
            with self.connection.cursor() as c:
                if(c.execute(f'SELECT * FROM categories WHERE name = "{name}"') != 0):
                    return self.return_object("ERROR", "Category already exists", None)
                c.execute(f'INSERT INTO categories VALUES (null, "{name}")')
                return self.return_object("SUCCESS", None, c.lastrowid)
        except:
            return self.return_object("ERROR", "Internal error", None)

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

    def add_or_edit_product():
        pass

    def get_product():
        pass

    def delete_product(id):
        pass

    def list_products():
        pass

    def get_products_by_category():
        pass
