import sqlite3 as sql


class DataBaseInterface:
    def __init__(self):
        self.conn = sql.connect('db/signatures_analysis.db')
        self.cursor = self.conn.cursor()
        self.setup_base_tables()

    def close(self):
        self.conn.close()

    def setup_base_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS signature_logs (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            generated_at DATETIME NOT NULL,
            extension TEXT NOT NULL,
            assurance DECIMAL(5,2) NOT NULL,
            correlation_matrix TEXT NOT NULL,
            signature_json TEXT NOT NULL
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS base_signatures (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            generated_at DATETIME NOT NULL,
            extension TEXT NOT NULL,
            signature_log_id INTEGER NOT NULL,
            FOREIGN KEY (signature_log_id)
                REFERENCES signature_logs (id)
        );
        """)

    def register_signature_log(self, sign):
        base_signature_id = self.get_next_signature_log_id()
        signature_json = "{}_{}.json".format(base_signature_id, sign.file_extension)

        if sign.last_compare:
            data = [[sign.file_extension, sign.last_compare['assurance'], sign.last_compare['correlation_matrix'], signature_json]]

            self.cursor.executemany("""
                INSERT INTO signature_logs (generated_at, extension, assurance, correlation_matrix, signature_json)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)
            """, data)
        else:
            data = [[sign.file_extension, '', '', signature_json]]

            self.cursor.executemany("""
                INSERT INTO signature_logs (generated_at, extension, assurance, correlation_matrix, signature_json)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)
            """, data)

        self.conn.commit()
        
        return signature_json

    def register_final_signature(self, extension):
        signature_json_id = self.get_last_log_id()
        data = [(signature_json_id, extension)]

        if self.has_base_signature(extension):
            self.cursor.executemany("""
                UPDATE base_signatures
                SET signature_log_id = ?,
                    generated_at = CURRENT_TIMESTAMP
                WHERE extension = ?
            """, data)

        else:
            self.cursor.executemany("""
                INSERT INTO base_signatures (generated_at, signature_log_id, extension)
                VALUES (CURRENT_TIMESTAMP, ?, ?)
            """, data)

        self.conn.commit()

    def has_base_signature(self, extension):
        self.cursor.execute("""
        SELECT * FROM base_signatures WHERE extension=?
        """, [extension])

        return self.cursor.fetchall().__len__() > 0

    def get_next_signature_log_id(self):
        self.cursor.execute("""
        SELECT MAX(id) from signature_logs
        """)

        next_row = self.cursor.fetchone()
        if next_row[0] is None:
            return 1
        else:
            return next_row[0] + 1

    def get_last_log_id(self):
        self.cursor.execute("""
        SELECT MAX(id) from signature_logs
        """)

        last_row = self.cursor.fetchone()
        if last_row[0] is None:
            return 1
        else:
            return last_row[0]

    def is_first_run(self):
        self.cursor.execute(""" SELECT * FROM base_signatures """)

        return self.cursor.fetchall().__len__() == 0

    def get_old_base_signature(self, extension):
        self.cursor.execute("""
        SELECT logs.signature_json FROM
        base_signatures as base_signs
        INNER JOIN signature_logs as logs
            ON base_signs.signature_log_id = logs.id
        WHERE base_signs.extension = ?
        """, [extension])

        tmp = self.cursor.fetchone()
        if tmp is not None:
            file_name = tmp[0]
            return file_name
