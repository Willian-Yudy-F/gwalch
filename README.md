# Cwymp Geiriau — Welsh Falling Words

[![CI](https://github.com/Willian-Yudy-F/gwalch/actions/workflows/ci.yml/badge.svg)](https://github.com/Willian-Yudy-F/gwalch/actions/workflows/ci.yml)

A small synthwave arcade game for practising beginner Welsh vocabulary. A Welsh word and emoji fall down the screen; the player chooses the matching English meaning before the word reaches the floor.

The project combines a JavaScript game loop with a Flask JSON API and a local SQLite leaderboard.

## Scope

This is a programming and vocabulary-practice project, not a complete language course. The 70+ word list was assembled for the game and has not been reviewed by a Welsh teacher or native-language editor. Some Welsh words depend on context and may have more than one English meaning.

Scores are stored locally by the Flask server. There are no player accounts, remote authentication or global leaderboard. The API validates the score range, but a determined user can still submit a fabricated in-range score because the game is calculated in the browser.

## Features

- animated Canvas game with increasing speed and three lives;
- 70+ Welsh words grouped into beginner categories;
- word gallery with emoji-based visual cues;
- Flask endpoints for words and the top ten scores;
- parameterised SQLite inserts;
- input validation and safe leaderboard rendering;
- database path configurable for local runs and tests.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python database.py
python app.py
```

Open `http://127.0.0.1:5000/`.

The database is created beside `database.py` by default. To keep it somewhere else:

```bash
export GWALCH_DB_PATH=/absolute/path/geiriau.db
python database.py
python app.py
```

`FLASK_DEBUG=1` enables Flask's development debugger. It is off by default and must never be used on a public server.

## API

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/api/palavras` | Return the vocabulary list |
| `GET` | `/api/placar` | Return the ten highest scores |
| `POST` | `/api/placar` | Save a name and integer score from 0 to 1,000,000 |

Example request:

```json
{
  "nome": "Player",
  "pontos": 120
}
```

## Project structure

```text
app.py               Flask page and API routes
database.py          SQLite schema and vocabulary seed
templates/index.html game page
static/game.js       game, API and DOM logic
static/style.css     synthwave presentation
tests/               API, database and client-safety checks
```

## Checks

```bash
python -m unittest discover -s tests -v
node --check static/game.js
```

CI runs both checks on Python 3.11 and 3.13.

## Next improvements

- have the vocabulary reviewed and attach a source or editor note to every entry;
- calculate or sign scores on the server for a trustworthy public leaderboard;
- add keyboard controls, audio pronunciation and reduced-motion game mode;
- add categories and reverse translation as selectable play modes.

Built by Willian Yudy Futema as a Python, SQL and JavaScript learning project. Licensed under [MIT](LICENSE).
