from imageai.Detection import ObjectDetection
import os
import cv2
import math

class DetectScene(object):
    def __init__(self):
        self.imagePath = 'example3.jpg'
        self.originalImage = cv2.imread(self.imagePath)
        self.detections = {}

        self.execution_path = os.getcwd()

        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath( os.path.join(self.execution_path , "resnet50_coco_best_v2.0.1.h5"))
        self.detector.loadModel()

    def detectaObjetos(self):
        detections = self.detector.detectObjectsFromImage(input_image=os.path.join(self.execution_path , self.imagePath), 
                                                    output_image_path=os.path.join(self.execution_path , "example3new2.jpg"), 
                                                    minimum_percentage_probability=50)

        self.detections = detections
        print(detections)
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
            
            for j in range(len(self.detections)):
                if (i == j):
                    continue
                jx, jy = self.calculaCoordenadasCentro(self.detections[j])
                cv2.line(self.originalImage, (ix, iy), (jx, jy), (255, 255, 255), 1)

        cv2.imwrite('linha_' + self.imagePath, self.originalImage)

    def distanciaEuclidiana(self, x1, y1, x2, y2):
        dif1 = math.pow(x1 - x2, 2)
        dif2 = math.pow(y1 - y2, 2)
        distancia = math.sqrt(dif1 + dif2)

        return distancia

detect = DetectScene()
detect.detectaObjetos()
detect.marcaPonto()
detect.criaMatrizDistancia()
detect.marcaLinha()