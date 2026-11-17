# Jogo da Forca

Projeto da Tarefa 03 da disciplina INE5201. O programa implementa o jogo da forca em Python com interface grafica Tkinter.

## Requisitos

- Python 3.8 ou superior
- Tkinter, incluido na instalacao padrao do Python

No Windows, execute:

```powershell
py forca_gui.py
```

## Funcionalidades

- Palavra aleatoria carregada de `palavras.txt`
- Banco com mais de 50 palavras
- Display com letras ocultas
- Teclado virtual com letras A-Z
- Teclado fisico tambem aceita letras
- Boneco visual com seis partes
- Contador de tentativas restantes
- Validacao de letras ja tentadas
- Mensagens de vitoria e derrota
- Botoes Novo Jogo, Desistir e Dicas
- Uma dica por partida, revelando uma letra nao tentada
- Estatisticas persistentes de vitorias e derrotas em `estatisticas.json`

## Regras

Cada letra correta permanece revelada no display. Cada letra incorreta adiciona uma parte ao boneco. O jogo termina quando todas as letras sao descobertas ou seis erros sao atingidos.

## Estrutura

- `forca_gui.py`: funcoes do jogo, interface grafica e loop de eventos
- `palavras.txt`: banco de palavras utilizado nas partidas
- `test_forca_gui.py`: testes das regras, do display e das estatisticas
- `estatisticas.json`: arquivo criado automaticamente ao encerrar uma partida

## Testes

Execute:

```powershell
py -m unittest discover -v
```

## Uso do GitHub Copilot

O GitHub Copilot no VS Code foi utilizado como assistente para organizar a interface, implementar as funcoes principais, criar o banco de palavras, escrever os testes e revisar o README. A implementacao foi validada por testes automatizados.
