import sqlite3 as sql


class DataBaseConnection:
    def __init__(self):
        self.conn = sql.connect('db/signatures_analysis.db')
        self.cursor = self.conn.cursor()
        self.create_base_tables()

    def close(self):
        self.conn.close()

    def create_base_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS base_signatures (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            generated_at DATETIME NOT NULL,
            extension TEXT NOT NULL,
            final_signature TEXT
        );            
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS signature_logs (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            generated_at DATETIME NOT NULL,
            extension TEXT NOT NULL,
            assurance DECIMAL(5,2) NOT NULL,
            correlation_matrix TEXT NOT NULL,
            final_signature TEXT NOT NULL
        );
        """)

    def register_signature_log(self, extension, assurance, correlation_matrix, final_signature):
        data = [[extension, assurance, correlation_matrix, final_signature]]

        self.cursor.executemany("""
            INSERT INTO signature_logs (generated_at, extension, assurance, correlation_matrix, final_signature)
            VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)
        """, data)

        self.conn.commit()

    def register_final_signature(self, extension, final_signature):
        data = [(final_signature, extension)]

        if self.has_base_signature(extension):
            self.cursor.executemany("""
                UPDATE base_signatures
                SET final_signature = ?,
                    generated_at = CURRENT_TIMESTAMP
                WHERE extension = ?
            """, data)

        else:
            self.cursor.executemany("""
                        INSERT INTO base_signatures (generated_at, final_signature, extension)
                        VALUES (CURRENT_TIMESTAMP, ?, ?)
                    """, data)

        self.conn.commit()

    def has_base_signature(self, extension):
        self.cursor.execute("""
        SELECT * FROM base_signatures WHERE extension=?
        """, [extension])

        return self.cursor.fetchall().__len__() > 0

