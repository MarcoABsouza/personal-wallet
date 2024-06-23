# Expense Management System

## Description

This project implements an Expense Management System in Python, using SQLite for data management and Tkinter to create an intuitive graphical interface. The system allows users to add, view, update and delete expenses and income, as well as organize and analyze expenses in different categories.

## Features

*   Database:

        Use of SQLite to create and manage the local database.

        Table structure for expenses, income and categories.

        Implementation of CRUD operations (Create, Read, Update, Delete) to manage income and expenses.

        Efficient integration with SQLite, using connections and cursors for queries and updates.

        Transaction management to ensure data consistency.

        Trigger to upkeep referential integrity between tables when deleting a category.

*   Graphical Interface:
        User-friendly and intuitive interface developed with Tkinter.

        Input fields for adding and editing income and expense data.

        Buttons for performing CRUD operations and generating reports.

        Combobox for selecting categories when adding or editing expenses.

*   Available Operations:

        Add Recipe: Adds a new recipe to the system by filling in the required fields.

        Add Expense: Adds a new expense to the system, including selecting a category.

        View Recipes and Expenses: Lists all recipes and expenses, along with their respective information.

        Update Recipe: Edits the information for a selected recipe, updating the fields as necessary.

        Update Expense: Edits the information of a selected expense, updating the fields as necessary.

        Delete Revenue or Expense: Removes a specific income or expense from the system after user confirmation.

        Delete Category: Removes a specific category from the system, ensuring that related expenses are also removed.

        Generate Reports: Generates visual reports of expenses by category and total revenues.

## Database Structure

* The database has three main tables:

        Category:

                id: (INTEGER, auto-incrementing primary key)
                name_category: (TEXT, category name, unique)

        Revenue:

                id: (INTEGER, auto-incrementing primary key)
                date_revenue: (DATE, date of revenue)
                value_revenue: (DECIMAL, revenue value)
                category_name: (TEXT, default category 'REVENUE')

        Expenses:

                id: (INTEGER, auto-increment primary key)
                date_expense: (DATE, date of expense)
                value_expense: (DECIMAL, value of expense)
                category_id: (INTEGER, foreign key referencing Category)
        
        

## Running the Inventory Management System

* Installation:

        Clone or Download the Project
        Install Required Libraries

* Runing the Program 

        Create the Database:

            python3 db.py

        Run the main program:

            python3 main.py