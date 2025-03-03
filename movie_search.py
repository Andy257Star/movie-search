from db_config import get_db_connection
from logs import QueryLogger

class MovieSearch:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.logger = QueryLogger()

    def search_by_keyword(self, keywords):
        words = keywords.split()
        query = """
        SELECT f.film_id, f.title, f.description, f.release_year, f.length, c.name 
        FROM film f
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category c ON fc.category_id = c.category_id
        WHERE """ + " OR ".join(["f.title LIKE %s OR f.description LIKE %s" for _ in words]) + " LIMIT 10"

        params = [f"%{word}%" for word in words for _ in range(2)]
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()

        self.logger.log_query(f"Keyword search: {keywords}")
        return results

    def search_by_genre(self, genre):
        query = """
        SELECT f.film_id, f.title, f.description, f.release_year, f.length, c.name 
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE c.name = %s
        LIMIT 10
        """
        self.cursor.execute(query, (genre,))
        results = self.cursor.fetchall()

        self.logger.log_query(f"Genre search: {genre}")
        return results

    def search_by_genre_and_year(self, genre, year):
        query = """
        SELECT f.film_id, f.title, f.description, f.release_year, f.length, c.name 
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE c.name = %s AND f.release_year = %s
        LIMIT 10
        """
        self.cursor.execute(query, (genre, year))
        results = self.cursor.fetchall()

        self.logger.log_query(f"Genre & Year search: {genre}, {year}")
        return results

    def get_available_genres(self):
        query = "SELECT name FROM category"
        self.cursor.execute(query)
        genres = [row[0] for row in self.cursor.fetchall()]
        return genres
