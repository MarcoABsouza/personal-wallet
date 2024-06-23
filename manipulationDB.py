import sys
import sqlite3 as lite
import pandas as pd

# Create connection
connection = lite.connect("expense-control/database.db")

# Create cursor for executions
cursor = connection.cursor()


# -------------- Function Insert

# Insert in Category table
def insert_category(name_category):
    with connection:
        query = "INSERT INTO Category (name_category) VALUES (?)"
        cursor.execute(query, name_category)

# Insert in Revenue table
def insert_revenue(revenue_data):
    with connection:
        query = "INSERT INTO Revenue (date_revenue,value_revenue,category) VALUES (?,?,?)"
        cursor.execute(query,revenue_data)

# Insert in Expenses table
def insert_expense(expense_data):
    with connection:
        query = "INSERT INTO Expenses (date_expense, value_expense, category) VALUES (?,?,?)"
        cursor.execute(query,expense_data)


# -------------- Function Delete

# Delete in Category table
def delete_category(id_category):
    with connection:
        query = "DELETE FROM Category WHERE id=?"
        cursor.execute(query, id_category)


# Delete in Revenue table
def delete_revenue(id_revenue):
    with connection:
        query = "DELETE FROM Revenue WHERE id=?"
        cursor.execute(query, id_revenue)

# Delete in Expenses table
def delete_expense(id_expenses):
    with connection:
        query = "DELETE FROM Expenses WHERE id=?"
        cursor.execute(query, id_expenses)

# -------------- Function View

# View itens in Category table
def view_category():
    list_categories = []
    with connection:
        query = "SELECT * FROM Category"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            list_categories.append(row)
    return list_categories

# View itens in Revenue table
def view_revenue():
    list_revenue = []
    with connection:
        query = "SELECT * FROM Revenue"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            list_revenue.append(row)
    return list_revenue


# View itens in Expenses table
def view_expenses():
    list_expenses = []
    with connection:
        query = "SELECT * FROM Expenses"
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            list_expenses.append(row)
    return list_expenses


# -------------- Function Update

# Update item in Category
def update_category(category_update):
    with connection:
        query = "UPDATE Category SET name_category=? Where id=?"
        cursor.execute(query, category_update)


# Update item in Revenue
def update_revenue(revenue_update):
    with connection:
        query = "UPDATE Revenue SET date_revenue=?, value_revenue=? Where id=?"
        cursor.execute(query, revenue_update)


# Update item in Expenses
def update_expense(expense_update):
    with connection:
        query = "UPDATE Expenses SET date_expense=?, value_expense=?,category=? Where id=?"
        cursor.execute(query, expense_update)



def table():
    expenses = view_expenses()
    revenue = view_revenue()

    table_list = []

    for i in expenses:
        table_list.append(i)

    for i in revenue:
        table_list.append(i)

    return table_list

def bar_values():
    # Receita Total ------------------------
    revenue = view_revenue()
    revenue_list = []

    for i in revenue:
        revenue_list.append(i[2])

    revenue_amount = sum(revenue_list)

    # Despesas Total ------------------------
    expenses = view_expenses()
    expenses_list = []

    for i in expenses:
        expenses_list.append(i[2])

    expenses_amount = sum(expenses_list)

    # Despesas Total ------------------------
    balance = revenue_amount - expenses_amount

    return[revenue_amount,expenses_amount,balance]

def percentage_value():

    # Receita Total ------------------------
    revenue = view_revenue()
    revenue_list = []

    for i in revenue:
        revenue_list.append(i[2])

    revenue_amount = sum(revenue_list)
    
    # Despesas Total ------------------------
    expenses = view_expenses()
    expenses_list = []

    for i in expenses:
        expenses_list.append(i[2])

    expenses_amount = sum(expenses_list)

    # Despesas Total ------------------------
    try:
        amount =  ((revenue_amount - expenses_amount) / revenue_amount) * 100
    except ZeroDivisionError:
        amount = 0

    return[amount]


def pie_values():
    expenses = view_expenses()
    table_list = []

    for i in expenses:
        table_list.append(i)

    dataframe = pd.DataFrame(table_list,columns = ['id', 'Date', 'Value', 'Category'])

    # Get the sum of the durations per month
    dataframe = dataframe.groupby('Category')['Value'].sum()
   
    qtd_list = dataframe.values.tolist()
    categories_list = []

    for i in dataframe.index:
        categories_list.append(i)

    return([categories_list,qtd_list])

