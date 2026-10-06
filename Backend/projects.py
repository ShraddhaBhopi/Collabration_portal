from Database.db import get_connection


def create_project(
    title,
    description,
    owner_id
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO projects
        (title, description, owner_id)
        VALUES (%s, %s, %s)
        """,
        (
            title,
            description,
            owner_id
        )
    )

    project_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO project_members
        (project_id, user_id)
        VALUES (%s, %s)
        """,
        (
            project_id,
            owner_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return project_id


def get_projects():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            projects.*,
            users.name AS owner_name
        FROM projects
        JOIN users
        ON projects.owner_id = users.id
        ORDER BY projects.created_at DESC
        """
    )

    projects = cursor.fetchall()

    cursor.close()
    connection.close()

    return projects


def join_project(project_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO project_members
            (project_id, user_id)
            VALUES (%s, %s)
            """,
            (
                project_id,
                user_id
            )
        )

        connection.commit()

        return True

    except Exception:

        connection.rollback()

        return False

    finally:

        cursor.close()
        connection.close()


def get_project_members(project_id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            users.id,
            users.name,
            users.email,
            users.skills
        FROM project_members
        JOIN users
        ON project_members.user_id = users.id
        WHERE project_members.project_id = %s
        """,
        (project_id,)
    )

    members = cursor.fetchall()

    cursor.close()
    connection.close()

    return members