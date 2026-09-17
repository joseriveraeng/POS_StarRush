import sys
import os
import mysql.connector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_database_connection


def register_sale(session_id, items, total, customer_id=None, payment_method='CASH', payment_status='PAID'):
    connection = get_database_connection()
    if not connection:
        return False, "Database connection error."

    cursor = connection.cursor()

    try:
        connection.autocommit = False

        query_sale = """
            INSERT INTO sales (session_id, customer_id, total, payment_method, payment_status)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_sale, (session_id, customer_id, total, payment_method, payment_status))
        
        sale_id = cursor.lastrowid

        query_detail = """
            INSERT INTO sale_details (sale_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        query_update_stock = """
            UPDATE products 
            SET current_stock = current_stock - %s 
            WHERE product_id = %s AND current_stock >= %s
        """

        for item in items:
            cursor.execute(query_detail, (
                sale_id, 
                item['product_id'], 
                item['quantity'], 
                item['unit_price'], 
                item['subtotal']
            ))

            cursor.execute(query_update_stock, (
                item['quantity'], 
                item['product_id'], 
                item['quantity']
            ))

            if cursor.rowcount == 0:
                raise Exception(f"Insufficient stock or product not found for ID: {item['product_id']}")

        connection.commit()
        return True, {"message": "Sale registered successfully.", "sale_id": sale_id}

    except mysql.connector.Error as err:
        connection.rollback()
        return False, f"Database error: {err}"
    except Exception as ex:
        connection.rollback()
        return False, f"Sale cancelled: {str(ex)}"
    finally:
        connection.autocommit = True
        cursor.close()
        connection.close()


if __name__ == "__main__":
    demo_cart = [
        {'product_id': 2, 'quantity': 5, 'unit_price': 20.00, 'subtotal': 36.00}
    ]
    
    success, result = register_sale(
        session_id=1, 
        items=demo_cart, 
        total=36.00, 
        customer_id=None,
        payment_method='CASH', 
        payment_status='PAID'
    )
    
    print("Test result:", result)