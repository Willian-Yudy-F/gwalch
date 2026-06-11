# Cwymp Geiriau 🏴 — Welsh Falling Words

> A retro **80s synthwave** arcade game to learn and help keep the **Welsh
> language** (*Cymraeg*) alive. Welsh words fall from the top of the screen —
> tap the correct English translation before they hit the floor!

Built with **Python (Flask)** + **SQLite** + HTML/CSS/JavaScript.
A fun little project to practise programming with something meaningful.

> *Iechyd da!* means "Cheers / good health" in Welsh — and it's the name of
> this project's home folder. 🍻

---

## ✨ Features

- 🕹️ **80s synthwave look** — neon grid, retro sun, scanlines and glow.
- 🖼️ **Visual learning** — every word falls with a picture (emoji) of its meaning.
- 📖 **Word gallery** — study all 70+ words before you play.
- 🏆 **Leaderboard** — scores saved to a real SQLite database.
- 📈 **Levels** — the words fall faster as you score more points.
- 💎 **"Treasure" words** — famous untranslatable Welsh words like *hiraeth*,
  *cwtch* and *cynefin*, with a note explaining each one.

## 🎮 How to play

1. A Welsh word falls with a picture of its meaning.
2. Tap the correct **English translation** before it reaches the floor.
3. Right answer = points. Wrong answer or a missed word = lose a life.
4. Every 60 points you **level up** and the words speed up. 3 lives total!

## 🚀 Run it locally

You need **Python 3** installed. Then, in this folder:

```bash
# 1. Create a virtual environment (isolates dependencies)
python3 -m venv venv

# 2. Activate it
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install Flask
pip install -r requirements.txt

# 4. Create the database with the words
python3 database.py

# 5. Start the server
python3 app.py
```

Now open **http://127.0.0.1:5000** in your browser and play!
Press `Ctrl + C` in the terminal to stop the server.

## 🗂️ Project structure

| File | What it does |
|---|---|
| `app.py` | Flask web server + the API that talks to the database. |
| `database.py` | Creates the SQLite database and stores the Welsh words. |
| `templates/index.html` | The game page. |
| `static/style.css` | The 80s synthwave styling. |
| `static/game.js` | Game logic: falling words, score, lives, levels. |
| `requirements.txt` | Python dependencies. |
| `geiriau.db` | The SQLite database (auto-generated, not committed). |

## 🧠 What you practise here

- **Python**: a real web server with Flask.
- **SQL**: `CREATE TABLE`, `INSERT`, `SELECT`, `ORDER BY`, `LIMIT` — see
  `database.py` and `app.py`.
- **Front-end**: HTML Canvas, click events and animation in `static/game.js`.

## 🛣️ Roadmap / ideas to improve

This project is made to keep growing — pull requests welcome! Some ideas:

- [ ] Sound effects (correct / wrong / level up) and retro music.
- [ ] "Reverse" mode: English falls, you pick the Welsh word.
- [ ] Show the word's curiosity note when you catch a "treasure".
- [ ] Filter by category (animals, nature, colours…) or difficulty.
- [ ] Two words falling at once on higher levels.
- [ ] Add more Welsh words (and audio pronunciation!).
- [ ] Player accounts and an all-time global leaderboard.
- [ ] Deploy online (e.g. Render, Railway or Fly.io) so anyone can play.

## 🤝 Contributing

Found a bug or have an idea? Open an issue or a pull request.
Adding a word is as easy as one line in `database.py`. 🙌

## 📜 License

[MIT](LICENSE) — free to use, learn from and build on.

---

Made to practise **Python + SQL** while celebrating the Welsh language. *Diolch!* 🏴
