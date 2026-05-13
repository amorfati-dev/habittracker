from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

practices = ["meditation", "sauna", "kraftsport", "coding"]

class Eintrag(BaseModel):
    datum: str
    meditation: str
    sauna: str
    kraftsport: str
    coding: str

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

def speichere_eintrag(eintrag: Eintrag):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    for practice in practices:
        wert = getattr(eintrag, practice)
        erledigt = 1 if wert == "y" else 0
        cursor.execute("INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)", (eintrag.datum, practice, erledigt))
    conn.commit()
    conn.close()

app = FastAPI()

@app.get("/")
def hello():
    """Gib eine freundliche Nachricht zurück"""
    return {"message": "Hello, World!"}

@app.get("/entries")
def get_entries() -> list[Eintrag]:
        """Gibt die Einträge als JSON zurück"""
        return lade_eintraege()
        
@app.post("/entries")
def post_entries(eintrag: Eintrag):
        """Schreibt einen neuen Eintrag"""
        speichere_eintrag(eintrag)
        return eintrag