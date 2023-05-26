import cv2 as cv
import numpy as np

classNames = {0: 'background',

              1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',

              5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',

              10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',

              14: 'motorbike', 15: 'person', 16: 'pottedplant',

              17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}

cap = cv.VideoCapture('Videos/video1.mp4')
net = cv.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")
while True:
    ret, frame = cap.read()

    frame_resized = cv.resize(frame, (300, 300))  # resize frame for prediction

    # MobileNet requires fixed dimensions for input image(s)
    # so we have to ensure that it is resized to 300x300 pixels.
    # set a scale factor to image because network the objects has differents size.
    # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
    # after executing this command our "blob" now has the shape:
    # (1, 3, 300, 300)
    blob = cv.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
    # Set to network the input blob
    net.setInput(blob)
    # Prediction of network
    detections = net.forward()

    # Size of frame resize (300x300)
    cols = frame_resized.shape[1]
    rows = frame_resized.shape[0]

    # For get the class and location of object detected,
    # There is a fix index for class, location and confidence
    # value in @detections array .
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]  # Confidence of prediction
        if confidence > 0.:  # Filter prediction
            class_id = int(detections[0, 0, i, 1])  # Class label

            # Object location
            xLeftBottom = int(detections[0, 0, i, 3] * cols)
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop = int(detections[0, 0, i, 5] * cols)
            yRightTop = int(detections[0, 0, i, 6] * rows)

            # Factor for scale to original size of frame
            heightFactor = frame.shape[0] / 300.0
            widthFactor = frame.shape[1] / 300.0
            # Scale object detection to frame
            xLeftBottom = int(widthFactor * xLeftBottom)
            yLeftBottom = int(heightFactor * yLeftBottom)
            xRightTop = int(widthFactor * xRightTop)
            yRightTop = int(heightFactor * yRightTop)
            # Draw location of object
            cv.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                          (0, 255, 0))

            # Draw label and confidence of prediction in frame resized
            if class_id in classNames:
                label = classNames[class_id] + ": " + str(confidence)
                labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                yLeftBottom = max(yLeftBottom, labelSize[1])
                cv.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                              (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                              (255, 255, 255), cv.FILLED)
                cv.putText(frame, label, (xLeftBottom, yLeftBottom),
                            cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

                print(label)  # print class and confidence
    cv.namedWindow("frame", cv.WINDOW_NORMAL)
    cv.imshow("frame", frame)
    if cv.waitKey(1) >= 0:  # Break with ESC
        break