import sqlite3
conn = sqlite3.connect("orm.db")
cursor = conn.cursor()

class Field:
    def __init__(self, name, datatype,primary=False,unique=False):
        self.name = name
        self.datatype = datatype
        self.primary=primary
        self.unique=unique

class IntegerField(Field):
    def __init__(self, name,primary=False,unique=False):
        super().__init__(name, "INTEGER",primary,unique)

class StringField(Field):
    def __init__(self, name,primary=False,unique=False):
        super().__init__(name, "TEXT",primary,unique)

class ForeignKeyField(Field):
    def __init__(self,name,ref_table,ref_column):
        super.__init__(name,"Integer")
        self.ref_table=ref_table
        self.ref_column=ref_column

class Model:
    @classmethod
    def create_table(cls):

        columns = []
        for key, field in cls.__dict__.items():
            if isinstance(field, Field):
                column_def = f"{field.name} {field.datatype}"
                if field.primary:
                    column_def += " PRIMARY KEY"
                if field.unique:
                    column_def += " UNIQUE"
                columns.append(column_def)

        query = f"""
        CREATE TABLE IF NOT EXISTS {cls.__name__.lower()}
        ({', '.join(columns)})
        """

        cursor.execute(query)
        conn.commit()


    def save(self):
        columns = []
        values = []

        for key, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                columns.append(field.name)
                value = getattr(self, key)
                if isinstance(value, str):
                    value = f"'{value}'"
                values.append(str(value))


        query = f"""
        INSERT INTO {self.__class__.__name__.lower()}
        ({', '.join(columns)})
        VALUES ({', '.join(values)})
        """

        cursor.execute(query)
        conn.commit()


    @classmethod
    def all(cls):
        query = f"SELECT * FROM {cls.__name__.lower()}"
        cursor.execute(query)
        return cursor.fetchall()

    @classmethod
    def find(cls, column, value):
        query = f"SELECT * FROM {cls.__name__.lower()} WHERE {column}=?"
        cursor.execute(query, (value,))
        return cursor.fetchall()


class User(Model):
    id = IntegerField("id",True,True)
    name = StringField("name",False,True)
    age = IntegerField("age")


    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age


User.create_table()

user1 = User(3, "Vijay Bharath", 22)
user1.save()

print(User.all())

print(User.find("name", "Vigneshwaran"))