import sqlite3


def create_database():
    conn = sqlite3.connect("school.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_name TEXT NOT NULL,
            location TEXT NOT NULL,
            students INTEGER NOT NULL,
            teachers INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE schools ADD COLUMN classrooms INTEGER DEFAULT 0")
cursor.execute("ALTER TABLE schools ADD COLUMN laboratories INTEGER DEFAULT 0")
cursor.execute("ALTER TABLE schools ADD COLUMN toilets INTEGER DEFAULT 0")
cursor.execute("ALTER TABLE schools ADD COLUMN computers INTEGER DEFAULT 0")

conn.commit()
conn.close()
create_database()