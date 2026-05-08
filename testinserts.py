import sqlite3

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)",
    ("2026-05-04", "meditation", 1)
)

cursor.execute(
    "INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)",
    ("2026-05-05", "kraftsport", 1)
)

cursor.execute(
    "INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)",
    ("2026-05-05", "meditation", 1)
)

cursor.execute(
    "INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)",
    ("2026-05-05", "sauna", 0)
)

conn.commit()
conn.close()

