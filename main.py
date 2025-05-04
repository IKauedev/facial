import time
import cv2
import numpy as np
import sqlite3
import os
import csv
import winsound
from datetime import datetime

DATASET_DIR = "dataset"
MODEL_PATH = "model/classifier.xml"
LOG_PATH = "log_recognitions.csv"

def create_database():
    os.makedirs('database', exist_ok=True)
    os.makedirs(DATASET_DIR, exist_ok=True)
    os.makedirs("model", exist_ok=True)

    conn = sqlite3.connect('database/access_control.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            access_level INTEGER NOT NULL)
    ''')
    conn.commit()
    conn.close()

def capture_face(name, access_level):
    conn = sqlite3.connect('database/access_control.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (name, access_level) VALUES (?, ?)", (name, access_level))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    print("Capturing face. Please look at the camera...")
    count = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face = gray[y:y + h, x:x + w]
            cv2.imwrite(f"{DATASET_DIR}/user.{user_id}.{count}.jpg", face)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Face Capture', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
            break

    cam.release()
    cv2.destroyAllWindows()
    print("Capture completed.")

def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = [], []

    for filename in os.listdir(DATASET_DIR):
        if filename.endswith(".jpg"):
            path = os.path.join(DATASET_DIR, filename)
            gray = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            user_id = int(filename.split(".")[1])
            faces.append(gray)
            ids.append(user_id)

    recognizer.train(faces, np.array(ids))
    recognizer.write(MODEL_PATH)
    print("Model trained and saved successfully.")

def log_recognition(name, confidence):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, f"{confidence}%"])
def face_recognition():
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Please train with registered users first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    conn = sqlite3.connect('database/access_control.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")
    id_name_map = dict(cursor.fetchall())

    print("📷 Starting face recognition. Press 'q' to exit or wait for timeout.")
    TIMEOUT = 30
    start_time = time.time()
    recognized_count = 0
    REQUIRED_MATCHES = 5
    CONFIDENCE_THRESHOLD = 60.0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error capturing camera frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))

        cv2.putText(frame, "Face recognition in progress...", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        if len(faces) == 0:
            cv2.putText(frame, "No face detected", (10, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        for (x, y, w, h) in faces:
            face = cv2.resize(gray[y:y + h, x:x + w], (150, 150))
            user_id, confidence = recognizer.predict(face)
            confidence_score = round(100 - confidence)
            name = id_name_map.get(user_id, "Unknown")

            if confidence < CONFIDENCE_THRESHOLD:
                recognized_count += 1
                label = f"{name} ({confidence_score}%)"
                color = (0, 255, 0)
            else:
                label = f"Unknown ({confidence_score}%)"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("🔍 Face Recognition - Please face the camera", frame)

        if recognized_count >= REQUIRED_MATCHES:
            print(f"✅ Access granted to {name} with {recognized_count} confirmations.")
            winsound.Beep(1000, 200)
            log_recognition(name, confidence_score)
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Recognition interrupted by user.")
            break

        if time.time() - start_time > TIMEOUT:
            print("⏱️ Recognition timeout reached.")
            break

    conn.close()
    cam.release()
    cv2.destroyAllWindows()

def main():
    create_database()

    print("1 - Register new user")
    print("2 - Perform face recognition")
    option = input("Choose an option: ").strip()

    if option == '1':
        name = input("Enter the user's name: ").strip()
        access_level = int(input("Enter access level (number): "))
        capture_face(name, access_level)
        train_model()
    elif option == '2':
        face_recognition()
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
