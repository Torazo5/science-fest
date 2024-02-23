from djitellopy import tello
import cv2
import math
import os
folder_path = "/Users/torazotokuda/Documents/GitHub/drone-practice-2/photos"
from ultralytics import YOLO  # Make sure to import YOLO from Ultralytics

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

# Initialize Tello drone
drone = tello.Tello()
drone.connect()
drone.streamon()
print(f'BATTERY: {drone.get_battery}')
# Initialize YOLO model
model = YOLO("yolo-Weights/yolov8n.pt")

while True:
    # Get frame from Tello camera
    frame = drone.get_frame_read().frame

    # Convert image from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform object detection with YOLO model
    results = model(frame, stream=True)

    # Rest of the code remains the same
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # put box in cam
            #cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)
            

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])
            print('xxxxxxxxxxxxxxxxxx')
            if (confidence > 0.55 and classNames[cls] == "apple"):
                # Calculate the center coordinates of the bounding box
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # Calculate the width and height of the resized bounding box
                new_width = (x2 - x1) * 2
                new_height = (y2 - y1) * 2

                # Calculate the new top-left and bottom-right coordinates of the bounding box
                new_x1 = max(center_x - int(new_width / 2), 0)
                new_y1 = max(center_y - int(new_height / 2), 0)
                new_x2 = min(center_x + int(new_width / 2), frame.shape[1])
                new_y2 = min(center_y + int(new_height / 2), frame.shape[0])

                # Resize the region within the new bounding box
                roi = cv2.resize(frame[new_y1:new_y2, new_x1:new_x2], (new_width, new_height))

                # Save the resized ROI as an image file
                file_name = f'apple_image_{x1}_{y1}.jpg'
                file_path = os.path.join(folder_path, file_name)
                cv2.imwrite(file_path, roi)

                print("Image saved successfully!")
            
            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            #cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Tello Camera', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Land the Tello drone
drone.land()
cv2.destroyAllWindows()