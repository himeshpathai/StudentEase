import tkinter as tk
from tkinter import Scrollbar, messagebox
from PIL import Image, ImageTk 
from tkinter import filedialog
import os
import cv2
import mysql.connector
from io import BytesIO
import tkinter as tk
from tkinter import ttk, Scrollbar
from tkinter import messagebox
from tkinter import *
import mysql.connector
import cv2
import os
from PIL import Image, ImageTk
import fitz  # PyMuPDF for PDFs
import pptx  # python-pptx for PPTs
import docx  # python-docx for DOCX

pdf_window = None
ppt_window = None
docx_window = None


def create_canvas2(frame2):
    
    global canvas_announcement, post_button, canvas_lecture, default_message, file_list_frame, chat_input1  # Use global keyword to modify global variables

    
    cn1 = tk.Canvas(frame2, bg="lightpink", width=690, height=460)
    cn1.grid(row=0, column=0, sticky="nsew")

    cn1_upper = tk.Frame(cn1, width=690, height=80, bg='darkslateblue')
    cn1.create_window(0, 0, anchor='center', window=cn1_upper)
    cn1_upper.grid(sticky='nsew')

    button_width = 200  # Adjust the width of the buttons as needed
    button_height = 45  # Increased height
    gap = 100  # Adjust the gap between the buttons as needed

    # Create the buttons
    button1 = tk.Button(cn1_upper, text="Announcement",command=show_announcement)
    button2 = tk.Button(cn1_upper, text="Lectures",command=show_lecture)

    # Place the buttons horizontally centered with a gap between them
    center_x = 345  # Adjust the center x-coordinate as needed
    button1_x = center_x - button_width - gap // 2
    button2_x = center_x + gap // 2
    button_y = 20 
    button1.place(x=button1_x, y=button_y, width=button_width, height=button_height)
    button2.place(x=button2_x, y=button_y, width=button_width, height=button_height)

    # Create canvas_announcement, canvas_lecture, file_list_frame, and upload_button inside os
    canvas_announcement = tk.Canvas(cn1, bg="lightpink", width=690, height=460)
    canvas_announcement.grid(row=1,column=0,sticky='nsew')

    canvas_lecture = tk.Canvas(cn1, bg="thistle", width=690, height=460)
    canvas_lecture.grid(row=1,column=0,sticky='nsew')
    

    
    file_list_frame = tk.Frame(canvas_announcement)
    file_list_frame.grid(row=2, column=0)

    refresh_file_list()
    

    fetch_and_display_videos(cursor, canvas_lecture)
    
    return cn1

def show_announcement():
    # Functionality for showing announcements
    canvas_announcement.grid()
    canvas_lecture.grid_forget()  # Hide the lecture chatbox canvas if it's visible

def show_lecture():
    canvas_lecture.grid()
    canvas_announcement.grid_forget()  # Hide the announcement chatbox canvas if it's visible


        
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="050603",
    database="studentease"
)
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="050603",
    database="studentease"
)
cursor = db.cursor()
def fetch_and_display_videos(cursor, canvas_lecture):
    def play_video(video_data):
    # Play the video using OpenCV
        temp_file = 'temp_video.avi'
        with open(temp_file, 'wb') as f:
            f.write(video_data)

            cap = cv2.VideoCapture(temp_file)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            current_frame = 0
            is_playing = True

            def on_play_pause():
                nonlocal is_playing
                is_playing = not is_playing

            def on_seek(value):
                nonlocal current_frame
                current_frame = int(value)
                cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

                # Calculate the current time position
                current_time = current_frame / cap.get(cv2.CAP_PROP_FPS)
                formatted_time = f"{int(current_time // 60)}:{int(current_time % 60):02d}"
                seeker.config(label=f"Time: {formatted_time}")

            def update_frame():
                nonlocal current_frame, is_playing
                if is_playing:
                    ret, frame = cap.read()
                    if ret:
                        current_frame += 1
                        if current_frame >= total_frames:
                            current_frame = 0
                            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                        cv2.imshow('Video', frame)

                    else:
                        current_frame = 0
                        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
                        is_playing = False
                video_frame.after(30, update_frame)

            def on_exit():
                cap.release()
                cv2.destroyAllWindows()

        # Create a new window for the video
        video_frame = tk.Toplevel()
        video_frame.title("Video Player")

        # Play/Pause Button
        play_pause_button = Button(video_frame, text="Play/Pause", command=on_play_pause)
        play_pause_button.pack(side=tk.LEFT)

        # Seeker
        seeker = tk.Scale(video_frame, from_=0, to=total_frames, orient=tk.HORIZONTAL, command=on_seek)
        seeker.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Start video playback
        update_frame()

    try:
        # Fetch video data from the database
        cursor.execute("SELECT video_name, video_data, timestamp FROM videos")
        videos = cursor.fetchall()

        # Clear any existing widgets in inner_frame2
        for widget in canvas_lecture.winfo_children():
            widget.destroy()

        # Create buttons and seekers for each video in inner_frame2
        for video_name, video_data, timestamp in videos:
            video_button_text = f"{video_name} ({timestamp})"
            video_button = Button(canvas_lecture, text=video_button_text, command=lambda vd=video_data: play_video(vd), font=("Arial", 12))
            video_button.pack(anchor=N, expand=True)

    
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to fetch videos from database: {error}")

