import unittest
from unittest.mock import patch, mock_open
from jogoPalavraSecreta.src.classeKBPJogo import JogoForca  # Substitua 'seu_modulo' pelo nome do seu arquivo Python

class TestJogoForca(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='palavra1\npalavra2\npalavra3\n')
    def test_get_palavra_no_arquivo(self, mock_file):
        jogo = JogoForca()
        palavra = jogo.get_palavra_no_arquivo('palavras.txt')
        self.assertIn(palavra, ['palavra1', 'palavra2', 'palavra3'])

    @patch('random.choice', return_value='ABC')
    def test_inicializacao_palavra_teste(self, mock_choice):
        jogo = JogoForca(palavraTeste=True)
        self.assertEqual(jogo.palavraSorteada, 'ABC')

    @patch('random.choice', return_value='TESTE')
    def test_inicializacao_palavra_arquivo(self, mock_choice):
        with patch('builtins.open', new_callable=mock_open, read_data='TESTE\n'):
            jogo = JogoForca()
            self.assertEqual(jogo.palavraSorteada, 'TESTE')

    def test_get_palavra_no_arquvivo_erro_não_encontrado(self):
        # Deve Retornar que o arquivo nao foi localizado
        jogo = JogoForca()
        resultado = jogo.get_palavra_no_arquivo()
        self.assertEqual(print(resultado), None)

    def test_get_letra_acerto(self):
        jogo = JogoForca(palavraTeste=True)
        jogo.palavraSorteada = 'ABC'
        jogo.get_letra('A')
        self.assertIn('A', jogo.letraAcertos)

    def test_get_letra_errada(self):
        jogo = JogoForca(palavraTeste=True)
        jogo.palavraSorteada = 'ABC'
        jogo.get_letra('D')
        self.assertIn('D', jogo.letraErrada)

    def test_get_letra_repetida(self):
        jogo = JogoForca(palavraTeste=True)
        jogo.palavraSorteada = 'ABC'
        jogo.get_letra('A')
        resultado = jogo.get_letra('A')  # Tentativa repetida
        self.assertIn('A', jogo.letraErrada)  # Deve ser considerada errada

    def test_tentativas_excedidas(self):
        jogo = JogoForca(palavraTeste=True)
        jogo.tentativas = 1  # Forçando apenas uma tentativa
        jogo.get_letra('A')  # Primeira tentativa
        with patch('builtins.input', return_value='S'):
            with self.assertRaises(SystemExit):  # Espera que o programa saia
                jogo.get_letra('B')  # Segunda tentativa

if __name__ == '__main__':
    unittest.main()