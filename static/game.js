/*
 * game.js — logic for "Cwymp Geiriau" (Welsh Falling Words).
 *
 * How it works:
 *   1. We fetch the words from the Python server (route /api/palavras).
 *   2. A Welsh word (with a picture/emoji of its meaning) falls down.
 *   3. Four English translations appear as buttons; tap the correct one.
 *      - Correct  -> gain points, next word falls.
 *      - Wrong OR the word reaches the floor -> lose a life.
 *   4. The game speeds up as you level up. 3 lives and it's over.
 *
 * (Comments are in Portuguese — the player/learner's own notes.)
 */

// ---- Elementos da página ----
const canvas   = document.getElementById("tela");
const ctx      = canvas.getContext("2d");
const elPontos = document.getElementById("pontos");
const elNivel  = document.getElementById("nivel");
const elVidas  = document.getElementById("vidas");
const elOpcoes = document.getElementById("opcoes");
const overlay  = document.getElementById("overlay");
const overlayTitulo = document.getElementById("overlay-titulo");
const instrucoes    = document.getElementById("instrucoes");
const btnComecar    = document.getElementById("btn-comecar");
const btnGaleria    = document.getElementById("btn-galeria");
const salvarArea    = document.getElementById("salvar-area");
const campoNome     = document.getElementById("campo-nome");
const btnSalvar     = document.getElementById("btn-salvar");
const galeria       = document.getElementById("galeria");

// Dimensões "lógicas" do canvas (o CSS estica para preencher a tela).
const L = canvas.width;   // 500
const A = canvas.height;  // 520

// ---- Estado do jogo ----
let palavras = [];
let atual = null;       // a palavra que está caindo agora
let y = 0;              // posição vertical da palavra que cai
let velocidade = 0.8;   // pixels por quadro (aumenta com o nível) — devagar = mais tempo
let pontos = 0;
let nivel = 1;
let vidas = 3;
let rodando = false;
let animacaoId = null;
let pulso = 0;          // brilho pulsante do bloco que cai

// Busca as palavras no servidor.
async function carregarPalavras() {
    const resp = await fetch("/api/palavras");
    palavras = await resp.json();
}

function aleatorio(lista) {
    return lista[Math.floor(Math.random() * lista.length)];
}

// Embaralha uma lista (Fisher–Yates).
function embaralhar(lista) {
    const copia = [...lista];
    for (let i = copia.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [copia[i], copia[j]] = [copia[j], copia[i]];
    }
    return copia;
}

// Prepara uma nova palavra e monta os botões de tradução em inglês.
function proximaPalavra() {
    atual = aleatorio(palavras);
    y = -80; // começa acima do topo

    const erradas = embaralhar(palavras.filter(p => p.english !== atual.english))
        .slice(0, 3)
        .map(p => p.english);
    const opcoes = embaralhar([atual.english, ...erradas]);

    elOpcoes.innerHTML = "";
    opcoes.forEach(textoEn => {
        const btn = document.createElement("button");
        btn.className = "opcao";
        btn.textContent = textoEn;
        btn.onclick = () => responder(textoEn, btn);
        elOpcoes.appendChild(btn);
    });
}

// Quando o jogador clica numa tradução.
function responder(textoEn, botao) {
    if (!rodando || !atual) return;

    if (textoEn === atual.english) {
        const bonus = Math.round((Math.max(y, 0) / A) * 10);
        pontos += 10 * nivel + bonus;
        botao.classList.add("certo");
        atualizarHud();
        subirDeNivel();
        proximaPalavra();
    } else {
        botao.classList.add("errado");
        setTimeout(() => botao.classList.remove("errado"), 350);
        perderVida();
    }
}

function subirDeNivel() {
    const novoNivel = 1 + Math.floor(pontos / 60);
    if (novoNivel > nivel) {
        nivel = novoNivel;
        velocidade += 0.2;   // acelera devagar, dá tempo de reagir
        atualizarHud();
    }
}

function perderVida() {
    vidas--;
    atualizarHud();
    if (vidas <= 0) {
        fimDeJogo();
    } else {
        proximaPalavra();
    }
}

function atualizarHud() {
    elPontos.textContent = pontos;
    elNivel.textContent = nivel;
    elVidas.textContent = "❤️".repeat(vidas) || "💀";
}

// Retângulo de cantos arredondados (compatível com navegadores antigos).
function blocoArredondado(x, y, largura, altura, raio) {
    ctx.beginPath();
    ctx.moveTo(x + raio, y);
    ctx.arcTo(x + largura, y, x + largura, y + altura, raio);
    ctx.arcTo(x + largura, y + altura, x, y + altura, raio);
    ctx.arcTo(x, y + altura, x, y, raio);
    ctx.arcTo(x, y, x + largura, y, raio);
    ctx.closePath();
}

