# Habittracker

A small, no-frills **habit / practice tracker**. Log whether you did each of your
daily practices, see the last days at a glance, and keep your **streaks** alive.

Comes in two flavours that share the same SQLite database:

- A **web app** (FastAPI + HTMX + Pico.css) — click a button to toggle today's
  practice, and the table + streaks update live without a page reload.
- A **CLI** (Rich) — a colored terminal table plus a quick prompt to log the day.

> **Built by hand.** Every line in this project was written and reviewed by me —
> it's a learning project, not AI-generated code.

---

## Tracked practices

Out of the box it tracks four daily practices:

`meditation` · `sauna` · `kraftsport` (strength training) · `coding`

A **streak** is the number of consecutive most-recent days a practice was marked
done (`y`), counting back from the latest entry until the first miss.

---

## Tech stack

- **Language:** Python
- **Web:** FastAPI · Jinja2 · HTMX · Pico.css (no build step, no JS framework)
- **CLI:** Rich
- **Storage:** SQLite (`tracker.db`)
- **Tests:** pytest

The SQLite database (`tracker.db`) is gitignored — it stays local.

---

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# create the database schema (one-time)
python setup_db.py
```

### Run the web app

```bash
uvicorn main:app --reload
```

Then open `http://localhost:8000` — toggle today's practices with the buttons
and watch the table and streaks update live.

### Run the CLI

```bash
python tracker.py
```

Prints a colored 7-day overview, shows the current streaks, and prompts you to
log today's practices.

---

## Web API

The web app also exposes a small JSON API:

| Method   | Endpoint            | Description                                  |
| -------- | ------------------- | -------------------------------------------- |
| `GET`    | `/`                 | HTML page (table + streaks + track buttons)  |
| `GET`    | `/entries`          | List all entries as JSON                     |
| `POST`   | `/entries`          | Create / overwrite an entry for a date       |
| `PUT`    | `/entries/{datum}`  | Update the entry for a date                  |
| `DELETE` | `/entries/{datum}`  | Delete the entry for a date                  |
| `POST`   | `/track/{practice}` | Toggle a practice for today (HTMX partial)   |

An entry has the shape:

```json
{
  "datum": "2026-05-04",
  "meditation": "y",
  "sauna": "n",
  "kraftsport": "y",
  "coding": "y"
}
```

---

## Project layout

```
main.py          FastAPI web app (routes, DB access, streak logic)
tracker.py       Rich-based CLI (overview + daily prompt)
setup_db.py      Creates the SQLite schema
migrate_json.py  One-off import from a legacy entries.json into the DB
test_streak.py   pytest test for the streak calculation
templates/       Jinja2 templates (index + HTMX partials)
```

## Tests

```bash
pytest
```

---

## Status

A personal learning project, built in small steady reps — *less ambition, more
finished things*. See also [Compass](https://github.com/amorfati-dev/compass),
my dividend-growth / FIRE tracker.
