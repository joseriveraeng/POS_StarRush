import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mysql.connector
from database import get_database_connection


def get_barcode(barcode):
    connection = get_database_connection()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM products WHERE barcode = %s AND is_active = TRUE"

    try:
        cursor.execute(query, (barcode,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error fetching product: {err}")
        return None
    finally:
        cursor.close()
        connection.close()


def add_new_product(barcode, name, cost_price, sale_price, initial_stock):
    connection = get_database_connection()
    if not connection:
        return False, "Error: Could not connect to the database"

    cursor = connection.cursor()
    query = """
        INSERT INTO products
            (barcode, name, cost_price, sale_price, current_stock, is_active)
        VALUES
            (%s, %s, %s, %s, %s, TRUE)
    """
    try:
        cursor.execute(query, (barcode, name, cost_price, sale_price, initial_stock))
        connection.commit()
        return True, f"Product '{name}' registered successfully."
    except mysql.connector.Error as err:
        connection.rollback()
        return False, f"Database error: {err}"
    finally:
        cursor.close()
        connection.close()


def restock_existing_product(barcode, added_stock, new_cost_price, new_sale_price=None):
    connection = get_database_connection()
    if not connection:
        return False, "Error: Could not connect to the database"

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT sale_price FROM products WHERE barcode = %s", (barcode,))
        product = cursor.fetchone()

        if not product:
            return False, "Product does not exist."

        final_sale_price = new_sale_price if new_sale_price is not None else product["sale_price"]

        query = """
            UPDATE products
            SET current_stock = current_stock + %s,
                cost_price = %s,
                sale_price = %s
            WHERE barcode = %s
        """
        cursor.execute(query, (added_stock, new_cost_price, final_sale_price, barcode))
        connection.commit()
        return True, "Stock and prices updated successfully."

    except mysql.connector.Error as err:
        connection.rollback()
        return False, f"Database error: {err}"
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    # Prueba del flujo desconectado
    code = "75099999"
    
    # 1. Simular escaneo
    prod = get_barcode(code)
    if not prod:
        print("1. Producto no existe en BD. Registrando nuevo...")
        add_new_product(code, "Papas Fritas 45g", 12.00, 18.00, 20)
    
    # 2. Simular reescaneo posterior (surtido)
    prod = get_barcode(code)
    if prod:
        print(f"2. Producto encontrado ('{prod['name']}'). Surtiendo +10 unidades...")
        restock_existing_product(code, 100, 20.50, 30)
        
    # 3. Verificación final
    final_prod = get_barcode(code)
    print("Estado final en BD:", final_prod)