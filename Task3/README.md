# Custom ORM (Object-Relational Mapper)
# Description
Design a lightweight ORM from scratch using Python
metaclasses and descriptors. Support model definition, field validation, query
building, relationships, and lazy loading.
# Prerequisites:
- Python metaclasses ( __new__ , __init_subclass__ )
- Descriptor protocol ( __get__ , __set__ , __set_name__ )
- Decorators and class decorators
- SQL syntax (DDL + DML)
- sqlite3
- standard library module
- Method chaining pattern

# Use-Case:
- Define database tables as Python classes with typed fields
- Auto-generate CREATE TABLE SQL from class definitions
- CRUD operations via .save() , .delete() , .filter()
- Support ForeignKey relationships with lazy-loaded access
- Chain queries: User.filter(age__gte=25).order_by("-name").all()