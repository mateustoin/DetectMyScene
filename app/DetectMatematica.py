import math

class DetectMatematica(object):
    
    @staticmethod
    def distanciaEuclidiana(x1, y1, x2, y2):
        """
            Calcula distância euclidiana dado dois pontos da imagem.
        """
        dif1 = math.pow(x1 - x2, 2)
        dif2 = math.pow(y1 - y2, 2)
        distancia = math.sqrt(dif1 + dif2)

        return int(distancia)
        
    @staticmethod
    def calculaBoxPoints(objeto):
        """
            Captura e retorna de maneira organizada os pontos x1, x2, y1, e y2 de um objeto identificado.
        """
        x1 = objeto['box_points'][0]
        x2 = objeto['box_points'][2]
        y1 = objeto['box_points'][1]
        y2 = objeto['box_points'][3]

        return (x1, y1, x2, y2)

    @staticmethod
    def calculaCoordenadasCentroBox(x1, y1, x2, y2):
        """
            Baseado nos pontos do objeto, calcula seu ponto central.
        """
        centroX = int((x2 + x1) / 2)
        centroY = int((y2 + y1) / 2)

        return (centroX, centroY)

    @staticmethod
    def calculaCoordenadasCentro(objeto):
        """
            Captura os pontos x1, x2, y1 e y2 de um objeto e retorna seu ponto central.
        """
        x1 = objeto['box_points'][0]
        x2 = objeto['box_points'][2]
        y1 = objeto['box_points'][1]
        y2 = objeto['box_points'][3]

        centroX = int((x2 + x1) / 2)
        centroY = int((y2 + y1) / 2)

        return (centroX, centroY)