import sqlite3

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS entries (
    datum TEXT, 
    practice TEXT, 
    erledigt INTEGER,
    UNIQUE(datum, practice)
               )
""")

conn.commit()    # Änderungen schreiben
conn.close()