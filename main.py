from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from datetime import date

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

def loesche_eintrag(datum: str):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE datum = ?", (datum,))
    conn.commit()
    conn.close()

def errechne_streak(eintraege: list[Eintrag], practice: str) -> int:
    """Errechnet die aktuelle Streak für die gegebene Practice"""
    streak = 0
    for eintrag in sorted(eintraege, key=lambda x: x["datum"], reverse=True):
        if eintrag.get(practice) == "y":
            streak += 1
        else:
            break
    return streak

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    eintraege = lade_eintraege()
    eintraege = sorted(eintraege, key=lambda x: x["datum"], reverse=True)
    streaks = {}
    for practice in practices:
        streaks[practice] = errechne_streak(eintraege, practice)
    return templates.TemplateResponse(request, "index.html", {"eintraege": eintraege, "streaks": streaks})
    
@app.get("/entries")
def get_entries() -> list[Eintrag]:
        """Gibt die Einträge als JSON zurück"""
        return lade_eintraege()
        
@app.post("/entries")
def post_entries(eintrag: Eintrag):
        """Schreibt einen neuen Eintrag"""
        speichere_eintrag(eintrag)
        return eintrag

@app.delete("/entries/{datum}")
def delete_entries(datum: str):
    """Löscht einen Eintrag"""
    loesche_eintrag(datum)
    return {"message": "Eintrag gelöscht"}

@app.put("/entries/{datum}")
def put_entries(datum: str, eintrag: Eintrag):
    """Aktualisiert einen Eintrag"""
    eintrag.datum = datum
    speichere_eintrag(eintrag)
    return eintrag

@app.post("/track/{practice}", response_class=HTMLResponse)
def check_practice(practice : str, request: Request):
    """Trackt die Practices die heute durchgeführt wurden"""
    heute = date.today().isoformat()

    # Get the current value of the practice for today
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT erledigt FROM entries WHERE datum = ? AND practice = ?", (heute, practice))
    result = cursor.fetchone()
    current_value = result[0] if result else 0
    toggle_value = 1 if current_value == 0 else 0
    cursor.execute("INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)", (heute, practice, toggle_value))
    conn.commit()
    conn.close()

    #Aktualisierte Eintrage laden und nur Tabelle rendern
    eintraege = lade_eintraege()
    eintraege = sorted(eintraege, key=lambda x: x["datum"], reverse=True)
    streaks = {}
    for p in practices:
        streaks[p] = errechne_streak(eintraege, p)
    return templates.TemplateResponse(request, "_track_response.html", {"eintraege": eintraege, "streaks": streaks})