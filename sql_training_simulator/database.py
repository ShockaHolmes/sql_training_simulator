from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path("data/sql_quest.db")

SCHEMA_SQL = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS enrollments;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    city TEXT,
    state TEXT,
    signup_date TEXT,
    loyalty_points INTEGER DEFAULT 0
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    discount REAL DEFAULT 0,
    FOREIGN KEY(order_id) REFERENCES orders(order_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    location TEXT
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department_id INTEGER,
    role TEXT,
    salary INTEGER,
    hire_date TEXT,
    manager_id INTEGER,
    FOREIGN KEY(department_id) REFERENCES departments(department_id),
    FOREIGN KEY(manager_id) REFERENCES employees(employee_id)
);

CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    department_id INTEGER,
    budget INTEGER,
    start_date TEXT,
    end_date TEXT,
    FOREIGN KEY(department_id) REFERENCES departments(department_id)
);

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    issue_type TEXT,
    priority TEXT,
    opened_date TEXT,
    closed_date TEXT,
    status TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    grade_level INTEGER,
    city TEXT
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT,
    subject TEXT,
    difficulty TEXT
);

CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    course_id INTEGER,
    score INTEGER,
    completed INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);
"""

SEED_SQL = """
INSERT INTO customers VALUES
(1,'Ava','Johnson','Wilmington','DE','2025-01-10',120),
(2,'Noah','Smith','Dover','DE','2025-02-14',75),
(3,'Mia','Brown','Bear','DE','2025-03-01',200),
(4,'Liam','Davis','Philadelphia','PA','2025-03-20',40),
(5,'Zoe','Wilson','Camden','NJ','2025-04-05',160),
(6,'Ethan','Moore','Newark','DE','2025-04-10',95),
(7,'Nia','Taylor','Bear','DE','2025-04-18',250),
(8,'Kai','Anderson','Dover','DE','2025-05-02',15);

INSERT INTO products VALUES
(1,'Python Workbook','Books',24.99,50),
(2,'SQL Flashcards','Books',14.99,100),
(3,'Coding Robot','STEM Kits',79.99,25),
(4,'Micro Drone','STEM Kits',129.99,10),
(5,'Notebook','Supplies',4.99,200),
(6,'Marker Set','Supplies',8.99,120),
(7,'Raspberry Pi Kit','STEM Kits',99.99,18),
(8,'Data Science Poster','Decor',12.99,40);

INSERT INTO orders VALUES
(1,1,'2025-05-01','shipped'),
(2,2,'2025-05-03','pending'),
(3,3,'2025-05-05','shipped'),
(4,1,'2025-05-07','cancelled'),
(5,5,'2025-05-09','shipped'),
(6,7,'2025-05-11','pending'),
(7,6,'2025-05-12','shipped'),
(8,3,'2025-05-13','shipped'),
(9,8,'2025-05-15','pending');

INSERT INTO order_items VALUES
(1,1,1,2,0),
(2,1,5,4,0.10),
(3,2,3,1,0),
(4,3,4,1,0.15),
(5,3,2,3,0),
(6,4,8,2,0),
(7,5,7,1,0.05),
(8,6,6,6,0),
(9,7,1,1,0),
(10,7,2,2,0),
(11,8,3,2,0.20),
(12,9,5,10,0);

INSERT INTO departments VALUES
(1,'Engineering','Wilmington'),
(2,'Data','Bear'),
(3,'Education','Dover'),
(4,'Operations','Newark');

INSERT INTO employees VALUES
(1,'Grace','Hopper',1,'Engineering Manager',135000,'2020-01-10',NULL),
(2,'Alan','Turing',2,'Data Engineer',118000,'2021-03-15',1),
(3,'Katherine','Johnson',2,'Data Scientist',122000,'2021-07-20',1),
(4,'Dorothy','Vaughan',3,'Program Director',105000,'2019-09-01',NULL),
(5,'Mary','Jackson',1,'Software Engineer',110000,'2022-05-12',1),
(6,'Ida','Rhodes',4,'Operations Analyst',82000,'2023-02-06',4),
(7,'Timnit','Gebru',2,'ML Researcher',128000,'2022-11-11',3),
(8,'Radia','Perlman',1,'Network Architect',132000,'2018-06-18',1);

