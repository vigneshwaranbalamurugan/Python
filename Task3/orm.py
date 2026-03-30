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
        super().__init__(name,"INTEGER")
        self.ref_table=ref_table
        self.ref_column=ref_column
    
class Model:
    @classmethod
    def create_table(cls):
        columns = []
        foreign_keys = []
        for key, field in cls.__dict__.items():
            if isinstance(field, Field):
                column_def = f"{field.name} {field.datatype}"
                if field.primary:
                    column_def += " PRIMARY KEY"
                if field.unique:
                    column_def += " UNIQUE"
                columns.append(column_def)
                if isinstance(field,ForeignKeyField):
                    foreign_keys.append(f"FOREIGN KEY({field.name}) REFERENCES {field.ref_table}({field.ref_column})")

        query = f"""
        CREATE TABLE IF NOT EXISTS {cls.__name__.lower()}
        ({', '.join(columns+foreign_keys)})
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

        rows = cursor.fetchall()
        objects = []

        for row in rows:
            obj = cls(*row)
            objects.append(obj)

        return objects

    @classmethod
    def find(cls, column, value):
        query = f"SELECT * FROM {cls.__name__.lower()} WHERE {column}=?"
        cursor.execute(query, (value,))

        rows = cursor.fetchall()
        return [cls(*row) for row in rows]

    @classmethod
    def findwithdept(cls,column,value):
        query=f"SELECT * FROM {cls.__name__.lower()} JOIN department ON {cls.__name__.lower()}.dept_id=department.id WHERE {column}=?"
        cursor.execute(query,(value,))
        return cursor.fetchall()
    
    @classmethod
    def delete(cls,column,value):
        query=f"DELETE FROM {cls.__name__.lower()} WHERE {column}=?"
        cursor.execute(query,(value,))
        conn.commit()

    @classmethod
    def order_by(cls, column, descending=False):
        direction = "DESC" if descending else "ASC"
        cursor.execute(
            f"SELECT * FROM {cls.__name__.lower()} ORDER BY {column} {direction}"
        )
        return cursor.fetchall()
        
    def __getattr__(self, name):
        for key, field in self.__class__.__dict__.items():
            if isinstance(field, ForeignKeyField):
                ref_table = field.ref_table.capitalize()
                if name == ref_table.lower():
                    ref_model = globals()[ref_table]
                    fk_value = getattr(self, key)
                    result = ref_model.find(field.ref_column, fk_value)
                    return result[0] if result else None

        raise AttributeError(name)

class User(Model):
    id = IntegerField("id",True,True)
    name = StringField("name",False,True)
    age = IntegerField("age")
    dept_id = ForeignKeyField("dept_id", "department","id")

    def __init__(self, id, name, age,dept_id):
        self.id = id
        self.name = name
        self.age = age
        self.dept_id=dept_id

class Department(Model):
    id=IntegerField("id",True,True)
    name = StringField("name",False,True)

    def __init__(self,id,name):
        self.id=id
        self.name=name

Department.create_table()
User.create_table()

# dept=Department(2,"IT")
# dept.save()

# user1 = User(6, "Vigneshwaran  B", 15,2)
# user1.save()

print(User.all())
print(Department.all())
print(User.find("name", "Vigneshwaran"))

print(User.findwithdept("user.name","Vigneshwaran"))

# User.delete("id",3)
# Department.delete("id",2)
print(User.all())
print(User.order_by("age",False))

u = User.find("id", 6)[0]
print(u.name)
print(u.department.name)