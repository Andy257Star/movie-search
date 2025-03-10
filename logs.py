import mysql.connector
from db_config import LOG_DB_CONFIG


class QueryLogger:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(**LOG_DB_CONFIG)
            self.cursor = self.conn.cursor()
            self.create_table()
        except mysql.connector.Error as err:
            print(f"Ошибка подключения к базе данных логов: {err}")
            self.conn = None
            self.cursor = None

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS Andrii_Sevruk_queries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            query_text VARCHAR(255) NOT NULL,
            query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def log_query(self, query_text):
        if not self.conn:
            return

        query = "INSERT INTO Andrii_Sevruk_queries (query_text) VALUES (%s)"
        self.cursor.execute(query, (query_text,))
        self.conn.commit()

    def get_popular_queries(self):
        if not self.conn:
            return []

        query = """
        SELECT query_text, COUNT(*) as count
        FROM Andrii_Sevruk_queries
        GROUP BY query_text
        ORDER BY count DESC
        LIMIT 10
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