INSERT INTO projects VALUES
(1,'Youth Dashboard',3,45000,'2025-01-01','2025-06-30'),
(2,'Data Pipeline Upgrade',2,90000,'2025-02-01',NULL),
(3,'Website Redesign',1,30000,'2025-03-15','2025-08-15'),
(4,'Inventory Automation',4,55000,'2025-04-01',NULL),
(5,'AI Tutor Pilot',3,75000,'2025-05-01',NULL);

INSERT INTO tickets VALUES
(1,1,'login','low','2025-05-01','2025-05-02','closed'),
(2,3,'payment','high','2025-05-03',NULL,'open'),
(3,5,'shipping','medium','2025-05-05','2025-05-09','closed'),
(4,7,'product','high','2025-05-08',NULL,'open'),
(5,2,'login','medium','2025-05-09','2025-05-10','closed'),
(6,6,'payment','critical','2025-05-11',NULL,'open');

INSERT INTO students VALUES
(1,'Sierra','Holmes',8,'Bear'),
(2,'Cameron','Holmes',6,'Bear'),
(3,'Amaya','Holmes',4,'Bear'),
(4,'Jordan','Lee',7,'Dover'),
(5,'Taylor','Kim',9,'Newark'),
(6,'Morgan','Diaz',8,'Wilmington');

INSERT INTO courses VALUES
(1,'Intro to Python','Coding','beginner'),
(2,'SQL Basics','Data','beginner'),
(3,'Robotics Lab','Robotics','intermediate'),
(4,'Drone Safety','Drones','intermediate'),
(5,'Data Storytelling','Data','advanced');

INSERT INTO enrollments VALUES
(1,1,1,95,1),
(2,1,2,92,1),
(3,2,1,88,1),
(4,2,3,74,0),
(5,3,2,91,1),
(6,4,4,80,1),
(7,5,5,97,1),
(8,6,3,69,0),
(9,6,2,85,1);
"""


def ensure_database(reset: bool = False) -> None:
    DB_PATH.parent.mkdir(exist_ok=True)
    if reset and DB_PATH.exists():
        DB_PATH.unlink()
    with sqlite3.connect(DB_PATH) as conn:
        if reset or not table_exists(conn, "customers"):
            conn.executescript(SCHEMA_SQL)
            conn.executescript(SEED_SQL)
            conn.commit()


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    ).fetchone()
    return row is not None


def run_query(sql: str) -> dict[str, Any]:
    ensure_database()
    statement = sql.strip()
    if not statement:
        return {"ok": False, "error": "Write a SQL query before running it.", "hint": "Try SELECT * FROM customers;"}

    # Keep simulator safe and lesson-focused.
    blocked = ("drop ", "delete ", "update ", "insert ", "alter ", "create ", "replace ", "pragma ", "attach ")
    lowered = statement.lower()
    if any(word in lowered for word in blocked):
        return {
            "ok": False,
            "error": "This training sandbox only allows read-only SELECT queries.",
            "hint": "Use SELECT, WHERE, JOIN, GROUP BY, CTEs, or window functions to explore the data."
        }

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(statement)
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            return {
                "ok": True,
                "columns": columns,
                "rows": [dict(row) for row in rows],
                "row_count": len(rows)
            }
    except sqlite3.Error as exc:
        return {"ok": False, "error": str(exc), "hint": explain_sql_error(str(exc), statement)}


def explain_sql_error(error: str, sql: str) -> str:
    message = error.lower()
    lowered = sql.lower()
    if "no such table" in message:
        return "Check the table name. Open the Schema panel and copy the table name exactly."
    if "no such column" in message:
        return "Check the column name. The column may belong to another table and need a JOIN."
    if "syntax error" in message:
        return "Look near the word mentioned in the error. SQL order is usually SELECT, FROM, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT."
    if "ambiguous column" in message:
        return "Two joined tables have a column with the same name. Prefix it with a table name, like customers.customer_id."
    if "misuse of aggregate" in message:
        return "Aggregate functions like COUNT, SUM, and AVG usually need GROUP BY when mixed with regular columns."
    if "group" in lowered and "where" in lowered and "having" not in lowered:
        return "Use WHERE before grouping to filter rows, and HAVING after grouping to filter aggregated results."
    return "Read the lesson goal, compare your query to the example pattern, and fix one part at a time."


def get_schema() -> dict[str, list[str]]:
    ensure_database()
    schema: dict[str, list[str]] = {}
    with sqlite3.connect(DB_PATH) as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
        for (table_name,) in tables:
            columns = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
            schema[table_name] = [f"{col[1]} {col[2]}" for col in columns]
    return schema
