import sqlite3 as lite

# Create connection
connection = lite.connect("expense-control/database.db")
cursor = connection.cursor()

# Create tables in our Database

# Table Category
with connection:
    cursor.execute("CREATE TABLE if not exists Category(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name_category TEXT NOT NULL)")

# Table Revenue
with connection:
    cursor.execute("CREATE TABLE if not exists Revenue(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date_revenue DATE, value_revenue DECIMAL NOT NULL, category TEXT NOT NULL)")

# Table Expenses
with connection:
    cursor.execute("CREATE TABLE if not exists Expenses(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date_expense DATE, value_expense DECIMAL NOT NULL, category TEXT NOT NULL)")

