import sqlite3
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table
console = Console()

heute = date.today().isoformat()

def lade_eintraege():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    zeilen = cursor.fetchall()
    conn.close()
    
    eintraege = {}
    for datum, practice, erledigt in zeilen:
        if datum not in eintraege:
            eintraege[datum] = {}
        eintraege[datum][practice] = "y" if erledigt == 1 else "n"
    return eintraege
    
def speichere_eintraege(daten):
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    for tag, eintrag in daten.items(): 
        for practice, status in eintrag.items():
            erledigt = 1 if status == "y" else 0
            cursor.execute(
            "INSERT OR REPLACE INTO entries (datum, practice, erledigt) VALUES (?, ?, ?)",
            (tag, practice, erledigt))
    conn.commit()
    conn.close()


def zeige_uebersicht(datensatz: dict)-> None:
    table = Table(title="Habit-Tracker")
    table.add_column("Date", justify="right", style="cyan", no_wrap=True)
    table.add_column("Kraftsport", style="magenta")
    table.add_column("Meditation", justify="right", style="green")
    table.add_column("Sauna", justify="right", style="green")
    table.add_column("Coding", justify="right", style="green")

    tage = []

    for n in range(7):
        tag = date.today() - timedelta(days=n)
        tage.append(tag.isoformat())

    for tag in tage:
        if tag in datensatz:
            e = datensatz[tag]
            table.add_row(tag, e["kraftsport"], e["meditation"], e["sauna"], e["coding"] )
        else:
            table.add_row(tag, "-", "-", "-", "-")

    console.print(table)


def errechne_streak(eintraege, practice) -> int:
    streak = 0
    for tag in sorted(eintraege, reverse = True):
        if eintraege[tag][practice] == "y":
            streak +=1
        else:
            break
    return streak


eintraege = lade_eintraege()

zeige_uebersicht(eintraege)

print(errechne_streak(eintraege, "meditation"))
print(errechne_streak(eintraege, "kraftsport"))
print(errechne_streak(eintraege, "sauna"))
print(errechne_streak(eintraege, "coding"))

if heute in eintraege:
    print("Heute gibt es schon einen Eintrag.")
    exit()

print("Heute gibt es noch keinen Eintrag!")
print("Practice Tracker")
print("----------------")

meditation = input("Hast du gestern meditiert?")
kraftsport = input("Kraftsport? Y/N?")
sauna = input("Sauna? Y/N?")
coding = input("Coding?Y/N?")

print()
print(f"Du hast geantwortet:{meditation}")
print(f"Kraftsport:{kraftsport}")
print(f"Sauna:{sauna}")
print(f"Coding:{coding}")

eintraege[heute] = {
    "meditation": meditation,
    "kraftsport": kraftsport,
    "sauna": sauna,
    "coding": coding
}

speichere_eintraege(eintraege)


print(f"Eintrag für {heute} gespeichert.")
