from gtts import gTTS
from random import randint

class DetectUtils(object):
    
    @staticmethod
    def remove_repetidos(lista):
        """
            Remove elementos repetidos de uma lista.
        """
        l = []
        for i in lista:
            if i not in l:
                l.append(i)
        l.sort()
        return l

    @staticmethod
    def criaAudio(texto, nome):
        """
            Utiliza um texto de entrada e nome para criação do arquivo, a fim de 
            transformar o texto em áudio, utilizando ferramentas do google text to speech.
        """
        print('Criando áudio...')
        tts = gTTS(text=texto, lang='pt-br')
        tts.save(nome + '_descricao.mp3')
        print('Audio criado!')

    @staticmethod 
    def randomize_rgb():
        """
            Cria uma cor RGB aleatória. Retorna tupla com 3 inteiros de 0 a 255.
        """
        cor1 = randint(0, 255)
        cor2 = randint(0, 255)
        cor3 = randint(0, 255)

        return (cor1, cor2, cor3)