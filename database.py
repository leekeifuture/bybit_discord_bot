import logging
from contextlib import contextmanager

from psycopg2 import pool
from psycopg2.extensions import AsIs, ISQLQuote, adapt

logger = logging.getLogger(__name__)


class User:
    def __init__(self,
                 uid: int,
                 telegram_id: int = None,
                 discord_id: int = None,
                 is_approved: int = None):
        self.uid = uid
        self.telegram_id = telegram_id
        self.discord_id = discord_id
        self.is_approved = is_approved

    def __str__(self):
        return f'{self.__class__}: {self.__dict__}'

    def __repr__(self):
        return self.__str__()

    def __conform__(self, protocol):
        if protocol is ISQLQuote:
            return self.__getquoted()
        return None

    def __getquoted(self):
        _uid = adapt(self.uid).getquoted().decode('utf-8')
        _telegram_id = adapt(self.telegram_id).getquoted().decode('utf-8')
        _discord_id = adapt(self.discord_id).getquoted().decode('utf-8')
        _is_approved = adapt(self.is_approved).getquoted().decode('utf-8')
        return AsIs(f'{_uid}, {_telegram_id}, {_discord_id}, {_is_approved}')


class Database:
    MIN_CONN = 2
    MAX_CONN = 10

    def __init__(self, connection_string: str, min_conn: int = MIN_CONN,
                 max_conn: int = MAX_CONN):
        self.connection_string = connection_string
        self.connection_pool = pool.SimpleConnectionPool(
            min_conn, max_conn, self.connection_string)
        self.__create_table()

    @contextmanager
    def __db(self):
        """
            Gets connection from pool and creates cursor within current context

            Yields:
                (psycopg2.extensions.connection, psycopg2.extensions.cursor):
                    Connection and cursor
        """
        con = self.connection_pool.getconn()
        cur = con.cursor()
        try:
            yield con, cur
        finally:
            cur.close()
            self.connection_pool.putconn(con)

    def __create_table(self):
        """
            Creates 'users' table
        """
        with self.__db() as (connection, cursor):
            try:
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS users
                        (   
                            id serial primary key not null,
                            uid bigint unique not null,
                            telegram_id bigint unique,
                            discord_id bigint unique,
                            is_approved boolean default false not null
                        )
                    """
                )
            except Exception as e:
                logger.error(e, exc_info=True)
                connection.rollback()
            else:
                connection.commit()

    def insert(self, entity: User):
        with self.__db() as (connection, cursor):
            try:
                cursor.execute("""
                                INSERT INTO users (
                                    uid, telegram_id, discord_id, is_approved
                                )
                                VALUES (%s)
                                """, (entity,))
            except Exception as e:
                logger.error(e, exc_info=True)
                connection.rollback()
            else:
                connection.commit()

    def find_by_uid(self, uid: int) -> User:
        with self.__db() as (_, cursor):
            try:
                cursor.execute("""
                                SELECT uid, telegram_id, discord_id, is_approved
                                FROM users
                                WHERE uid = %s
                                """, (uid,))
            except Exception as e:
                logger.error(e, exc_info=True)

            user = cursor.fetchall()

        return user

    def find_by_discord_id(self, discord_id: int) -> User:
        with self.__db() as (_, cursor):
            try:
                cursor.execute("""
                                SELECT uid, telegram_id, discord_id, is_approved
                                FROM users
                                WHERE discord_id = %s
                                """, (discord_id,))
            except Exception as e:
                logger.error(e, exc_info=True)

            user = cursor.fetchall()

        return user
