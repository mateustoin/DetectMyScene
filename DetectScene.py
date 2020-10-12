from imageai.Detection import ObjectDetection
import os
import cv2
import math
from gtts import gTTS
from elementos import lista_original, lista_traduzida

from random import randint

class DetectScene(object):
    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.originalImage = cv2.imread(self.imagePath)
        self.detections = {}

        self.execution_path = os.getcwd()

        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath( os.path.join(self.execution_path , "resnet50_coco_best_v2.0.1.h5"))
        self.detector.loadModel()

    def detectaObjetos(self):
        detections = self.detector.detectObjectsFromImage(input_image=os.path.join(self.execution_path , self.imagePath), 
                                                    output_image_path=os.path.join(self.execution_path , 'imageai_' + self.imagePath), 
                                                    minimum_percentage_probability=45)

        self.detections = detections

        return detections

    def criaMatrizDistancia(self):
        matriz_distancia = []

        for i in range(len(self.detections)):
            linhaDistancia = []
            ix, iy = self.calculaCoordenadasCentro(self.detections[i])
            
            for j in range(len(self.detections)):
                jx, jy = self.calculaCoordenadasCentro(self.detections[j])
                distancia = self.distanciaEuclidiana(ix, iy, jx, jy)
                linhaDistancia.append(distancia)
            matriz_distancia.append(linhaDistancia)

        for index in range(len(self.detections)):
            for element in range(len(self.detections)):
                print(f"Distancia do objeto identificado {index} -> {element} : {matriz_distancia[index][element]}")

    def calculaBoxPoints(self, objeto):
        x1 = objeto['box_points'][0]
        x2 = objeto['box_points'][2]
        y1 = objeto['box_points'][1]
        y2 = objeto['box_points'][3]

        return (x1, y1, x2, y2)

    def calculaCoordenadasCentroBox(self, x1, y1, x2, y2):
        centroX = int((x2 + x1) / 2)
        centroY = int((y2 + y1) / 2)

        return (centroX, centroY)

    def calculaCoordenadasCentro(self, objeto):
        x1 = objeto['box_points'][0]
        x2 = objeto['box_points'][2]
        y1 = objeto['box_points'][1]
        y2 = objeto['box_points'][3]

        centroX = int((x2 + x1) / 2)
        centroY = int((y2 + y1) / 2)

        return (centroX, centroY)
    
    def marcaPonto(self):
        for eachObject in self.detections:
            x1, y1, x2, y2 = self.calculaBoxPoints(eachObject)

            altura_obj = y2 - y1
            largura_obj = x2 - x1

            centroX, centroY = self.calculaCoordenadasCentroBox(x1, y1, x2, y2)

            if (largura_obj < altura_obj):
                raio = int(0.05 * largura_obj)
            else:
                raio = int(0.05 * altura_obj)

            cv2.circle(self.originalImage, (centroX, centroY), raio, (252, 15, 192), -1)

            print(eachObject["name"] , " : ", 
                  eachObject["percentage_probability"], " : ", 
                  eachObject["box_points"])
            print(40 * "-")

        cv2.imwrite('ponto_' + self.imagePath, self.originalImage)

    def marcaLinha(self):
        for i in range(len(self.detections)):
            ix, iy = self.calculaCoordenadasCentro(self.detections[i])
            cor1 = randint(0, 255)
            cor2 = randint(0, 255)
            cor3 = randint(0, 255)

            cv2.putText(self.originalImage, str(i), (ix, iy - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255))

            for j in range(i, len(self.detections)):
                if (i == j):
                    continue
                jx, jy = self.calculaCoordenadasCentro(self.detections[j])
                cv2.line(self.originalImage, (ix, iy), (jx, jy), (cor1, cor2, cor3), 1)

        cv2.imwrite('linha_' + self.imagePath, self.originalImage)

    def criaDescricaoSimples(self):
        lista_nomes_original = []
        for item in self.detections:
            index_nome = lista_original.index(item['name'])
            nome = lista_traduzida[index_nome] 
            lista_nomes_original.append(nome)
        
        lista_nomes_sem_repeticao = self.remove_repetidos(lista_nomes_original)

        itens_descricao = []
        texto_descricao = 'A cena da imagem que você enviou contém: \n'
        for item in lista_nomes_sem_repeticao:
            quantidade_item = lista_nomes_original.count(item)
            itens_descricao.append((item, quantidade_item))
            if (quantidade_item != 1): 
                texto_descricao += f'{quantidade_item} {item}s \n'
            else:
                texto_descricao += f'{quantidade_item} {item} \n'

        print(texto_descricao)

        return texto_descricao

    def criaAudio(self, texto):
        print('Criando áudio...')
        tts = gTTS(texto, lang='pt-br')
        tts.save('descricao.mp3')
        print('Audio criado!')

    def remove_repetidos(self, lista):
        l = []
        for i in lista:
            if i not in l:
                l.append(i)
        l.sort()
        return l

    def distanciaEuclidiana(self, x1, y1, x2, y2):
        dif1 = math.pow(x1 - x2, 2)
        dif2 = math.pow(y1 - y2, 2)
        distancia = math.sqrt(dif1 + dif2)

        return int(distancia)

detect = DetectScene('example3.jpg')
detect.detectaObjetos()
detect.marcaPonto()
detect.criaMatrizDistancia()
detect.marcaLinha()
detect.criaAudio(detect.criaDescricaoSimples())