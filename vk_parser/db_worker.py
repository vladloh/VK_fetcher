"""Work with database."""
import sqlite3

from vk_parser.config import DATABASE_NAME, DATABASE_PATH


def command(func):
    """Handle db-commands."""
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DATABASE_PATH)
        try:
            res = func(conn.cursor(), *args, **kwargs)
        except Exception:
            res = None
        finally:
            conn.commit()
            conn.close()
        return res

    return wrapper


@command
def create_db_if_not_exists(cursor):
    """Create database."""
    sql_request = f"""
        CREATE TABLE IF NOT EXISTS {DATABASE_NAME}
        (id_from INTEGER, id_to INTEGER, PRIMARY KEY (id_from, id_to))
    """
    cursor.execute(sql_request)


@command
def drop_db_if_exists(cursor):
    """Delete table."""
    cursor.execute(f'DROP TABLE IF EXISTS {DATABASE_NAME}')


@command
def add_friendlist(cursor, user_id, friend_list):
    """Add user's friendlist."""
    friend_edges = [(user_id, user_friend) for user_friend in friend_list]
    friend_edges.append((user_id, user_id))
    cursor.executemany(
        f'INSERT OR IGNORE INTO {DATABASE_NAME} VALUES (?, ?)',
        friend_edges,
    )


@command
def get_user_friends(cursor, user_id):
    """Get user's friendlist from database."""
    edges = cursor.execute(
        f'SELECT * FROM {DATABASE_NAME} WHERE id_from=:user_id',
        {'user_id': user_id},
    ).fetchall()
    if not edges:
        return None
    return [id_to for (_, id_to) in edges if id_to != user_id]
