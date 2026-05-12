from fastapi import FastAPI
import sqlite3
import uvicorn

def lade_eintraege():
    """Lädt die Einträge aus der Datenbank und gibt sie als Dictionary zurück"""
    conn =sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    rows = cursor.fetchall()
    conn.close()

    zwischen = {}
    for datum, practice, erledigt in rows:
        if datum not in zwischen:
            zwischen[datum] = {}
        zwischen[datum][practice] = "y" if erledigt == 1 else "n"
        print(f"Nach Iteration: {zwischen}")
    entries = []
    for datum, eintrag in zwischen.items():
            eintrag["datum"] = datum
            entries.append(eintrag)
            print(f"Nach Wiederholung: {entries}")
    return entries

app = FastAPI()

@app.get("/")
def hello():
    """Gib eine freundliche Nachricht zurück"""
    return {"message": "Hello, World!"}

@app.get("/entries")
def get_entries() -> list[dict]:
        """Gibt die Einträge als JSON zurück"""
        return lade_eintraege()
        