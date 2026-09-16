from utils.db import get_connection, release_connection
import bcrypt


def create_user(name, email, password, role, department):
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, role, department) VALUES (%s, %s, %s, %s, %s) RETURNING id",
        (name, email, password_hash, role, department)
    )
    new_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    release_connection(conn)

    return new_id


def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email, password_hash, role, department FROM users WHERE email = %s",
        (email,)
    )
    row = cursor.fetchone()
    cursor.close()
    release_connection(conn)

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "password_hash": row[3],
        "role": row[4],
        "department": row[5]
    }


def check_password(plain_password, password_hash):
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))