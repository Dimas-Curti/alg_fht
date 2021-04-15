import sqlite3 as sql


class DataBaseConnection:
    def __init__(self):
        self.conn = sql.connect('db/signatures_analysis.db')
        self.cursor = self.conn.cursor()
        self.create_base_signature_table()

    def close(self):
        self.conn.close()

    def create_base_signature_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS base_signatures (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            generated_at DATETIME NOT NULL,
            extension TEXT NOT NULL,
            signature TEXT
        );
            
        """)

    def register_base_signature(self, extension, signature):
        self.create_base_signature_table()

        data = [(extension, signature)]
        self.cursor.executemany("""
            INSERT INTO base_signatures (generated_at, extension, signature)
            VALUES (CURRENT_TIMESTAMP, ?, ?)
        """, data)

        self.conn.commit()