def refresh_file_list():

    # Fetch data from the 'files' table
    cursor2.execute("SELECT name, timestamp FROM files ORDER BY timestamp DESC")
    file_data = cursor2.fetchall()

    # Fetch data from the 'announcements' table
    cursor3.execute("SELECT message, timestamp FROM announcements ORDER BY timestamp DESC")
    announcement_data = cursor3.fetchall()

    # Combine both datasets with a flag indicating the type (0 for file, 1 for announcement)
    combined_data = [(name, timestamp, 0) for name, timestamp in file_data] + [(message, timestamp, 1) for message, timestamp in announcement_data]

    # Sort combined data by timestamp
    combined_data.sort(key=lambda x: x[1], reverse=True)

    # Clear existing widgets
    for widget in file_list_frame.winfo_children():
        widget.destroy()

    # Display the combined data in the file_list_frame
    for i, (data, timestamp, data_type) in enumerate(combined_data):
        frame = tk.Frame(file_list_frame, width=690, height=20, bg="lightgray")
        frame.grid(row=i, column=0, columnspan=2, sticky="ew")
        if data_type == 0:  # File name
            label_text = f"File: {data} ({timestamp})"
            button_text = "Download"
            command = lambda name=data, ext=data: download_file_by_name(name, ext)
            # Create label and download button
            label = tk.Label(file_list_frame, text=label_text, cursor="hand2", bg="lightgray", font=("Arial", 12))
            label.grid(row=i, column=0, sticky="ew")
            download_button = tk.Button(file_list_frame, text=button_text, command=command)
            download_button.grid(row=i, column=1, padx=5)
        else:  # Announcement message
            label_text = f"Announcement: {data} ({timestamp})"
            # Create label for announcement
            label = tk.Label(file_list_frame, text=label_text, cursor="hand2", bg="lightgray", font=("Arial", 12))
            label.grid(row=i, column=0, columnspan=2, sticky="ew")

        # Bind label to open_file function
        label.bind("<Button-1>", lambda event, data=data: open_file(data))

cursor4 = connection.cursor()
cursor5 = connection.cursor()



def download_file_by_name(file_name, file_extension):
    # Retrieve file data from the database
    cursor2.execute("SELECT data FROM files WHERE name = %s", (file_name,))
    file_data = cursor2.fetchone()[0]

    # Determine the file extension
    file_extension = file_name.split(".")[-1].lower()

    # Prompt user to choose download location
    file_path = filedialog.asksaveasfilename(defaultextension=file_extension, filetypes=[(f"{file_extension.upper()} files", f"*.{file_extension}")])
    
    if file_path:
        # Write the file data to the chosen file path
        with open(file_path, "wb") as file:
            file.write(file_data)

        print(f"Downloading file: {file_name}.{file_extension} to {file_path}")
    else:
        print("Download canceled by user")

