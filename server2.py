import mysql.connector
from flask import Flask, request
import cv2
import threading
from datetime import datetime, timedelta
import os

app = Flask(__name__)
RECORDING_DURATION = 60  # 1 minute in seconds
VIDEO_FOLDER = r'C:\Users\himes\OneDrive\Desktop\Mini Project Sem IV\videos'  # Update with the actual folder path

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="050603",
    database="studentease"
)
cursor = db.cursor()

recording_started = False  # Flag to indicate if recording has started

def store_video_in_db(video_name, video_path):
    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="050603",
            database="studentease"
        )
        cursor = db_connection.cursor()

        with open(video_path, "rb") as video_file:
            video_data = video_file.read()

        query = "INSERT INTO videos (video_name, video_data) VALUES (%s, %s)"
        cursor.execute(query, (video_name, video_data))
        db_connection.commit()

        cursor.close()
        db_connection.close()

        print("Video stored in database successfully.")
    except mysql.connector.Error as error:
        print("Error storing video in database:", error)


@app.route('/validate_rfid', methods=['POST'])
def validate_rfid():
    global recording_started
    rfid_data = request.data.decode('utf-8')
    # Query the database to check if the RFID data is valid
    query = "SELECT * FROM rfid_data WHERE rfid_code = %s AND is_valid = TRUE"
    cursor.execute(query, (rfid_data,))
    result = cursor.fetchone()
    print("RFID Validation Result:", result)  # Debug print
    if result:
        recording_started = True  # Set the flag to start recording
        print("Recording Started...")  # Debug print
        start_recording()
        return "RFID Validated"
    else:
        return "RFID Invalid"

def start_recording():
    global recording_started
    if recording_started:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Failed to open webcam.")
            return

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        video_name = f'video_{timestamp}.avi'
        video_path = os.path.join(VIDEO_FOLDER, video_name)
        out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))
        
        if not out.isOpened():
            print("Error: Failed to open VideoWriter.")
            cap.release()
            return

        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < RECORDING_DURATION:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
            out.write(frame)

            cv2.imshow('Recording', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()
        recording_started = False  # Reset the flag after recording ends
        print("Recording Ended...")

        # Store the recorded video in the database
        store_video_in_db(video_name, video_path)
    else:
        print("Recording not started.")


# Start the recording thread
recording_thread = threading.Thread(target=start_recording)
recording_thread.start()


if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}).start()
