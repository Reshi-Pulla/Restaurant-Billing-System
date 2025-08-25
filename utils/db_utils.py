import sqlite3
import os
import csv
from datetime import datetime

DB_PATH = 'db/restaurant.db'

def create_tables():
    os.makedirs('db', exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        gst REAL,
        calories INTEGER,
        image_url TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_number TEXT,
        date TEXT,
        customer_name TEXT,
        order_type TEXT,
        total REAL,
        payment_method TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
        order_id INTEGER,
        item_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(item_id) REFERENCES menu(id)
    )''')

    conn.commit()
    conn.close()

def load_menu_from_csv():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM menu")
    if cursor.fetchone()[0] > 0:
        print("✅ Menu already exists. Skipping load.")
        conn.close()
        return

    with open('data/menu.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('''
                INSERT INTO menu (name, category, price, gst, calories, image_url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['name'],
                row['category'],
                float(row['price']),
                float(row['gst']),
                int(row.get('calories', 0)),
                row.get('image_url', '')
            ))
    conn.commit()
    conn.close()
    print("✅ Menu loaded into database.")

def get_menu():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_bill_number():
    today = datetime.now().strftime("%Y%m%d")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM orders WHERE date LIKE ?", (f"%{today[:4]}-{today[4:6]}-{today[6:]}",))
    count = cursor.fetchone()[0] + 1
    conn.close()
    return f"BILL-{today}-{str(count).zfill(3)}"

def save_order(order_details, order_items):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (bill_number, date, customer_name, order_type, total, payment_method)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', order_details)
    order_id = cursor.lastrowid
    for item_id, qty in order_items.items():
        cursor.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)", (order_id, item_id, qty))
    conn.commit()
    conn.close()
