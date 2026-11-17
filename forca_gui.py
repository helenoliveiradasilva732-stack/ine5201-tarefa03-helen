"""Jogo da Forca com interface grafica Tkinter."""

import json
import random
import tkinter as tk
from pathlib import Path
from typing import Iterable, List, Set


MAX_ERROS = 6
ARQUIVO_PALAVRAS = Path(__file__).with_name("palavras.txt")
ARQUIVO_ESTATISTICAS = Path(__file__).with_name("estatisticas.json")


def carregar_palavras(arquivo: Path = ARQUIVO_PALAVRAS) -> List[str]:
    palavras = []
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        palavra = linha.strip().upper()
        if palavra and palavra.isalpha() and palavra.isascii():
            palavras.append(palavra)
    if not palavras:
        raise ValueError("O arquivo de palavras nao contem palavras validas")
    return palavras


def escolher_palavra(lista: Iterable[str]) -> str:
    palavras = list(lista)
    if not palavras:
        raise ValueError("A lista de palavras esta vazia")
    return random.choice(palavras).upper()


def atualizar_display(palavra: str, letras_tentadas: Set[str]) -> str:
    return " ".join(letra if letra in letras_tentadas else "_" for letra in palavra.upper())


def verificar_vitoria(palavra: str, letras_tentadas: Set[str]) -> bool:
    return all(letra in letras_tentadas for letra in palavra.upper())


def desenhar_boneco(canvas: tk.Canvas, erros: int) -> None:
    canvas.delete("all")
    canvas.create_line(40, 230, 220, 230, width=4)
    canvas.create_line(80, 230, 80, 30, width=4)
    canvas.create_line(80, 30, 180, 30, width=4)
    canvas.create_line(180, 30, 180, 55, width=4)

    if erros >= 1:
        canvas.create_oval(155, 55, 205, 105, width=4)
    if erros >= 2:
        canvas.create_line(180, 105, 180, 155, width=4)
    if erros >= 3:
        canvas.create_line(180, 120, 145, 145, width=4)
    if erros >= 4:
        canvas.create_line(180, 120, 215, 145, width=4)
    if erros >= 5:
        canvas.create_line(180, 155, 145, 195, width=4)
    if erros >= 6:
        canvas.create_line(180, 155, 215, 195, width=4)


def salvar_estatisticas(vitorias: int, derrotas: int, arquivo: Path = ARQUIVO_ESTATISTICAS) -> None:
    arquivo.write_text(
        json.dumps({"vitorias": vitorias, "derrotas": derrotas}, ensure_ascii=False),
        encoding="utf-8",
    )


def carregar_estatisticas(arquivo: Path = ARQUIVO_ESTATISTICAS) -> tuple[int, int]:
    try:
        dados = json.loads(arquivo.read_text(encoding="utf-8"))
        return int(dados.get("vitorias", 0)), int(dados.get("derrotas", 0))
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError, AttributeError):
        return 0, 0


