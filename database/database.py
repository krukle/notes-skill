import os
from pathlib import Path
import sqlite3

class Database:
    def __init__(self):
        self.database_path = Path(Path.home(), 'mycroft-core', 'database', 'fastnotes-skill', 'database.db')
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.schema_path = f'{os.path.dirname(os.path.realpath(__file__))}{os.sep}schema.sql'
        try:
            conn = self._initialize_connection()
            self.get_all_posts()
        except sqlite3.OperationalError:
            with open(self.schema_path) as f:
                conn.executescript(f.read())
            conn.commit()
        finally:
            conn.close()
            
    def _initialize_connection(self) -> sqlite3.Connection:
        """Initialize a connection to the database with read, write and create rights.

        Returns:
            sqlite3.Connection: connection to database.
        """
        return sqlite3.connect(f"file:{self.database_path}?mode=rwc", uri=True)

    def _get_connection(self) -> sqlite3.Connection:
        """Get a sqlite3 connection with read and write rights.

        Returns:
            sqlite3.Connection: connection to database.
        """
        return sqlite3.connect(f"file:{self.database_path}?mode=rw", uri=True)

    def get_all_posts(self) -> "list[tuple[int, str, str]]":
        """Get all the posts .

        Returns:
            list: posts
                int: id
                str: date created
                str: content
        """
        conn = self._get_connection()
        posts = conn.execute('SELECT * FROM posts').fetchall()
        conn.close()
        return posts

    def get_post(self, post_id:int) -> "tuple[int, str, str]":
        """Get the post with the given ID .

        Returns:
            int: id
            str: date created
            str: content
        """
        conn = self._get_connection()
        post = conn.execute('SELECT * FROM posts WHERE id = ?',
                            (post_id, )).fetchone()
        conn.close()
        return post

    def create_post(self, content:str):
        conn = self._get_connection()
        conn.execute('INSERT INTO posts (content) VALUES (?)',
                     (content, ))
        conn.commit()
        conn.close()

    def edit_post(self, content:str, post_id:int):
        conn = self._get_connection()
        conn.execute('UPDATE posts SET content = ? WHERE id = ?',
                     (content, post_id))
        conn.commit()
        conn.close()

    def delete_all_posts(self):
        conn = self._get_connection()
        conn.execute('DELETE FROM posts')
        conn.commit()
        conn.close()

    def delete_post(self, post_id:int):
        conn = self._get_connection()
        conn.execute('DELETE FROM posts WHERE id = ?', (post_id, ))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    db = Database()