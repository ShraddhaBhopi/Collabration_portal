from Database.db import get_connection


def get_notifications(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, message, is_read, created_at
        FROM notifications
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    notifications = cursor.fetchall()

    cursor.close()
    connection.close()

    return notifications


def mark_notification_read(notification_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE notifications
        SET is_read = TRUE
        WHERE id = %s AND user_id = %s
        """,
        (notification_id, user_id)
    )

    connection.commit()

    cursor.close()
    connection.close()