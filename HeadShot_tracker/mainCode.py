import cv2
import serial
import time


SERIAL_PORT = 'COM5'  
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  


webcam = cv2.VideoCapture(0)  
FRAME_WIDTH = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
FRAME_HEIGHT = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

CENTER_X = FRAME_WIDTH // 2
CENTER_Y = FRAME_HEIGHT // 2

def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

try:
    while True:
        ret, frame = webcam.read()
        if not ret:
            print("Error: Unable to access webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

           
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            
            delta_x = face_center_x - CENTER_X
            delta_y = face_center_y - CENTER_Y

            servo_x = map_value(delta_x, -CENTER_X, CENTER_X, 180, 0)  
            servo_y = map_value(delta_y, -CENTER_Y, CENTER_Y, 0, 180)  

            command = f"{servo_x},{servo_y}\n"
            ser.write(command.encode())

            break  

        cv2.imshow("Face Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    webcam.release()
    cv2.destroyAllWindows()
    ser.close()
