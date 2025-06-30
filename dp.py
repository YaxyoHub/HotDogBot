import psycopg2
import os
from dotenv import load_dotenv
ORDERS_FILE = "orders.json"

load_dotenv()

def connect_psql():
    db_name = os.getenv("DATABASE_NAME")
    db_user = os.getenv("DATABASE_USER")
    db_pass = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")

    DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?sslmode=require"

    return psycopg2.connect(DATABASE_URL)

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
