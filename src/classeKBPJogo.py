import os
from loguru import logger
logger.add(fr'../logInfo.log', format="{time:YY-MM-DD HH:mm:ss} | {message}", filter=lambda record: record["level"].name == "INFO", level="INFO", rotation="1 week", retention="2 week", compression="zip", enqueue=True, backtrace=True, diagnose=True, colorize=True, encoding='utf8')
logger.add(fr'../logErros.log', format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="WARNING", rotation="1 week", retention="2 week", compression="zip", enqueue=True, backtrace=True, diagnose=True, colorize=True, encoding='utf8')
import random

class JogoForca:
    def __init__(self, palavraTeste=False, tentativas=0):
        self.TELA               = ['''****************************************************************************************************************\n***                                          JOGO da PALAVRA SECRETA                                         ***\n***                                                                                                          ***\n***************************************************************************************************by-Prince****''','''****************************************************************************************************************\n***                                          JOGO da PALAVRA SECRETA                                         ***\n***                                                                                                          ***\n***                                              FIM DE JOGO                                                 ***\n***************************************************************************************************by-Prince****''']
        self.VERSAO             = '1.0.2021015'
        self.letraTentativas    = []
        self.letraAcertos       = []
        self.letraErrada      = []
        self.palpites           = 0
        if palavraTeste:
            self.palavraSorteada = random.choice(['ABC', 'BCD', 'CDE'])
        else:
            self.palavraSorteada = self.get_palavra_no_arquivo().upper()
        self.palavraOculta      = self.set_palavra_com_underscore()
        self.tentativas         = len(self.palavraSorteada) + 1
    def get_palavraSorteada(self):
        return self.palavraSorteada
    def get_palavraOculta(self):
        return self.palavraOculta
    def get_letrasTentativa(self):
        return ' '.join(self.letraTentativas)
    def get_letrasAcerto(self):
        return ' '.join(self.letraAcertos)
    def get_letrasErrada(self):
        return ' '.join(self.letraErrada)
    def get_tentativas(self):
        return self.tentativas
    def get_letra(self, letra, mostrarErro=False):
        try:
            if len(self.letraTentativas) >= self.tentativas:
                opcao = input("Você chegou no limite de tentativas:\nDigite S para Sair")
                if opcao.upper() == "S":
                    exit()
                if mostrarErro:
                    raise ValueError("Número máximo de tentativas excedido.")
            letra = str(letra).upper()
            self.letraTentativas.append(letra)
            self.palpites += 1

            if letra.upper() == self.palavraSorteada:
                self.mostrar_tela(1)
                self.mostrar_resultado(mostrarPalavraSecreta=True)
                print("\n\nParabéns você acertou a palavra\n")
                self.jogar_novamente()

            if not letra.isalpha() or len(letra) != 1:
                self.letraErrada.append(letra)
                if mostrarErro:
                    raise ValueError("Digite apenas uma letra.")
            elif letra in self.letraAcertos:
                self.letraErrada.append(letra.upper())
                if mostrarErro:
                    raise ValueError("Jogou uma letra que já havia jogado.")
            elif letra not in self.palavraSorteada:
                self.letraErrada.append(letra.upper())
                if mostrarErro:
                    raise ValueError("Jogou uma letra que já havia jogado.")
            elif letra in self.palavraSorteada:
                self.letraAcertos.append(letra.upper())
        except ValueError as e:
            logger.error(f'Erro em get_letra: {e}')
            return False
    def get_palavra_no_arquivo(self, arquivoOrigem='palavras.txt'):
        try:
            with open(arquivoOrigem, 'r', encoding='utf-8') as arquivo:
                palavras = arquivo.readlines()
            palavras = [palavra.strip() for palavra in palavras if palavra.strip()]
            if not palavras:
                raise ValueError("O arquivo está vazio ou não contém palavras válidas.")
            palavra = random.choice(palavras)
            return palavra
        except FileNotFoundError:
            return "Erro: O arquivo 'palavras.txt' não foi encontrado."
        except ValueError as ve:
            return f"Erro: {ve}"
        except Exception as e:
            return f"Erro inesperado: {e}"
    def set_palavra_com_underscore(self, palavra='', lista=[]):
        if not palavra:
            palavra = self.palavraSorteada
        if not lista:
            lista = self.letraAcertos
        palavra_com_underscore = ''.join(['_' if letra not in lista else letra for letra in palavra])
        self.palavraOculta = palavra_com_underscore
        return palavra_com_underscore
    def set_quantidadeTentativas(self, valor=2):
        try:
            if not isinstance(valor, int):
                self.tentativas = len(self.palavraSorteada) + 1
                raise ValueError("Erro: O valor deve ser um número inteiro.")
            valor = int(valor)
            if valor < 1 or valor > 9:
                self.tentativas = len(self.palavraSorteada) + 1
                raise ValueError("Erro: O valor deve estar entre 1 e 9.")
            else:
                self.tentativas = len(self.palavraSorteada) + valor
        except Exception as e:
            logger.warning(f'Valor da variavel self.tentativas permanece inalterado:::::Valor informado foi {valor}:{type(valor)}::::{e}')
    def mostrar_tela(self, tela=1):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.TELA[tela])
    def mostrar_resultado(self, mostrarPalavraSecreta=True):
        self.set_palavra_com_underscore()
        print(f'Tentativas : {len(self.letraTentativas)}/{self.tentativas}')
        if mostrarPalavraSecreta:
            print(f'Palavra sorteada    :{self.get_palavraSorteada()}')
        print(f'Palavra oculta      :{self.get_palavraOculta()}')
        print(f'Letras Acertadas    :{self.get_letrasAcerto()}')
        print(f'Letras Tentadas     :{self.get_letrasTentativa()}')
        print(f'Letras Erradas      :{self.get_letrasErrada()}')
    def inicializar_tudo(self):
        self.letraTentativas = []
        self.letraAcertos = []
        self.letraErrada = []
        self.palpites = 0
        self.palavraSorteada = self.get_palavra_no_arquivo().upper()
        self.palavraOculta = self.set_palavra_com_underscore()
        self.tentativas = len(self.palavraSorteada) + 4
    def jogar_novamente(self):
        opcao = input('Digite S para jogar novamente: ')
        if opcao.upper() == 'S':
            self.inicializar_tudo()
            self.jogarForca()

        else:
            exit()
    def jogarForca(self):
        while len(self.letraTentativas) < self.tentativas and '_' in self.set_palavra_com_underscore():
            os.system('cls' if os.name == 'nt' else 'clear')
            self.mostrar_tela(0)
            self.mostrar_resultado(mostrarPalavraSecreta=False)
            letra = input("Qual a sua letra: ")
            if not self.get_letra(letra):
                print("Tente novamente.")
        os.system('cls' if os.name == 'nt' else 'clear')
        self.mostrar_resultado()

        if '_' not in self.set_palavra_com_underscore():
            os.system('cls' if os.name == 'nt' else 'clear')
            self.mostrar_tela(1)
            self.mostrar_resultado(mostrarPalavraSecreta=True)
            print("\nParabéns! Você acertou a palavra!\n")
            self.jogar_novamente()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.mostrar_tela(1)
            self.mostrar_resultado(mostrarPalavraSecreta=True)
            print('\n\n...Você Errou...')
            self.jogar_novamente()

if __name__ == "__main__":
    jogo = JogoForca()
    jogo.jogarForca()

