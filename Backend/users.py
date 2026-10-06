from Database.db import get_connection


def get_user(user_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = %s
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


def update_profile(
    user_id,
    department,
    skills,
    bio
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET department = %s,
            skills = %s,
            bio = %s
        WHERE id = %s
        """,
        (
            department,
            skills,
            bio,
            user_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def find_teammates(
    current_user_id,
    skill=""
):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if skill:

        cursor.execute(
            """
            SELECT id, name, email,
                   department, skills, bio
            FROM users
            WHERE role = 'student'
            AND id != %s
            AND skills LIKE %s
            """,
            (
                current_user_id,
                f"%{skill}%"
            )
        )

    else:

        cursor.execute(
            """
            SELECT id, name, email,
                   department, skills, bio
            FROM users
            WHERE role = 'student'
            AND id != %s
            """,
            (current_user_id,)
        )

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return users