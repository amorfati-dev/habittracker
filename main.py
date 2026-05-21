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
    entries = []
    for datum, eintrag in zwischen.items():
            eintrag["datum"] = datum
            entries.append(eintrag)
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

def toggle_practice(datum: str, practice: str):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT erledigt FROM entries WHERE datum = ? AND practice = ?", (datum, practice))
    result = cursor.fetchone()
    current_value = result[0] if result else 0
    toggle_value = 1 if current_value == 0 else 0
    cursor.execute("INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)", (datum, practice, toggle_value))
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

def errechne_alle_streaks(eintraege: list[Eintrag]) -> dict[str, int]:
    """Berechnet die Streaks für alle Practices"""
    streaks = {}
    for p in practices:
        streaks[p] = errechne_streak(eintraege, p)
    return streaks

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    eintraege = lade_eintraege()
    eintraege = sorted(eintraege, key=lambda x: x["datum"], reverse=True)
    streaks = errechne_alle_streaks(eintraege)
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
    toggle_practice(heute, practice)

    #Aktualisierte Eintrage laden und nur Tabelle rendern
    eintraege = lade_eintraege()
    eintraege = sorted(eintraege, key=lambda x: x["datum"], reverse=True)
    streaks = errechne_alle_streaks(eintraege)
    return templates.TemplateResponse(request, "_track_response.html", {"eintraege": eintraege, "streaks": streaks})