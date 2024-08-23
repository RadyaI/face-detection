import cv2
import pygame
import threading

# Inisialisasi pygame mixer
pygame.mixer.init()

# Load the sound
sound = pygame.mixer.Sound('OpenGate.mp3')

repeat_sound = False

def play_sound():
    print("Playing sound")
    sound.play()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(1) # ganti jadi (0) kalo pake kamera default

face_detected_last_time = False  
sound_played = False  

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        if repeat_sound:
            if not face_detected_last_time:
                threading.Thread(target=play_sound).start()
                print("Face detected - playing sound")
                face_detected_last_time = True
        else:
            if not sound_played:
                threading.Thread(target=play_sound).start()
                print("Face detected - playing sound")
                sound_played = True
            face_detected_last_time = True
    else:
        face_detected_last_time = False

    # Ini biar ga muncul popup videonya
    # cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
