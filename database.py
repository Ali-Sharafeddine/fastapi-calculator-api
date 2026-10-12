import sqlite3


def get_connection():
    return sqlite3.connect("calculator.db")


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            a REAL NOT NULL,
            b REAL NOT NULL,
            operation TEXT NOT NULL,
            result REAL NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_table()


def save_calculation(a: float, b: float, operation: str, result: float):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO calculations (a, b, operation, result)
        VALUES (?, ?, ?, ?)
        """,
        (a, b, operation, result)
    )

    connection.commit()
    connection.close()


def get_calculations():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, a, b, operation, result
        FROM calculations
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_calculations_count():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM calculations"
    )

    row = cursor.fetchone()

    connection.close()

    return row[0]


def delete_calculation(calculation_id: int) -> bool:
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM calculations WHERE id = ?",
            (calculation_id,)
        )

        deleted = cursor.rowcount > 0
        connection.commit()

        return deleted

    finally:
        connection.close()


def update_result(calculation_id: int, new_result: float):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE calculations
        SET result = ?
        WHERE id = ?
        """,
        (new_result, calculation_id)
    )

    connection.commit()
    connection.close()


