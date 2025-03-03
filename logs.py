import mysql.connector
from db_config import get_log_db_connection

class QueryLogger:
    def __init__(self):
        self.conn = get_log_db_connection()
        self.cursor = self.conn.cursor()
        self.create_table()

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
        query = "INSERT INTO Andrii_Sevruk_queries (query_text) VALUES (%s)"
        self.cursor.execute(query, (query_text,))
        self.conn.commit()

    def get_popular_queries(self):
        query = """
        SELECT query_text, COUNT(*) as count
        FROM Andrii_Sevruk_queries
        GROUP BY query_text
        ORDER BY count DESC
        LIMIT 10
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
