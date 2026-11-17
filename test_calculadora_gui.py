import unittest

from calculadora_gui import calcular


class TestCalcular(unittest.TestCase):
    def test_operacoes_basicas(self):
        self.assertEqual(calcular("8 + 4"), 12)
        self.assertEqual(calcular("8 - 4"), 4)
        self.assertEqual(calcular("8 * 4"), 32)
        self.assertEqual(calcular("8 / 4"), 2)

    def test_precedencia_e_sinais(self):
        self.assertEqual(calcular("-2 + 3 * 4"), 10)
        self.assertEqual(calcular("-(2 + 3)"), 0 - 5)

    def test_numeros_decimais(self):
        self.assertAlmostEqual(calcular("1.25 + 2.5"), 3.75)
        self.assertAlmostEqual(calcular("5.5 / 2"), 2.75)

    def test_divisao_por_zero(self):
        with self.assertRaisesRegex(ValueError, "dividir por zero"):
            calcular("10 / 0")

    def test_expressoes_invalidas_sao_rejeitadas(self):
        for expressao in ("", "2 +", "nome", "2 ** 3", "1 / (2 - 2)"):
            with self.subTest(expressao=expressao):
                with self.assertRaises(ValueError):
                    calcular(expressao)

    def test_nao_avalia_chamadas_de_funcao(self):
        with self.assertRaises(ValueError):
            calcular("__import__('os').system('echo inseguro')")


if __name__ == "__main__":
    unittest.main()
