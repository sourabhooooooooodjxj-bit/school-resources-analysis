import sqlite3

def create_database():
    con = sqlite3.connect("school.db")
    cursor = con.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            school_name TEXT NOT NULL,
            location TEXT NOT NULL,
            students INTEGER NOT NULL,
            teachers INTEGER NOT NULL,
            classrooms INTEGER DEFAULT 0,
            laboratories INTEGER DEFAULT 0,
            toilets INTEGER DEFAULT 0,
            computers INTEGER DEFAULT 0
        )
    """)

    con.commit()
    con.close()


create_database()
