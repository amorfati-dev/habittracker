import json
import sqlite3

try: 
    with open("entries.json", "r") as f:
        entries = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    entries = {}

conn = sqlite3.connect("tracker.db")
cursor = conn.cursor()

for tag, eintrag in entries.items():
    # tag ist der Schlüssel ("2026-05-04")
    # eintrag ist der Wert (das innere Dict)
    for practice, status in eintrag.items():
    # practice ist "meditation", "kraftsport", ...
    # status ist "y" oder "n"
        erledigt = 1 if status == "y" else 0
        cursor.execute(
        "INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)",
        (tag, practice, erledigt))



conn.commit()
conn.close()
