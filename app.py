"""
app.py
------
O servidor web do jogo, feito com Flask (Python).

Ele faz duas coisas:
  1. Serve a página do jogo (o HTML/CSS/JS).
  2. Oferece uma "API": endereços que devolvem dados em JSON, lendo/gravando
     no banco SQLite. É aqui que o Python conversa com o SQL.

Endereços (rotas):
  GET  /              -> a página do jogo
  GET  /api/palavras  -> todas as palavras galesas (em JSON)
  GET  /api/placar    -> os 10 melhores resultados
  POST /api/placar    -> salva um novo resultado

Para rodar:
    python3 app.py
e abra http://127.0.0.1:5000 no navegador.
"""

from flask import Flask, jsonify, request, render_template
from database import get_connection, init_db
import os
import unicodedata

app = Flask(__name__)


@app.after_request
def add_security_headers(response):
    """Add small, sensible defaults for this local learning app."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    return response


@app.route("/")
def index():
    """Mostra a página principal do jogo."""
    return render_template("index.html")


@app.route("/api/palavras")
def api_palavras():
    """Devolve TODAS as palavras como JSON.
    SQL usado aqui: SELECT (ler do banco)."""
    conn = get_connection()
    linhas = conn.execute(
        "SELECT welsh, english, emoji, category, note FROM palavras"
    ).fetchall()
    conn.close()
    # Transforma cada linha do banco em um dicionário simples.
    palavras = [dict(linha) for linha in linhas]
    return jsonify(palavras)


@app.route("/api/placar", methods=["GET"])
def get_placar():
    """Devolve os 10 maiores resultados, do maior para o menor.
    SQL: SELECT ... ORDER BY ... LIMIT."""
    conn = get_connection()
    linhas = conn.execute(
        "SELECT nome, pontos, data FROM placar ORDER BY pontos DESC LIMIT 10"
    ).fetchall()
    conn.close()
    return jsonify([dict(linha) for linha in linhas])


@app.route("/api/placar", methods=["POST"])
def salvar_placar():
    """Salva um novo resultado no placar.
    Recebe um JSON do navegador: {"nome": "...", "pontos": 123}
    SQL: INSERT (gravar no banco)."""
    dados = request.get_json(silent=True) or {}
    nome_recebido = dados.get("nome", "Anonymous")
    pontos = dados.get("pontos")

    if not isinstance(nome_recebido, str):
        return jsonify({"error": "Name must be text."}), 400
    if not isinstance(pontos, int) or isinstance(pontos, bool):
        return jsonify({"error": "Score must be an integer."}), 400
    if pontos < 0 or pontos > 1_000_000:
        return jsonify({"error": "Score is outside the accepted range."}), 400

    nome = "".join(
        char for char in nome_recebido.strip()
        if not unicodedata.category(char).startswith("C")
    )[:20] or "Anonymous"

    conn = get_connection()
    conn.execute(
        "INSERT INTO placar (nome, pontos) VALUES (?, ?)",
        (nome, pontos),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


if __name__ == "__main__":
    init_db()
    app.run(
        debug=os.getenv("FLASK_DEBUG") == "1",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
    )
