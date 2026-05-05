import json
from datetime import date

heute = date.today().isoformat()

try: 
    with open("entries.json", "r") as f:
        eintraege = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    eintraege = {}

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
