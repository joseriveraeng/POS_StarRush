Python
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mysql.connector
from database import get_database_connection


def open_cash_session(user_id, initial_cash):
    connection = get_database_connection()
    if not connection:
        return False, "Error: Could not connect to the database", None

    cursor = connection.cursor()
    query = """
        INSERT INTO cash_sessions (user_id, opened_at, initial_cash, estimated_cash)
        VALUES (%s, NOW(), %s, %s)
    """
    try:
        cursor.execute(query, (user_id, initial_cash, initial_cash))
        connection.commit()
        session_id = cursor.lastrowid
        return True, "Cash session opened successfully.", session_id
    except mysql.connector.Error as err:
        connection.rollback()
        return False, f"Database error: {err}", None
    finally:
        cursor.close()
        connection.close()


def close_cash_session(session_id, real_cash):
    connection = get_database_connection()
    if not connection:
        return False, "Error: Could not connect to the database"

    cursor = connection.cursor()
    query = """
        UPDATE cash_sessions
        SET closed_at = NOW(),
            real_cash = %s
        WHERE session_id = %s
    """
    try:
        cursor.execute(query, (real_cash, session_id))
        connection.commit()
        return True, "Cash session closed successfully."
    except mysql.connector.Error as err:
        connection.rollback()
        return False, f"Database error: {err}"
    finally:
        cursor.close()
        connection.close()


def register_cash_movement(movement_type, amount, description, session_id=None, supplier_id=None):
    connection = get_database_connection()
    if not connection:
        return False, "Error: Could not connect to the database"

    cursor = connection.cursor()
    query = """
        INSERT INTO cash_movements (session_id, supplier_id, movement_type, amount, description, created_at)
        VALUES (%s, %s, %s, %s, %s, NOW())
    """

    try:
        cursor.execute(query, (session_id, supplier_id, movement_type, amount, description))
        connection.commit()
        return True, "Cash movement registered successfully."
    except mysql.connector.Error as err:
        connection.rollback()
        return False, f"Database error: {err}"
    finally:
        cursor.close()
        connection.close()


def get_today_cash_movements():
    connection = get_database_connection()
    if not connection:
        return None

    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT movement_id, session_id, supplier_id, movement_type, amount, description, created_at
        FROM cash_movements
        WHERE DATE(created_at) = CURDATE()
        ORDER BY created_at DESC
    """

    try:
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error fetching cash movements: {err}")
        return None
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    # 1. Probar apertura de turno (simulando user_id = 1 y $500 de fondo)
    success, msg, session_id = open_cash_session(1, 500.00)
    print("Prueba 1 (Abrir Turno):", msg, "| Session ID:", session_id)

    if session_id:
        # 2. Probar movimiento de salida vinculado a la sesion
        success, msg = register_cash_movement('OUT', 150.00, "Pago de refrescos", session_id=session_id)
        print("Prueba 2 (Salida en sesion):", msg)

        # 3. Probar cierre de turno
        success, msg = close_cash_session(session_id, 350.00)
        print("Prueba 3 (Cerrar Turno):", msg)