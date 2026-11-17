"""Calculadora de operações básicas com interface gráfica."""

import ast
import math
import operator
import tkinter as tk
from typing import List, Union


Numero = Union[int, float]
OPERADORES_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
OPERADORES_UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _avaliar_no(no: ast.AST) -> Numero:
    if isinstance(no, ast.Expression):
        return _avaliar_no(no.body)
    if isinstance(no, ast.Constant) and type(no.value) in (int, float):
        if isinstance(no.value, float) and not math.isfinite(no.value):
            raise ValueError("Número inválido")
        return no.value
    if isinstance(no, ast.BinOp) and type(no.op) in OPERADORES_BINARIOS:
        esquerda = _avaliar_no(no.left)
        direita = _avaliar_no(no.right)
        if isinstance(no.op, ast.Div) and direita == 0:
            raise ValueError("Não é possível dividir por zero")
        return OPERADORES_BINARIOS[type(no.op)](esquerda, direita)
    if isinstance(no, ast.UnaryOp) and type(no.op) in OPERADORES_UNARIOS:
        return OPERADORES_UNARIOS[type(no.op)](_avaliar_no(no.operand))
    raise ValueError("Expressão inválida")


def calcular(expressao: str) -> Numero:
    """Calcula uma expressão usando apenas +, -, * e /."""
    try:
        arvore = ast.parse(expressao, mode="eval")
        resultado = _avaliar_no(arvore)
    except (SyntaxError, OverflowError) as erro:
        raise ValueError("Expressão inválida") from erro
    if isinstance(resultado, float) and not math.isfinite(resultado):
        raise ValueError("Resultado inválido")
    return resultado


def _formatar_resultado(resultado: Numero) -> str:
    if isinstance(resultado, float):
        return format(resultado, ".12g")
    return str(resultado)


class CalculadoraApp:
    """Janela e eventos da calculadora."""

    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        self.display = tk.StringVar()
        self._erro_exibido = False
        self._resultado_exibido = False
        self.historico: List[str] = []
        self.criar_layout()

    def criar_layout(self) -> None:
        self.raiz.title("Calculadora")
        self.raiz.resizable(False, False)
        self.raiz.configure(padx=12, pady=12, bg="#202124")

        self.entrada = tk.Entry(
            self.raiz,
            textvariable=self.display,
            justify="right",
            font=("Segoe UI", 24),
            width=18,
            bd=0,
            relief="flat",
            state="readonly",
            readonlybackground="#303134",
            fg="#f1f3f4",
        )
        self.entrada.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 10), ipady=12)

        botoes = [
            ("C", 1, 0, self.limpar),
            ("←", 1, 1, self.apagar_ultimo),
            ("/", 1, 2, lambda: self.adicionar_caractere("/")),
            ("*", 1, 3, lambda: self.adicionar_caractere("*")),
            ("7", 2, 0, lambda: self.adicionar_caractere("7")),
            ("8", 2, 1, lambda: self.adicionar_caractere("8")),
            ("9", 2, 2, lambda: self.adicionar_caractere("9")),
            ("-", 2, 3, lambda: self.adicionar_caractere("-")),
            ("4", 3, 0, lambda: self.adicionar_caractere("4")),
            ("5", 3, 1, lambda: self.adicionar_caractere("5")),
            ("6", 3, 2, lambda: self.adicionar_caractere("6")),
            ("+", 3, 3, lambda: self.adicionar_caractere("+")),
            ("1", 4, 0, lambda: self.adicionar_caractere("1")),
            ("2", 4, 1, lambda: self.adicionar_caractere("2")),
            ("3", 4, 2, lambda: self.adicionar_caractere("3")),
            ("=", 4, 3, self.calcular_display),
            ("0", 5, 0, lambda: self.adicionar_caractere("0")),
            (".", 5, 2, lambda: self.adicionar_caractere(".")),
        ]
        for texto, linha, coluna, comando in botoes:
            destaque = texto in {"+", "-", "*", "/", "="}
            botao = tk.Button(
                self.raiz,
                text=texto,
                command=comando,
                font=("Segoe UI", 16),
                width=4,
                height=2,
                bd=0,
                relief="flat",
                bg="#8ab4f8" if destaque else "#3c4043",
                fg="#202124" if destaque else "#f1f3f4",
                activebackground="#aecbfa" if destaque else "#5f6368",
                activeforeground="#202124" if destaque else "#f1f3f4",
            )
            colspan = 2 if texto == "0" else 1
            botao.grid(row=linha, column=coluna, columnspan=colspan, sticky="nsew", padx=3, pady=3)

        painel_historico = tk.LabelFrame(
            self.raiz,
            text="Histórico recente",
            font=("Segoe UI", 10),
            bg="#202124",
            fg="#f1f3f4",
            padx=8,
            pady=8,
        )
        painel_historico.grid(row=0, column=4, rowspan=6, sticky="nsew", padx=(10, 0))
        self.lista_historico = tk.Listbox(
            painel_historico,
            width=28,
            height=16,
            font=("Segoe UI", 10),
            bd=0,
            bg="#303134",
            fg="#f1f3f4",
            selectbackground="#5f6368",
        )
        self.lista_historico.pack(fill="both", expand=True)

    def atualizar_display(self, valor: str) -> None:
        self.display.set(valor)

    def tratar_erro(self, mensagem: str) -> None:
        self.atualizar_display("Erro: " + mensagem)
        self._erro_exibido = True
        self._resultado_exibido = False

    def adicionar_caractere(self, caractere: str) -> None:
        texto = self.display.get()
        if self._erro_exibido or (self._resultado_exibido and caractere.isdigit()):
            texto = ""
        elif self._resultado_exibido and caractere == ".":
            texto = ""
        self.atualizar_display(texto + caractere)
        self._erro_exibido = False
        self._resultado_exibido = False

    def apagar_ultimo(self) -> None:
        if self._erro_exibido:
            self.limpar()
            return
        self.atualizar_display(self.display.get()[:-1])
        self._resultado_exibido = False

    def limpar(self) -> None:
        self.atualizar_display("")
        self.historico.clear()
        self.lista_historico.delete(0, tk.END)
        self._erro_exibido = False
        self._resultado_exibido = False

    def adicionar_ao_historico(self, expressao: str, resultado: Numero) -> None:
        registro = "{} = {}".format(expressao, _formatar_resultado(resultado))
        self.historico.insert(0, registro)
        del self.historico[10:]
        self.lista_historico.delete(0, tk.END)
        for item in self.historico:
            self.lista_historico.insert(tk.END, item)

    def calcular_display(self) -> None:
        expressao = self.display.get()
        try:
            resultado = calcular(expressao)
        except ValueError as erro:
            self.tratar_erro(str(erro))
            return
        self.adicionar_ao_historico(expressao, resultado)
        self.atualizar_display(_formatar_resultado(resultado))
        self._resultado_exibido = True


def main() -> None:
    raiz = tk.Tk()
    CalculadoraApp(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
