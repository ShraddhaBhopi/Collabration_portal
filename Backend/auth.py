import bcrypt
from Database.db import get_connection


def register_user(name, email, password, role):

    connection = get_connection()
    cursor = connection.cursor()

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, password_hash, role)
        )

        connection.commit()

        return True, "Registration successful."

    except Exception as error:

        connection.rollback()

        if "Duplicate entry" in str(error):
            return False, "Email already registered."

        return False, str(error)

    finally:

        cursor.close()
        connection.close()


def login_user(email, password):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = %s
        """,
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:
        return None

    valid = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"].encode("utf-8")
    )

    if valid:
        return user

    return None