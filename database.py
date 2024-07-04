import functools
import pymysql

from config import Config


def db_session(config: Config):
    def wrapper(method):
        @functools.wraps(method)
        def wrapped(self, *args, **kwargs):
            connection = pymysql.connect(
                host=config.DB_HOST,
                port=3306,
                # database=config.DB_NAME,
                user=config.DB_USERNAME,
                password=config.DB_PASSWORD,
                cursorclass=pymysql.cursors.DictCursor
            )
            try:
                cursor = connection.cursor()
                connection.begin()
                try:
                    result = method(self, *args, **kwargs, cursor=cursor)
                    connection.commit()
                    return result
                except Exception as e:
                    print(f'Ошибка: {e}')
                    connection.rollback()
                    print('Откат изменений')
                    cursor.execute("ALTER TABLE `boobscoin`.`users` AUTO_INCREMENT = 1")
                    connection.commit()
                finally:
                    cursor.close()
            except Exception as err:
                print(f'Произошла ошибка подключения: {err}')
            finally:
                if connection:
                    connection.close()
        return wrapped
    return wrapper



class Database:
    config = Config()
    
    @db_session(config)
    def __init__(self, cursor: pymysql.cursors.DictCursor):
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{self.config.DB_NAME}`")
        cursor.execute(f"USE `{self.config.DB_NAME}`")
        cursor.execute("CREATE TABLE IF NOT EXISTS `users`(id int AUTO_INCREMENT," \
                        "chat_id int UNIQUE KEY," \
                        "username varchar(32)," \
                        "score int," \
                        "PRIMARY KEY(id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS `boosts`(id int AUTO_INCREMENT," \
                        "user_id int," \
                        "name_boost varchar(46)," \
                        "lvl_boost int," \
                        "PRIMARY KEY(id)," \
                        "FOREIGN KEY (user_id) REFERENCES users(id))")
    
    @db_session(config)
    def __use_db(self, cursor: pymysql.cursors.DictCursor):
        cursor.execute(f"USE `{self.config.DB_NAME}`")
    
    @db_session(config)
    def add_user(self, chat_id: int, username: str, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("INSERT INTO users (chat_id, username, score) VALUES (%s, %s, %s)", (chat_id, username, 0))
        
    @db_session(config)
    def get_user(self, chat_id: int, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id))
        return cursor.fetchone()
    
    @db_session(config)
    def get_user_score(self, chat_id: int, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("SELECT score FROM users WHERE chat_id = %s", (chat_id))
        return cursor.fetchone()['score']
    
    @db_session(config)
    def get_all_users(self, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("SELECT * FROM users ORDER BY score DESC")
        return cursor.fetchall()
        
    @db_session(config)
    def update_user_score(self, chat_id: int, score: int, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("UPDATE users SET score = %s WHERE chat_id = %s", (score, chat_id))


    @db_session(config)
    def add_boost(self, chat_id: int, name_boost: str, lvl_boost: int, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("SELECT id FROM users WHERE chat_id = %s", (chat_id))
        user_id = cursor.fetchone()['id']
        cursor.execute("SELECT * FROM boosts WHERE user_id = %s AND name_boost = %s", (user_id, name_boost))
        if cursor.fetchone():
            return False
        else:
            cursor.execute("INSERT INTO boosts (user_id, name_boost, lvl_boost) VALUES (%s, %s, %s)",
                           (user_id, name_boost, lvl_boost))

    @db_session(config)
    def get_boost(self, chat_id: int, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("SELECT id FROM users WHERE chat_id = %s", (chat_id))
        user_id = cursor.fetchone()['id']
        cursor.execute("SELECT boosts.name_boost, boosts.lvl_boost FROM boosts WHERE user_id = %s", (user_id))
        return cursor.fetchall()
    
    @db_session(config)
    def get_boost_lvl(self, chat_id: int, name_boost: str, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("SELECT id FROM users WHERE chat_id = %s", (chat_id))
        user_id = cursor.fetchone()['id']
        cursor.execute("SELECT lvl_boost FROM boosts WHERE user_id = %s AND name_boost = %s", (user_id, name_boost))
        return cursor.fetchone()['lvl_boost']
    
    @db_session(config)
    def update_boost(self, chat_id: int, name_boost: str, lvl_boost: int, cursor: pymysql.cursors.DictCursor):
        self.__use_db()
        cursor.execute("UPDATE boosts SET lvl_boost = %s WHERE user_id = (SELECT id FROM users WHERE chat_id = %s) AND name_boost = %s",
                       (lvl_boost, chat_id, name_boost))


def db(config: Config):
    Database.config = config
    return Database()


__init__ = [
    db
]