import json
from datetime import date, timedelta
from rich.console import Console
from rich.table import Table

heute = date.today().isoformat()

try: 
    with open("entries.json", "r") as f:
        eintraege = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    eintraege = {}

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
    if tag in eintraege:
        e = eintraege[tag]
        table.add_row(tag, e["kraftsport"], e["meditation"], e["sauna"], e["coding"] )
        print(f"{tag}: Kraftsport: {e["kraftsport"]} Meditation: {e["meditation"]} Sauna: {e["sauna"]} Coding: {e["coding"]} ")
    else:
        print(f"{tag} is not in")
        table.add_row(tag, "-", "-", "-", "-")
                      
                      
eintraege.get(tag, {})


console = Console()
console.print(table)

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

with open("entries.json", "w") as f: 
    json.dump(eintraege, f,indent=4)


print(f"Eintrag für {heute} gespeichert.")
