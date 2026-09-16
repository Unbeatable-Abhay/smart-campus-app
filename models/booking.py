from utils.db import get_connection, release_connection


def create_booking(user_id, resource_id, start_time, end_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (user_id, resource_id, start_time, end_time, status) VALUES (%s, %s, %s, %s, 'pending') RETURNING id",
        (user_id, resource_id, start_time, end_time)
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    release_connection(conn)
    return new_id


def get_bookings_for_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, user_id, resource_id, start_time, end_time, status, created_at FROM bookings WHERE user_id = %s",
        (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    release_connection(conn)
    return _rows_to_dicts(rows)


def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, user_id, resource_id, start_time, end_time, status, created_at FROM bookings"
    )
    rows = cursor.fetchall()
    cursor.close()
    release_connection(conn)
    return _rows_to_dicts(rows)


def get_booking_by_id(booking_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, user_id, resource_id, start_time, end_time, status, created_at FROM bookings WHERE id = %s",
        (booking_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    release_connection(conn)

    if row is None:
        return None

    return _rows_to_dicts([row])[0]


def update_booking_status(booking_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE bookings SET status = %s WHERE id = %s",
        (new_status, booking_id)
    )
    conn.commit()
    cursor.close()
    release_connection(conn)


def get_conflicting_bookings(resource_id, start_time, end_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id FROM bookings
        WHERE resource_id = %s
        AND status IN ('pending', 'approved')
        AND start_time < %s
        AND end_time > %s
        """,
        (resource_id, end_time, start_time)
    )
    rows = cursor.fetchall()
    cursor.close()
    release_connection(conn)
    return len(rows)


def _rows_to_dicts(rows):
    bookings = []
    for row in rows:
        bookings.append({
            "id": row[0],
            "user_id": row[1],
            "resource_id": row[2],
            "start_time": str(row[3]),
            "end_time": str(row[4]),
            "status": row[5],
            "created_at": str(row[6])
        })
    return bookings