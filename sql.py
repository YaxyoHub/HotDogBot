import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect_psql():
    db_name = os.getenv("DATABASE_NAME")
    db_user = os.getenv("DATABASE_USER")
    db_pass = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_port = os.getenv("DATABASE_PORT")

    DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?sslmode=require"

    return psycopg2.connect(DATABASE_URL)

"""Yangi taom qo'shish"""
def add_menu(name, price):
    conn = connect_psql()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM products WHERE name = %s;", (name,))
        if cursor.fetchone():
            return "Bu nomdagi taom allaqachon mavjud!"

        cursor.execute(
            "INSERT INTO products (name, price) VALUES (%s, %s);",
            (name, price)
        )
        conn.commit()
        return "✅ Yangi taom qo‘shildi!"
    except Exception as e:
        return f"Xatolik taom qo'shishda: {e}"
    finally:
        cursor.close()
        conn.close()
# 
def delete_menu(item_id):
    try:
        conn = connect_psql()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = %s;", (item_id,))
        conn.commit()
    except Exception as e:
        print("Xatolik:", e)
    finally:
        cursor.close()
        conn.close()

def get_product_by_id(product_id):
    try:
        conn = connect_psql()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM products WHERE id = %s;", (product_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("Xatolik:", e)
    finally:
        cursor.close()
        conn.close()