class ForcaApp:
    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        self.palavras = carregar_palavras()
        self.palavra = ""
        self.letras_tentadas: Set[str] = set()
        self.erros = 0
        self.jogo_ativo = False
        self.dica_disponivel = True
        self.vitorias, self.derrotas = carregar_estatisticas()
        self.botoes_letras = {}
        self.criar_layout()
        self.novo_jogo()
        self.raiz.bind("<Key>", self.tratar_tecla)

    def criar_layout(self) -> None:
        self.raiz.title("Jogo da Forca")
        self.raiz.resizable(False, False)
        self.raiz.configure(padx=16, pady=16, bg="#f3f6fa")

        titulo = tk.Label(
            self.raiz,
            text="JOGO DA FORCA",
            font=("Segoe UI", 20, "bold"),
            bg="#f3f6fa",
            fg="#1f3a5f",
        )
        titulo.grid(row=0, column=0, columnspan=7, pady=(0, 10))

        self.canvas = tk.Canvas(
            self.raiz,
            width=260,
            height=250,
            bg="#ffffff",
            highlightthickness=1,
            highlightbackground="#d4dbe5",
        )
        self.canvas.grid(row=1, column=0, columnspan=3, rowspan=3, padx=(0, 12))

        painel = tk.Frame(self.raiz, bg="#f3f6fa")
        painel.grid(row=1, column=3, columnspan=4, sticky="nsew")

        self.display_palavra = tk.StringVar()
        tk.Label(
            painel,
            textvariable=self.display_palavra,
            font=("Consolas", 26, "bold"),
            bg="#f3f6fa",
            fg="#202124",
        ).pack(pady=(18, 12))

        self.restantes = tk.StringVar()
        tk.Label(
            painel,
            textvariable=self.restantes,
            font=("Segoe UI", 12),
            bg="#f3f6fa",
            fg="#d1495b",
        ).pack()

        self.tentadas = tk.StringVar()
        tk.Label(
            painel,
            textvariable=self.tentadas,
            font=("Segoe UI", 11),
            bg="#f3f6fa",
            fg="#5f6368",
        ).pack(pady=8)

        self.mensagem = tk.StringVar()
        tk.Label(
            painel,
            textvariable=self.mensagem,
            font=("Segoe UI", 12, "bold"),
            bg="#f3f6fa",
            fg="#1f3a5f",
            wraplength=300,
        ).pack(pady=(4, 12))

        linha_letras = tk.Frame(self.raiz, bg="#f3f6fa")
        linha_letras.grid(row=4, column=0, columnspan=7, pady=10)
        for indice, letra in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            linha = indice // 7
            coluna = indice % 7
            botao = tk.Button(
                linha_letras,
                text=letra,
                width=4,
                height=1,
                font=("Segoe UI", 11, "bold"),
                command=lambda l=letra: self.tentar_letra(l),
                bg="#5b8def",
                fg="white",
                activebackground="#3d73dd",
                relief="flat",
            )
            botao.grid(row=linha, column=coluna, padx=3, pady=3)
            self.botoes_letras[letra] = botao

        botoes = tk.Frame(self.raiz, bg="#f3f6fa")
        botoes.grid(row=5, column=0, columnspan=7, pady=(8, 0))
        tk.Button(
            botoes, text="Novo Jogo", command=self.novo_jogo,
            font=("Segoe UI", 11), width=12, bg="#2a9d8f", fg="white", relief="flat",
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            botoes, text="Desistir", command=self.desistir,
            font=("Segoe UI", 11), width=12, bg="#d1495b", fg="white", relief="flat",
        ).grid(row=0, column=1, padx=5)
        self.botao_dica = tk.Button(
            botoes, text="Dicas", command=self.usar_dica,
            font=("Segoe UI", 11), width=12, bg="#f4a261", fg="#202124", relief="flat",
        )
        self.botao_dica.grid(row=0, column=2, padx=5)

        self.estatisticas = tk.StringVar()
        tk.Label(
            self.raiz,
            textvariable=self.estatisticas,
            font=("Segoe UI", 10),
            bg="#f3f6fa",
            fg="#5f6368",
        ).grid(row=6, column=0, columnspan=7, pady=(10, 0))
        self.atualizar_estatisticas()

    def tratar_tecla(self, evento: tk.Event) -> None:
        letra = evento.char.upper()
        if letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            self.tentar_letra(letra)

    def novo_jogo(self) -> None:
        nova_palavra = escolher_palavra(self.palavras)
        while len(self.palavras) > 1 and nova_palavra == self.palavra:
            nova_palavra = escolher_palavra(self.palavras)
        self.palavra = nova_palavra
        self.letras_tentadas = set()
        self.erros = 0
        self.jogo_ativo = True
        self.dica_disponivel = True
        self.botao_dica.config(state="normal")
        for botao in self.botoes_letras.values():
            botao.config(state="normal", bg="#5b8def")
        self.atualizar_interface()
        self.mensagem.set("Escolha uma letra")

    def tentar_letra(self, letra: str) -> None:
        if not self.jogo_ativo:
            return
        letra = letra.upper()
        if letra in self.letras_tentadas:
            self.mensagem.set("Esta letra ja foi tentada")
            return

        self.letras_tentadas.add(letra)
        self.botoes_letras[letra].config(state="disabled", bg="#b7bdc6")
        if letra not in self.palavra:
            self.erros += 1
            self.mensagem.set("Letra nao encontrada")
        else:
            self.mensagem.set("Boa! Letra encontrada")
        self.verificar_fim()
        self.atualizar_interface()

    def usar_dica(self) -> None:
        if not self.jogo_ativo or not self.dica_disponivel:
            return
        letras_restantes = [
            letra for letra in set(self.palavra)
            if letra not in self.letras_tentadas
        ]
        if not letras_restantes:
            return
        letra = random.choice(letras_restantes)
        self.dica_disponivel = False
        self.botao_dica.config(state="disabled")
        self.letras_tentadas.add(letra)
        self.botoes_letras[letra].config(state="disabled", bg="#f4a261")
        self.mensagem.set("Dica: revelada a letra " + letra)
        self.verificar_fim()
        self.atualizar_interface()

    def verificar_fim(self) -> None:
        if verificar_vitoria(self.palavra, self.letras_tentadas):
            self.encerrar(True)
        elif self.erros >= MAX_ERROS:
            self.encerrar(False)

    def encerrar(self, venceu: bool) -> None:
        if not self.jogo_ativo:
            return
        self.jogo_ativo = False
        if venceu:
            self.vitorias += 1
            self.mensagem.set("Voce venceu!")
        else:
            self.derrotas += 1
            self.mensagem.set("Voce perdeu! Palavra: " + self.palavra)
        salvar_estatisticas(self.vitorias, self.derrotas)
        self.atualizar_estatisticas()
        self.botao_dica.config(state="disabled")
        for botao in self.botoes_letras.values():
            botao.config(state="disabled")

    def desistir(self) -> None:
        if self.jogo_ativo:
            self.encerrar(False)
            self.atualizar_interface()

    def atualizar_interface(self) -> None:
        self.display_palavra.set(atualizar_display(self.palavra, self.letras_tentadas))
        restantes = MAX_ERROS - self.erros
        self.restantes.set("Tentativas restantes: " + str(restantes))
        letras = " ".join(sorted(self.letras_tentadas)) or "-"
        self.tentadas.set("Letras tentadas: " + letras)
        desenhar_boneco(self.canvas, self.erros)

    def atualizar_estatisticas(self) -> None:
        self.estatisticas.set(
            "Vitorias: {} | Derrotas: {}".format(self.vitorias, self.derrotas)
        )


def main() -> None:
    raiz = tk.Tk()
    ForcaApp(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
