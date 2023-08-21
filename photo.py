import cv2

# Используемые моделью MobileNetSSD классификации объектов
classNames = {0: 'фон',
              1: 'самолёт', 2: 'велосипед', 3: 'птица', 4: 'лодка',
              5: 'бутылка', 6: 'автобус', 7: 'машина', 8: 'кошка', 9: 'стул',
              10: 'корова', 11: 'стол', 12: 'собака', 13: 'лошадь',
              14: 'мотоцикл', 15: 'человек', 16: 'растение в горшке',
              17: 'овца', 18: 'диван', 19: 'поезд', 20: 'монитор'}


def main(photo_path, camera_id=0):
    # Загрузка используемой модели вместе с конфигурацией
    net = cv2.dnn.readNetFromCaffe('Models/MobileNetSSD_deploy.prototxt', 'Models/MobileNetSSD_deploy.caffemodel')

    frame = cv2.imread(photo_path)  # Загрузка введенного изображения
    frame_resized = cv2.resize(frame, (300, 300))  # изменение размера фото для распознования людей
    #  Создание переменных масштаба
    heightFactor = frame.shape[0] / 300.0
    widthFactor = frame.shape[1] / 300.0
    # Создание блоб-объекта из изображения
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
    # Подача blob в MobileNetSSD
    net.setInput(blob)

    detections = net.forward()  # Все объекты, обнаруженные моделью

    frame_copy = frame.copy()

    # Размер изображения
    cols = frame_resized.shape[1]
    rows = frame_resized.shape[0]
    number_of_people = 0
    for i in range(detections.shape[2]):

        class_id = int(detections[0, 0, i, 1])  # Классификация объекта

        if class_id == 15:  # Если объект является человеком
            number_of_people += 1
            # Местоположение объекта в изменённом изображении
            xLeftBottom = int(detections[0, 0, i, 3] * cols)
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop = int(detections[0, 0, i, 5] * cols)
            yRightTop = int(detections[0, 0, i, 6] * rows)
            # Местоположение объекта в оригинальном изображении
            xLeftBottom_ = int(widthFactor * xLeftBottom)
            yLeftBottom_ = int(heightFactor * yLeftBottom)
            xRightTop_ = int(widthFactor * xRightTop)
            yRightTop_ = int(heightFactor * yRightTop)
            # рисоване прямоугольников у людей
            cv2.rectangle(frame_resized, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                          (0, 255, 0))

            cv2.rectangle(frame_copy, (xLeftBottom_, yLeftBottom_), (xRightTop_, yRightTop_),
                          (0, 255, 0), -1)

    cv2.addWeighted(frame_copy, 0, frame, 1, 0, frame)

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        class_id = int(detections[0, 0, i, 1])
        if confidence > 0.0 and class_id == 15:
            xLeftBottom = int(detections[0, 0, i, 3] * cols)
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop = int(detections[0, 0, i, 5] * cols)
            yRightTop = int(detections[0, 0, i, 6] * rows)

            xLeftBottom_ = int(widthFactor * xLeftBottom)
            yLeftBottom_ = int(heightFactor * yLeftBottom)
            xRightTop_ = int(widthFactor * xRightTop)
            yRightTop_ = int(heightFactor * yRightTop)
            cv2.rectangle(frame, (xLeftBottom_, yLeftBottom_), (xRightTop_, yRightTop_),
                          (255, 0, 0), thickness=2)
            # Нанесение прямоугольников и вероятности принадлежности к классу на оригинальном изображении

            label = classNames[class_id] + ": " + str(confidence)

    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow("frame", frame)
    cv2.imwrite(f'static/Photos/{camera_id}.jpeg', frame)

    return number_of_people
