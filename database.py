"""
database.py
-----------
Cria o banco de dados SQLite e enche com as palavras galesas (cymraeg).

Aqui é onde você pratica SQL! Cada função abaixo roda comandos SQL de verdade:
  - CREATE TABLE  -> cria as tabelas
  - INSERT        -> insere palavras e pontuações
  - SELECT        -> lê as palavras e o placar

Rode este arquivo sozinho uma vez para criar o banco:
    python3 database.py
"""

import sqlite3

# Nome do arquivo do banco. O SQLite guarda tudo nesse único arquivo.
DB_NAME = "geiriau.db"  # "geiriau" = "words" em galês


def get_connection():
    """Abre uma conexão com o banco. row_factory deixa a gente ler
    cada linha como um dicionário (linha["welsh"]) em vez de tupla."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# As palavras galesas. Cada tupla é:
#   (welsh, english, emoji, category, note)
# O "emoji" é a figura que mostramos no jogo, para ficar bem visual.
# "note" traz curiosidades — várias dessas palavras são raras, antigas
# ou "intraduzíveis", parte do tesouro da língua galesa.
# ---------------------------------------------------------------------------
PALAVRAS = [
    ("ci",        "dog",        "🐕", "animals",  ""),
    ("cath",      "cat",        "🐈", "animals",  ""),
    ("aderyn",    "bird",       "🐦", "animals",  ""),
    ("pysgodyn",  "fish",       "🐟", "animals",  ""),
    ("tŷ",        "house",      "🏠", "places",   ""),
    ("ysgol",     "school",     "🏫", "places",   ""),
    ("mynydd",    "mountain",   "⛰️", "nature",   ""),
    ("afon",      "river",      "🏞️", "nature",   ""),
    ("môr",       "sea",        "🌊", "nature",   ""),
    ("coeden",    "tree",       "🌳", "nature",   ""),
    ("blodyn",    "flower",     "🌸", "nature",   ""),
    ("haul",      "sun",        "☀️", "nature",   ""),
    ("lleuad",    "moon",       "🌙", "nature",   ""),
    ("seren",     "star",       "⭐", "nature",   ""),
    ("dŵr",       "water",      "💧", "food",     ""),
    ("bara",      "bread",      "🍞", "food",     ""),
    ("llaeth",    "milk",       "🥛", "food",     ""),
    ("afal",      "apple",      "🍎", "food",     ""),
    ("bwyd",      "food",       "🍽️", "food",     ""),
    ("coch",      "red",        "🔴", "colours",  ""),
    ("glas",      "blue",       "🔵", "colours",  ""),
    ("gwyrdd",    "green",      "🟢", "colours",  ""),
    ("mam",       "mother",     "👩", "family",   ""),
    ("tad",       "father",     "👨", "family",   ""),
    ("plentyn",   "child",      "🧒", "family",   ""),
    ("llyfr",     "book",       "📖", "objects",  ""),
    ("hapus",     "happy",      "😊", "feelings", ""),
    ("diolch",    "thank you",  "🙏", "phrases",  ""),
    # --- números ---
    ("un",        "one",        "1️⃣", "numbers",  ""),
    ("dau",       "two",        "2️⃣", "numbers",  ""),
    ("tri",       "three",      "3️⃣", "numbers",  ""),
    ("pedwar",    "four",       "4️⃣", "numbers",  ""),
    ("pump",      "five",       "5️⃣", "numbers",  ""),
    # --- mais animais ---
    ("ceffyl",    "horse",      "🐴", "animals",  ""),
    ("dafad",     "sheep",      "🐑", "animals",  ""),
    ("buwch",     "cow",        "🐄", "animals",  ""),
    ("mochyn",    "pig",        "🐷", "animals",  ""),
    ("llygoden",  "mouse",      "🐭", "animals",  ""),
    ("draig",     "dragon",     "🐉", "animals",  ""),
    # --- corpo ---
    ("llaw",      "hand",       "✋", "body",     ""),
    ("troed",     "foot",       "🦶", "body",     ""),
    ("llygad",    "eye",        "👁️", "body",     ""),
    ("ceg",       "mouth",      "👄", "body",     ""),
    ("calon",     "heart",      "❤️", "body",     ""),
    # --- mais natureza / clima ---
    ("eira",      "snow",       "❄️", "nature",   ""),
    ("glaw",      "rain",       "🌧️", "nature",   ""),
    ("tân",       "fire",       "🔥", "nature",   ""),
    ("gwynt",     "wind",       "💨", "nature",   ""),
    ("cwmwl",     "cloud",      "☁️", "nature",   ""),
    # --- mais comida ---
    ("caws",      "cheese",     "🧀", "food",     ""),
    ("wy",        "egg",        "🥚", "food",     ""),
    ("te",        "tea",        "🍵", "food",     ""),
    ("cacen",     "cake",       "🍰", "food",     ""),
    # --- mais cores ---
    ("du",        "black",      "⬛", "colours",  ""),
    ("gwyn",      "white",      "⬜", "colours",  ""),
    ("melyn",     "yellow",     "🟡", "colours",  ""),
    # --- objetos do dia a dia ---
    ("car",       "car",        "🚗", "objects",  ""),
    ("cadair",    "chair",      "🪑", "objects",  ""),
    ("drws",      "door",       "🚪", "objects",  ""),
    ("ffenest",   "window",     "🪟", "objects",  ""),
    ("amser",     "time",       "⏰", "objects",  ""),
    # --- descrevendo ---
    ("mawr",      "big",        "🐘", "describing", ""),
    ("bach",      "small",      "🐁", "describing", ""),
    ("poeth",     "hot",        "🥵", "describing", ""),
    ("oer",       "cold",       "🥶", "describing", ""),
    # --- mais saudações ---
    ("helo",      "hello",      "👋", "phrases",  ""),
    ("bore da",   "good morning","🌅", "phrases",  ""),
    ("nos da",    "good night", "🌃", "phrases",  ""),
    # --- palavras famosas, raras ou "intraduzíveis" ---
    ("hiraeth",   "longing",    "🌫️", "treasures",
     "Almost untranslatable — a deep longing for a home that may no longer exist."),
    ("cwtch",     "a warm hug", "🤗", "treasures",
     "A hug that also means a safe place. There is no real English equivalent."),
    ("cynefin",   "belonging",  "🏡", "treasures",
     "The place where you belong and feel at home. A very Welsh idea."),
    ("iechyd da", "cheers!",    "🍻", "phrases",
     "A Welsh toast meaning 'good health' — and the name of this folder! 🏴"),
]


def init_db():
    """Cria as tabelas e insere as palavras.
    Recria a tabela de palavras toda vez (para o esquema/dados ficarem
    sempre atualizados), mas mantém o seu placar intacto."""
    conn = get_connection()
    cur = conn.cursor()

    # Tabela das palavras — recriada para garantir o esquema novo (com emoji).
    cur.execute("DROP TABLE IF EXISTS palavras")
    cur.execute("""
        CREATE TABLE palavras (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            welsh    TEXT NOT NULL,
            english  TEXT NOT NULL,
            emoji    TEXT NOT NULL,
            category TEXT,
            note     TEXT
        )
    """)

    # Tabela do placar (high scores) — só cria se ainda não existir.
    cur.execute("""
        CREATE TABLE IF NOT EXISTS placar (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            nome   TEXT NOT NULL,
            pontos INTEGER NOT NULL,
            data   TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)

    # Insere todas as palavras.
    cur.executemany(
        "INSERT INTO palavras (welsh, english, emoji, category, note) "
        "VALUES (?, ?, ?, ?, ?)",
        PALAVRAS,
    )

    conn.commit()
    conn.close()
    print(f"Banco '{DB_NAME}' pronto com {len(PALAVRAS)} palavras galesas! 🏴")


if __name__ == "__main__":
    # Permite criar/recriar o banco rodando: python3 database.py
    init_db()
