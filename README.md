# Calculadora com interface gráfica

Projeto da Tarefa 02 da disciplina INE5201: uma calculadora de operações básicas feita em Python com interface Tkinter.

## Requisitos

- Python 3.8 ou superior.
- Tkinter, incluído na instalação padrão do Python para Windows.

## Como executar

No Windows, abra o terminal na pasta do projeto e execute:

```powershell
py calculadora_gui.py
```

Use os botões da interface para formar uma expressão e pressione `=` para calcular. O ponto (`.`) insere casas decimais. O botão `←` apaga o último caractere. O botão `C` limpa o display e todo o histórico.

## Funcionalidades

- Operações de adição, subtração, multiplicação e divisão.
- Expressões com números decimais e precedência matemática.
- Validação de expressões e mensagem específica para divisão por zero.
- Histórico dos 10 cálculos mais recentes, exibidos ao lado da calculadora.
- Botões numéricos, operadores, igualdade, limpeza e backspace.

O avaliador aceita apenas números e operadores aritméticos permitidos; não executa código digitado na expressão.

## Testes

Execute os testes automatizados com:

```powershell
py -m unittest discover -v
```

## Estrutura

- `calculadora_gui.py`: avaliador aritmético, interface e loop de eventos.
- `test_calculadora_gui.py`: testes do cálculo, validação e tratamento de erros.

## Uso do GitHub Copilot

O GitHub Copilot no VS Code foi usado como assistente durante a implementação. O enunciado fornecido foi usado como prompt para organizar a interface, as operações, o histórico e o tratamento de erros. O Copilot também auxiliou na implementação do avaliador seguro de expressões e na criação dos testes automatizados. As alterações foram verificadas executando a suíte de testes do projeto.
