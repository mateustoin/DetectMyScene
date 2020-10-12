from imageai.Detection import ObjectDetection
import os
import cv2

image = "example3.jpg"

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , image), 
                                             output_image_path=os.path.join(execution_path , "example3new2.jpg"), 
                                             minimum_percentage_probability=40,
                                             display_percentage_probability=False,
                                             display_object_name=False)

img = cv2.imread(image)

for eachObject in detections:
    x1 = eachObject['box_points'][0]
    x2 = eachObject['box_points'][2]
    y1 = eachObject['box_points'][1]
    y2 = eachObject['box_points'][3]

    altura_obj = y2 - y1
    largura_obj = x2 - x1
    raio = 5

    centroX = int((x2 + x1) / 2)
    centroY = int((y2 + y1) / 2)

    if (largura_obj < altura_obj):
        raio = int(0.05 * largura_obj)
    else:
        raio = int(0.05 * altura_obj)

    cv2.circle(img, (centroX, centroY), raio, (252, 15, 192), -1)

    print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"], 
          "X1: ", x1, "X2: ", x2, "Y1: ", y1, "Y2: ", y2)
    print("--------------------------------")

cv2.imwrite('didatico_' + image, img)