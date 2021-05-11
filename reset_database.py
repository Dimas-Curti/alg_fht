import sqlite3 as sql
import shutil

conn = sql.connect('db/signatures_analysis.db')
cursor = conn.cursor()

cursor.executescript("""
    DROP TABLE IF EXISTS signature_logs;
    DROP TABLE IF EXISTS base_signatures;
""")

shutil.rmtree("db/csv")


