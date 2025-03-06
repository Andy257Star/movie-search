import mysql.connector
from db_config import DB_CONFIG
from logs import QueryLogger


class MovieSearch:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            self.logger = QueryLogger()
        except mysql.connector.Error as err:
            print(f"Ошибка подключения к базе данных: {err}")
            self.conn = None
            self.cursor = None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def search_by_keyword(self, keywords):
        if not self.conn:
            return []

        words = keywords.split()
        conditions = " OR ".join(["f.title LIKE %s OR f.description LIKE %s"] * len(words))
        query = f"""
        SELECT f.title, f.description, f.release_year, f.length, c.name 
        FROM film f
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category c ON fc.category_id = c.category_id
        WHERE {conditions} 
        LIMIT 10
        """
        params = [f"%{word}%" for word in words for _ in range(2)]

        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            self.logger.log_query(f"Keyword search: {keywords}")
            return results
        except mysql.connector.Error as err:
            print(f"Ошибка при выполнении запроса: {err}")
            return []

    def search_by_genre(self, genre):
        if not self.conn:
            return []

        query = """
        SELECT f.title, f.description, f.release_year, f.length, c.name 
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE c.name = %s
        LIMIT 10
        """

        try:
            self.cursor.execute(query, (genre,))
            results = self.cursor.fetchall()
            self.logger.log_query(f"Genre search: {genre}")
            return results
        except mysql.connector.Error as err:
            print(f"Ошибка при выполнении запроса: {err}")
            return []

    def search_by_genre_and_year(self, genre, year):
        if not self.conn:
            return []

        query = """
        SELECT f.title, f.description, f.release_year, f.length, c.name 
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE c.name = %s AND f.release_year = %s
        LIMIT 10
        """

        try:
            self.cursor.execute(query, (genre, year))
            results = self.cursor.fetchall()
            self.logger.log_query(f"Genre & Year search: {genre}, {year}")
            return results
        except mysql.connector.Error as err:
            print(f"Ошибка при выполнении запроса: {err}")
            return []

    def get_available_genres(self):
        if not self.conn:
            return []

        query = "SELECT name FROM category"

        try:
            self.cursor.execute(query)
            genres = [row[0] for row in self.cursor.fetchall()]
            return genres
        except mysql.connector.Error as err:
            print(f"Ошибка при получении жанров: {err}")
            return []
