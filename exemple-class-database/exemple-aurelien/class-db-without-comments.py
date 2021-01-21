import mysql.connector

class Database ():

    def __init__ (self, user, password, host, database):
        self.connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )

        self.cursor = self.connection.cursor()

    def select (self, table, columns):
        request = "SELECT {columns} FROM {table}".format(
            table=table,
            columns=columns
        )
        self.cursor.execute(request)

        return self.cursor.fetchall()

    def insert (self, table, element):
        values = tuple(element.values())

        request = "INSERT INTO {table} VALUES {values}".format(
            table=table,
            values=values
        )

        self.execute_and_commit(request)

    def delete (self, table, element):
        column = tuple(element.keys())
        value = tuple(element.values())

        where = self.create_dynamic_request(column, value, ' AND ')

        request = "DELETE FROM {table} WHERE {conditions}".format(
            table=table,
            conditions=where
        )

        self.execute_and_commit(request)

    def update (self, table, element, update_element):
        update_column = tuple(update_element.keys())
        column = tuple(element.keys())

        update_value = tuple(update_element.values())
        value = tuple(element.values())

        set = self.create_dynamic_request(update_column, update_value, ',')
        where = self.create_dynamic_request(column, value, ' AND ')

        request = "UPDATE {table} SET {update} WHERE {conditions}".format(
            table=table,
            update=set,
            conditions=where
        )

        self.execute_and_commit(request)

    def execute_and_commit (self, request):
        self.cursor.execute(request)
        self.connection.commit()

    def close_connection (self):
        self.cursor.close()

    def create_dynamic_request (self, column, values, separator):
        request = ''

        for c, v in zip(column, values):
            if isinstance(v, str): v = "'" + v + "'"
            request += (c + ' = ' + str(v) + separator)

        request = request[:-len(separator)]

        return request
        
d = Database(user='pythonuser', password='pythonpwd', host='localhost', database='pythondb')

'''
    EXEMPLE DE REQUÊTES
'''
#print(d.select(table='mytable', column='nom, age'))
#d.insert(table='mytable', element={'id': 0, 'nom': 'Victor', 'age': 26})
#d.delete(table='mytable', element={'nom': 'Victori', 'age': 26})
#d.update(table='mytable', element={'nom': 'Victor'}, update_element={'nom': 'Victor', 'age': 20})
