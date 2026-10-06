from Database.db import get_connection


def add_task(
    project_id,
    title,
    description
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks
        (project_id, title, description)
        VALUES (%s, %s, %s)
        """,
        (
            project_id,
            title,
            description
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_tasks(project_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE project_id = %s
        ORDER BY id DESC
        """,
        (project_id,)
    )

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return tasks