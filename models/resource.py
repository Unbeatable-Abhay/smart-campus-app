from utils.db import get_connection, release_connection


def get_all_resources():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, capacity, department, location FROM resources")
    rows = cursor.fetchall()
    cursor.close()
    release_connection(conn)

    resources = []
    for row in rows:
        resources.append({
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "capacity": row[3],
            "department": row[4],
            "location": row[5]
        })

    return resources


def create_resource(name, type, capacity, department, location):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO resources (name, type, capacity, department, location) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (name, type, capacity, department, location)
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    release_connection(conn)
    return new_id


def check_resource_availability(resource_id, start_time, end_time):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT COUNT(*) FROM bookings
        WHERE resource_id = %s
        AND status IN ('pending', 'approved')
        AND start_time < %s
        AND end_time > %s
        """,
        (resource_id, end_time, start_time)
    )
    conflict_count = cursor.fetchone()[0]
    cursor.close()
    release_connection(conn)

    return conflict_count == 0