// O "coração" do jogo: ~60x por segundo, desenha tudo.
function loop() {
    ctx.clearRect(0, 0, L, A);

    // Linha do "chão" (zona de perigo) — neon rosa pulsante.
    ctx.save();
    ctx.shadowColor = "#ff2e97";
    ctx.shadowBlur = 14;
    ctx.strokeStyle = "#ff2e97";
    ctx.lineWidth = 2.5;
    ctx.setLineDash([12, 10]);
    ctx.beginPath();
    ctx.moveTo(0, A - 6);
    ctx.lineTo(L, A - 6);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();

    if (atual) {
        y += velocidade;
        pulso += 0.12;

        const altura = 100;
        ctx.font = "bold 26px 'Orbitron', sans-serif";
        const textoLargura = ctx.measureText(atual.welsh).width;
        const largura = Math.max(200, textoLargura + 64);
        const x = L / 2 - largura / 2;

        // Cor neon: alterna ciano / rosa por palavra.
        const neon = (atual.welsh.length % 2 === 0) ? "#00f0ff" : "#ff2e97";
        const brilho = 12 + 10 * Math.abs(Math.sin(pulso));

        // Fundo escuro translúcido do bloco.
        ctx.save();
        blocoArredondado(x, y, largura, altura, 14);
        ctx.fillStyle = "rgba(13, 2, 33, 0.82)";
        ctx.fill();
        ctx.restore();

        // Borda neon com brilho (glow).
        ctx.save();
        ctx.shadowColor = neon;
        ctx.shadowBlur = brilho;
        ctx.strokeStyle = neon;
        ctx.lineWidth = 2.5;
        blocoArredondado(x, y, largura, altura, 14);
        ctx.stroke();
        ctx.restore();

        // A figura (emoji) — a parte bem visual.
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.font = "42px 'Segoe UI Emoji', 'Apple Color Emoji', sans-serif";
        ctx.fillText(atual.emoji, L / 2, y + 34);

        // A palavra galesa com brilho neon.
        ctx.save();
        ctx.shadowColor = neon;
        ctx.shadowBlur = brilho;
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 26px 'Orbitron', sans-serif";
        ctx.fillText(atual.welsh, L / 2, y + 76);
        ctx.restore();

        // Bateu no chão?
        if (y + altura >= A - 6) {
            perderVida();
        }
    }

    if (rodando) {
        animacaoId = requestAnimationFrame(loop);
    }
}

// Começa uma partida do zero.
function iniciar() {
    pontos = 0;
    nivel = 1;
    vidas = 3;
    velocidade = 0.8;
    rodando = true;
    atualizarHud();
    overlay.classList.add("escondido");
    salvarArea.classList.add("escondido");
    proximaPalavra();
    loop();
}

// Fim de jogo: para tudo e mostra a tela final com campo de nome.
function fimDeJogo() {
    rodando = false;
    cancelAnimationFrame(animacaoId);
    atual = null;
    ctx.clearRect(0, 0, L, A);

    overlayTitulo.textContent = "Game over!";
    instrucoes.classList.add("escondido");
    btnGaleria.classList.add("escondido");

    // Remove uma mensagem anterior (se o jogador já jogou antes) e cria a nova.
    const antiga = document.getElementById("resultado-msg");
    if (antiga) antiga.remove();
    overlayTitulo.insertAdjacentHTML("afterend",
        `<p id="resultado-msg">You scored <b>${pontos}</b> points at level <b>${nivel}</b>. 👏<br>` +
        `Save your name to the leaderboard and try again!</p>`);

    btnSalvar.disabled = false;
    btnSalvar.textContent = "Save score";
    salvarArea.classList.remove("escondido");

    btnComecar.innerHTML = "Play again · <em>Eto!</em>";
    overlay.classList.remove("escondido");
}

// Salva a pontuação no servidor (SQL: INSERT) e recarrega o placar.
async function salvarPontuacao() {
    const nome = (campoNome.value || "Anonymous").trim() || "Anonymous";
    btnSalvar.disabled = true;
    btnSalvar.textContent = "Saving...";
    await fetch("/api/placar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nome: nome, pontos: pontos }),
    });
    btnSalvar.textContent = "Saved! ✅";
    await carregarPlacar();
}

// Mostra/esconde a galeria rolando até ela.
function irParaGaleria() {
    document.getElementById("galeria-secao").scrollIntoView({ behavior: "smooth" });
}

// Busca o placar e mostra na lista.
async function carregarPlacar() {
    const resp = await fetch("/api/placar");
    const lista = await resp.json();
    const ol = document.getElementById("placar");
    ol.innerHTML = "";
    if (lista.length === 0) {
        ol.innerHTML = "<li>No scores yet. Be the first! 🏆</li>";
        return;
    }
    const medalhas = ["🥇", "🥈", "🥉"];
    lista.forEach((item, i) => {
        const li = document.createElement("li");
        const marca = medalhas[i] || `${i + 1}.`;
        li.innerHTML =
            `<span><span class="pos">${marca}</span>${item.nome}</span>` +
            `<span class="pts">${item.pontos}</span>`;
        ol.appendChild(li);
    });
}

// Monta a galeria visual com todas as palavras (figura + galês + inglês).
function montarGaleria() {
    galeria.innerHTML = "";
    palavras.forEach(p => {
        const card = document.createElement("div");
        card.className = "card-palavra" + (p.category === "treasures" ? " tesouro" : "");
        card.innerHTML =
            `<div class="card-emoji">${p.emoji}</div>` +
            `<div class="card-welsh">${p.welsh}</div>` +
            `<div class="card-en">${p.english}</div>` +
            (p.note ? `<div class="card-nota">${p.note}</div>` : "");
        galeria.appendChild(card);
    });
}

// ---- Liga os botões ----
btnComecar.onclick = iniciar;
btnSalvar.onclick = salvarPontuacao;
btnGaleria.onclick = irParaGaleria;
campoNome.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !btnSalvar.disabled) salvarPontuacao();
});

// Ao abrir a página: carrega palavras, placar e monta a galeria.
(async function () {
    await carregarPalavras();
    await carregarPlacar();
    montarGaleria();
})();
