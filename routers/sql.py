import sqlite3
import csv
import os

DB_NAME = 'zus_coffee.db'
CSV_FILE = os.path.join(os.path.dirname(__file__), 'zus_locations.csv')


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS zus_locations (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               address TEXT NOT NULL,
               opening_time TEXT NOT NULL,
               closing_time TEXT NOT NULL,
               services TEXT NOT NULL
               );
               """)

with open(CSV_FILE, 'r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    records = [
        (
            row['name'],
            row['address'],
            row['opening_time'],
            row['closing_time'],
            row['services']
        )
        for row in csv_reader
    ]

cursor.executemany("""
INSERT INTO zus_locations (name, address, opening_time, closing_time, services)
VALUES (?, ?, ?, ?, ?);
""", records)

conn.commit()
conn.close()


