from app.DetectMatematica import DetectMatematica
from app.DetectUtils import DetectUtils
from app.elementos import lista_original, lista_traduzida

from imageai.Detection import ObjectDetection

import os
import cv2

import numpy as np

class DetectScene(object):
    def __init__(self, imagePath):
        """
            Recebe bytes da imagem no endpoint da API e a prepara para processamento.
            Cria todas os atributos de Classe para realizar operações com os objetos identificados.
        """
        #self.imagePath = imagePath
        #self.originalImage = cv2.imread(self.imagePath)
        self.imagePath = 'imageUpload.jpg'
        self.img_np = cv2.imdecode(np.frombuffer(imagePath, np.uint8), -1) #np.fromstring(imagePath, np.uint8)
        self.img_np = cv2.cvtColor(self.img_np, cv2.COLOR_BGR2RGB)
        self.originalImage = self.img_np
        self.detections = {}
        self.objectCenter = []

        self.execution_path = os.getcwd()

        # Seta e carrega modelo resnet para detecção de objetos
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath( os.path.join(self.execution_path , "resnet50_coco_best_v2.0.1.h5"))
        self.detector.loadModel()

    def detectaObjetos(self):
        """
            Utiliza os bytes da imagem para iniciar a detecção de objetos.
            Para mais informações visitar a documentação a biblioteca em:
            https://github.com/OlafenwaMoses/ImageAI/blob/master/imageai/Detection/README.md

            Retorno: Retorna objetos identificados, informando Nome, Porcentagem e Box_Points na imagem
        """

        #detections = self.detector.detectObjectsFromImage(input_image=os.path.join(self.execution_path , self.imagePath), 
        #                                            output_image_path=os.path.join(self.execution_path , 'imageai_' + self.imagePath), 
        #                                            minimum_percentage_probability=45)

        detections = self.detector.detectObjectsFromImage(input_type="array",
                                                        input_image=self.img_np,
                                                        output_image_path=('imageai_' + self.imagePath), 
                                                        minimum_percentage_probability=45)

        self.detections = detections

        return detections

    def criaMatrizDistancia(self):
        """
            Utiliza os objetos identificados na imagem para criar matriz de distância entre eles.
            A distância é baseada na Distância Euclidiana.
        """
        matriz_distancia = []

        for i in range(len(self.detections)):
            linhaDistancia = []
            # Calcula coordenadas de centro do objeto
            ix, iy = DetectMatematica.calculaCoordenadasCentro(self.detections[i])

            nome_original = self.detections[i]['name']
            nome_traduzido = lista_traduzida[lista_original.index(nome_original)]
            # Cria lista de descrição de cada objeto
            info_object = {
                'id': i,
                'name': nome_traduzido,
                'centerCoord': (ix, iy)
            }
            self.objectCenter.append(info_object)

            # Calcula matriz de distância entre todos os objetos da cena
            for j in range(len(self.detections)):
                jx, jy = DetectMatematica.calculaCoordenadasCentro(self.detections[j])
                distancia = DetectMatematica.distanciaEuclidiana(ix, iy, jx, jy)
                linhaDistancia.append(distancia)
            matriz_distancia.append(linhaDistancia)

        # Printa no console a matriz de distância, objeto a objeto
        for index in range(len(self.detections)):
            for element in range(len(self.detections)):
                print(f"Distancia do objeto identificado {index} -> {element} : {matriz_distancia[index][element]}")

    def marcaPonto(self):
        """
            Percorre todos os objetos da imagem para marcar em cada um o ponto central que os representa.
            Desenha um círculo a fim de revelar seu centro.
            Cria nova imagem com as marcações na pasta de execução.
        """
        for eachObject in self.detections:
            x1, y1, x2, y2 = DetectMatematica.calculaBoxPoints(eachObject)

            altura_obj = y2 - y1
            largura_obj = x2 - x1

            centroX, centroY = DetectMatematica.calculaCoordenadasCentroBox(x1, y1, x2, y2)

            if (largura_obj < altura_obj):
                raio = int(0.05 * largura_obj)
            else:
                raio = int(0.05 * altura_obj)

            cv2.circle(self.originalImage, (centroX, centroY), raio, (252, 15, 192), -1)

            '''
            print(eachObject["name"] , " : ", 
                  eachObject["percentage_probability"], " : ", 
                  eachObject["box_points"])
            print(40 * "-")
            '''

        cv2.imwrite('ponto_' + self.imagePath, cv2.cvtColor(self.originalImage, cv2.COLOR_RGB2BGR))

    def marcaLinha(self):
        """
            Utiliza Matriz de Distância para desenhar linhas entre todos os objetos identificados na imagem.
            Cria nova imagem com as marcações na pasta de execução.
        """
        for i in range(len(self.detections)):
            ix, iy = DetectMatematica.calculaCoordenadasCentro(self.detections[i])
            cor1, cor2, cor3 = DetectUtils.randomize_rgb()

            cv2.putText(self.originalImage, str(i), (ix, iy - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255))

            for j in range(i, len(self.detections)):
                if (i == j):
                    continue
                jx, jy = DetectMatematica.calculaCoordenadasCentro(self.detections[j])
                cv2.line(self.originalImage, (ix, iy), (jx, jy), (cor1, cor2, cor3), 1)

        cv2.imwrite('linha_' + self.imagePath, cv2.cvtColor(self.originalImage, cv2.COLOR_RGB2BGR))

    def criaDescricaoSimples(self):
        """
            Utiliza os objetos identificados da imagem para criar uma simples descrição textual dos objetos 
            que estão contidos na imagem e suas respectivas quantidades.
        """
        lista_nomes_original = []
        for item in self.detections:
            index_nome = lista_original.index(item['name'])
            nome = lista_traduzida[index_nome] 
            lista_nomes_original.append(nome)
        
        lista_nomes_sem_repeticao = DetectUtils.remove_repetidos(lista_nomes_original)

        itens_descricao = []
        texto_descricao = 'A cena da imagem que você enviou contém: \n'
        for item in lista_nomes_sem_repeticao:
            quantidade_item = lista_nomes_original.count(item)
            itens_descricao.append((item, quantidade_item))
            if (quantidade_item != 1): 
                texto_descricao += f'{quantidade_item} {item}s \n'
            else:
                texto_descricao += f'{quantidade_item} {item} \n'

        #print(texto_descricao)

        return texto_descricao

    def criaDescricaoLocalizada(self):
        """
            Utiliza os objetos identificados e suas respectivas posições na imagem para 
            locazilá-los entre lado esquerdo, centro e lado direito do cenário da imagem enviada.
        """
        lista_nomes_original = []
        for item in self.detections:
            index_nome = lista_original.index(item['name'])
            nome = lista_traduzida[index_nome] 
            lista_nomes_original.append(nome)
        
        lista_nomes_sem_repeticao = DetectUtils.remove_repetidos(lista_nomes_original)

        itens_descricao = []
        texto_descricao = 'A cena da imagem contém: \n'
        for item in lista_nomes_sem_repeticao:
            quantidade_item = lista_nomes_original.count(item)
            itens_descricao.append((item, quantidade_item))
            if (quantidade_item != 1): 
                texto_descricao += f'{quantidade_item} {item}s, \n'
            else:
                texto_descricao += f'{quantidade_item} {item}, \n'

        texto_descricao += '.'

        height, width, channels = self.originalImage.shape
        fatia_imagem = width/3

        obj_esquerda = []
        obj_direita = []
        obj_meio = []

        itens_descricao = []
        # Separa cada objeto em sua localização na imagem baseado no eixo X do ponto central
        # Realiza contagem total de objetos
        for item in self.objectCenter:
            
            x_axis = item['centerCoord'][0]
            # Se está do lado esquerdo da imagem
            if (x_axis < fatia_imagem):
                obj_esquerda.append(item)
            # Se está no meio
            elif (x_axis > fatia_imagem and x_axis < fatia_imagem*2):
                obj_meio.append(item)
            # Se está do lado direito da imagem
            else:
                obj_direita.append(item)

        # Começa descrição total
        texto_descricao += '\n Do lado esquerdo da imagem temos: \n'
        if not obj_esquerda:
            texto_descricao += 'Nenhum objeto identificado.'
        else:
            for item in obj_esquerda:
                texto_descricao += item['name'] + ', '
            texto_descricao += '.'

        texto_descricao += '\n No centro da imagem temos: \n'
        if not obj_meio:
            texto_descricao += 'Nenhum objeto identificado.'
        else:
            for item in obj_meio:
                texto_descricao += item['name'] + ', '
            texto_descricao += '.'

        texto_descricao += '\n Do lado direito da imagem temos: \n'
        if not obj_direita:
            texto_descricao += 'Nenhum objeto identificado.'
        else:
            for item in obj_direita:
                texto_descricao += item['name'] + ', '
            texto_descricao += '.'

        return texto_descricao