import os
import mysql.connector

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="050603",
    database="studentease"
)

# Create a cursor object to execute SQL queries
cursor = db.cursor()

# Read the video file as binary data
video_file_path = r"C:\Users\himes\OneDrive\Desktop\Mini Project Sem IV\videos\Programming in Java.mp4"
video_name = os.path.basename(video_file_path)
with open(video_file_path, "rb") as file:
    video_data = file.read()

# Insert the video data into the database
insert_query = "INSERT INTO videos (video_name, video_data) VALUES (%s, %s)"
cursor.execute(insert_query, (video_name, video_data))

# Commit the transaction
db.commit()

# Close the cursor and database connection
cursor.close()
db.close()
