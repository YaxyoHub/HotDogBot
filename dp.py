import psycopg2
import os
from dotenv import load_dotenv
ORDERS_FILE = "orders.json"

load_dotenv()

def connect_psql():
    return psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=os.getenv("DATABASE_HOST"),
        port=os.getenv("DATABASE_PORT")
    )

def get_all_products():
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products ORDER BY id;")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_product_by_id(product_id):
    conn = connect_psql()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE id = %s;", (product_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result if result else ("Noma’lum", 0)

def add_menu(name, price):
    conn = connect_psql()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM products WHERE name = %s;", (name,))
        if cursor.fetchone():
            return "❌ Bu nomdagi mahsulot allaqachon mavjud!"
        cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s);", (name, price))
        conn.commit()
        return "✅ Yangi mahsulot qo‘shildi!"
    except Exception as e:
        return f"Xatolik: {e}"
    finally:
        cursor.close()
        conn.close()