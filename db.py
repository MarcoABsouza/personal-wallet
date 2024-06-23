import sqlite3 as lite

# Create connection
connection = lite.connect("expense-control/database.db")
cursor = connection.cursor()

# Create tables in our Database

# Table Category
try:
    with connection:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Category (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name_category TEXT UNIQUE NOT NULL
            )
        """)
    print("Table Category created successfully.")
except lite.Error as error:
    print(f"Database error table Category: {error}")

 # Table Revenue
try:
    with connection:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Revenue (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                date_revenue DATE,
                value_revenue DECIMAL(10, 2) NOT NULL CHECK(value_revenue > 0),
                category_name TEXT NOT NULL DEFAULT 'REVENUE' CHECK(category_name = 'REVENUE')
            )
        """)
    print("Table Revenue created successfully.")
except lite.Error as error:
    print(f"Database error table Revenue: {error}")

# Table Expenses
try:
    with connection:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                date_expense DATE,
                value_expense DECIMAL(10, 2) NOT NULL CHECK(value_expense > 0),
                category_id INTEGER NOT NULL,
                CONSTRAINT fk_category_name_expense FOREIGN KEY (category_id) REFERENCES Category(id)
            )
        """)
    print("Table Expenses created successfully.")
except lite.Error as error:
    print(f"Database error table Expense: {error}")


# Create Index in tables
try:
    
    with connection:
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_category_expense ON Expenses(category_id)")
    print("Index idx_category_expense created successfully.")
except lite.Error as error:
    print(f"Database error index: {error}")

# ------ Ensuring data integrity
delete_category_cascade = """
    CREATE TRIGGER IF NOT EXISTS delete_category_cascade
    BEFORE DELETE ON Category
    FOR EACH ROW
    BEGIN   
        DELETE FROM Expenses WHERE category_id = OLD.id;
    END;
"""
try:
    with connection:
        cursor.execute(delete_category_cascade)
    print("Trigger delete_category_cascade created successfully.")
except lite.Error as error:
    print(f"Database error trigger: {error}")