import tempfile
import unittest
from pathlib import Path

from forca_gui import (
    ARQUIVO_PALAVRAS,
    atualizar_display,
    carregar_estatisticas,
    carregar_palavras,
    salvar_estatisticas,
    verificar_vitoria,
)


class TestForca(unittest.TestCase):
    def test_banco_tem_pelo_menos_cinquenta_palavras(self):
        palavras = carregar_palavras(ARQUIVO_PALAVRAS)
        self.assertGreaterEqual(len(palavras), 50)

    def test_todas_as_palavras_sao_validas(self):
        palavras = carregar_palavras(ARQUIVO_PALAVRAS)
        self.assertTrue(all(palavra.isalpha() and palavra.isascii() for palavra in palavras))

    def test_display_oculta_letras_nao_tentadas(self):
        self.assertEqual(atualizar_display("CASA", {"C", "A"}), "C A S A".replace("S", "_"))

    def test_display_mostra_letra_repetida(self):
        self.assertEqual(atualizar_display("BOLA", {"B", "O"}), "B O _ _")

    def test_vitoria_quando_todas_as_letras_foram_tentadas(self):
        self.assertTrue(verificar_vitoria("JAVA", {"J", "A", "V"}))
        self.assertFalse(verificar_vitoria("JAVA", {"J", "A"}))

    def test_estatisticas_sao_persistidas(self):
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "estatisticas.json"
            salvar_estatisticas(7, 3, arquivo)
            self.assertEqual(carregar_estatisticas(arquivo), (7, 3))

    def test_estatisticas_inexistentes_retorna_zero(self):
        with tempfile.TemporaryDirectory() as diretorio:
            arquivo = Path(diretorio) / "arquivo_inexistente.json"
            self.assertEqual(carregar_estatisticas(arquivo), (0, 0))


if __name__ == "__main__":
    unittest.main()