def open_file(file_name):
    cursor2.execute("SELECT data FROM files WHERE name = %s", (file_name,))
    file_data = cursor2.fetchone()[0]
    file_extension = file_name.split(".")[-1].lower()
    if file_extension == "pdf":
        display_pdf(file_data)
    elif file_extension == "pptx":
        display_ppt(file_data)
    elif file_extension == "docx":
        display_docx(file_data)
    else:
        print(f"Unsupported file type: {file_extension}")

def display_pdf(file_data):
    pdf_window = tk.Toplevel()
    pdf_window.title("PDF Viewer")
    pdf_viewer = fitz.open(stream=BytesIO(file_data), filetype="pdf")
    pdf_text = ""
    for page in pdf_viewer:
        pdf_text += page.get_text("text")
    pdf_viewer.close()
    pdf_scrollbar = tk.Scrollbar(pdf_window)
    pdf_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    pdf_text_widget = tk.Text(pdf_window, wrap=tk.WORD, yscrollcommand=pdf_scrollbar.set)
    pdf_text_widget.pack(fill=tk.BOTH, expand=True)
    pdf_text_widget.insert(tk.END, pdf_text)
    pdf_scrollbar.config(command=pdf_text_widget.yview)

def display_ppt(file_data):
    ppt_window = tk.Toplevel()
    ppt_window.title("PPT Viewer")
    ppt_viewer = pptx.Presentation(BytesIO(file_data))
    slide_images = []
    for slide in ppt_viewer.slides:
        slide_image_stream = BytesIO()
        slide.save(slide_image_stream, "PNG")
        slide_images.append(Image.open(slide_image_stream))
    ppt_viewer.close()
    current_slide = 0
    slide_image_label = tk.Label(ppt_window, image=ImageTk.PhotoImage(slide_images[current_slide]))
    slide_image_label.pack()
    def show_next_slide():
        nonlocal current_slide
        current_slide = (current_slide + 1) % len(slide_images)
        slide_image_label.config(image=ImageTk.PhotoImage(slide_images[current_slide]))
    next_button = tk.Button(ppt_window, text="Next Slide", command=show_next_slide)
    next_button.pack()

def display_docx(file_data):
    docx_window = tk.Toplevel()
    docx_window.title("DOCX Viewer")
    doc = docx.Document(BytesIO(file_data))
    doc_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    doc_text_widget = tk.Text(docx_window, wrap=tk.WORD)
    doc_text_widget.pack(fill=tk.BOTH, expand=True)
    doc_text_widget.insert(tk.END, doc_text)

# Connect to the MySQL database


cursor1 = connection.cursor()
cursor2 = connection.cursor()


def on_mousewheel(event):
    canvas = event.widget
    if canvas.cget("scrollregion"):
        shift = canvas.winfo_height() // 100 * ((-1) if event.delta < 0 else 1)
       
    
def upload_message():
    print("upload button clicked")

        
def post_message():
    # Get the message from the chat input
    message = chat_input1.get("1.0", tk.END).strip()
    
    # Check if the message is not empty
    if message and message != default_message:
        try:
            # Insert the message into the announcements table in the database
            cursor3.execute("INSERT INTO announcements (message) VALUES (%s)", (message,))
            connection.commit()
            print("Message posted successfully.")
            
            # Clear the chat input after posting the message
            chat_input1.delete("1.0", tk.END)
            chat_input1.insert(tk.END, default_message)
            chat_input1.tag_add("default", "1.0", "end")
            chat_input1.tag_config("default", foreground="darkgrey")
            
        except mysql.connector.Error as error:
            print(f"Failed to post message: {error}")
    else:
        print("Please enter a message to post.")
      # Disable the post button if the chat input contains the default message
    
        
cursor3 = connection.cursor()        
        
        

def cancel_message():
    print("Cancel button clicked")  

    
def clear_default_message(event):
    """Clears the default message when the user clicks on the text box"""
    if chat_input1.get("1.0", "end-1c") == "Announce something to the class":
        chat_input1.delete("1.0", tk.END) 