import tkinter as tk
from tkinter import Scrollbar, messagebox
from PIL import Image, ImageTk 
from tkinter import filedialog
import os

root = None
frame1 = None
frame2 = None
small_frame = None


def login_page():
    # Create an instance of NewPage and display it
    login_page_instance = login_page.NewPage(root)
    login_page_instance.pack(fill=tk.BOTH, expand=True)


def on_configure(event):
    for widget in widgets:
        if isinstance(widget, tk.Canvas):
            widget.config(scrollregion=widget.bbox("all"))

def toggle_frame_visibility():
    global frame1_visible
    if frame1_visible:
        frame1.grid_forget()  # Hide frame1
        frame1_visible = False
        root.grid_columnconfigure(0, weight=0)  # Decrease size of frame1
        root.grid_columnconfigure(1, weight=1)  # Increase size of frame2
        frame2.grid_columnconfigure(0, weight=1)  # Expand canvas4
    else:
        frame1.grid(row=1, column=0, sticky="nsew")  # Show frame1
        frame1_visible = True
        root.grid_columnconfigure(0, weight=1)  # Increase size of frame1
        root.grid_columnconfigure(1, weight=0)  # Decrease size of frame2
        frame2.grid_columnconfigure(0, weight=0)  # Shrink canvas4

def show_account_details():
    global small_frame
    # Function to retrieve account details from the database and display them
    # For demonstration purposes, let's assume account details are retrieved from a function get_account_details()
    account_details = get_account_details()

    # Create a small frame to display account details
    small_frame = tk.Frame(root, width=200, height=300, bg="lightgray")
    small_frame.grid(row=1, column=1, sticky="ne")  # Position the frame towards the right

    # Display account details in the small frame
    details_label = tk.Label(small_frame, text=account_details, font=("Arial", 12), bg="lightgray")
    details_label.pack()

    # Create a logout button in the small frame
    logout_button = tk.Button(small_frame, text="Logout", command=logout)
    logout_button.pack()

def get_account_details():
    # Function to retrieve account details from the database (replace this with your actual database retrieval code)
    return "Account Details:\nName: John Doe\nEmail: johndoe@example.com\nRole: Proffessor"
button_list = []  # Initialize an empty list to store buttons

def switch_canvas(canvas_to_hide, canvas_to_show):
    canvas_to_hide.grid_forget()
    canvas_to_show.grid(row=0, column=0, sticky="nsew")


import subprocess

def logout():
    # Function to handle logout button click
    global small_frame
    if small_frame:
        small_frame.destroy()  # Destroy the small frame if it exists
        small_frame = None  # Reset the small_frame variable
    
    # Display a confirmation messagebox for logout
    confirm_logout = messagebox.askokcancel("Logout", "Are you sure you want to logout?")
    if confirm_logout:
        # Launch the login page script using subprocess
        print("Launching login page script...")
        subprocess.Popen(["python", r"C:\Users\HP\Desktop\python project\login_page.py"])
        print("Login page script launched.")

        root.quit()  # Quit the main application


def hide_details(event):
    global small_frame
    if small_frame:
        x, y = event.x_root, event.y_root
        if x < small_frame.winfo_rootx() or x > small_frame.winfo_rootx() + small_frame.winfo_width() \
                or y < small_frame.winfo_rooty() or y > small_frame.winfo_rooty() + small_frame.winfo_height():
            small_frame.destroy()
            small_frame = None
            
def toggle_dropdown():
    if dropdown_frame.winfo_ismapped():
        canvas2.itemconfigure(dropdown_button, text="Classes")
        dropdown_frame.place_forget()  # Use place_forget to hide the dropdown frame
    else:
        canvas2.itemconfigure(dropdown_button, text="Enrolled Classes")
        
        # Calculate the position for the dropdown frame in the center of the canvas and frame
        canvas_width = canvas2.winfo_width()
        canvas_height = canvas2.winfo_height()
        frame_width = dropdown_frame.winfo_reqwidth()  # Get the required width of the dropdown frame
        frame_height = dropdown_frame.winfo_reqheight()  # Get the required height of the dropdown frame
        
        x = (canvas_width - frame_width) // 2  # Calculate the x-coordinate for centering horizontally
        y = (canvas_height - canvas_height) + 40  # Calculate the y-coordinate for centering vertically
        
        dropdown_frame.place(x=x, y=y)  # Place the dropdown frame in the center of the canvas and frame

        # Ensure the dropdown button is above the dropdown frame
        canvas2.tag_raise(dropdown_button)
        canvas2.tag_lower(dropdown_frame)
def on_mousewheel(event):
    canvas = event.widget
    if canvas.cget("scrollregion"):
        shift = canvas.winfo_height() // 100 * ((-1) if event.delta < 0 else 1)
def on_mousewheel(event):
    """Function to handle mousewheel scrolling in the chat_input text box"""
    chat_input.yview_scroll(-1 * (event.delta // 120), "units")
def show_upload_button():
    
    global upload_button_frame,upload_button
    
    # Create the chatbox frame
    upload_button_frame = tk.Frame(root, bg="lightgrey", width=600, height=700)  # Adjust size as needed
    upload_button_frame.place(x=730, y=128)  # Adjust position as needed
    upload_button = tk.Button(upload_button_frame, text="Upload", command=upload_message)
    upload_button.grid(row=1, column=1, padx=2, pady=2,sticky="se")
    upload_button_frame.grid_rowconfigure(0, weight=1)
def upload_message():
    print("upload button clicked")

def show_chatbox():
   
    global chatbox_frame, chat_input, post_button, cancel_button
    
    # Create the chatbox frame
    chatbox_frame = tk.Frame(root, bg="lightgrey", width=430, height=100)  # Adjust size as needed
    chatbox_frame.place(x=228, y=128)  # Adjust position as needed
    
    # Create the text box inside the chatbox frame
    chat_input = tk.Text(chatbox_frame, bg="white", width=60, height=4)  # Adjust width and height as needed
    chat_input.grid(row=0, column=0, columnspan=2, padx=5, pady=5,sticky="nsew")  # Adjust padding as needed
      # Set default message in the text box


    # Set default message in the text box
    default_message = "Announce something to the class"
    chat_input.insert(tk.END, default_message)
    chat_input.tag_add("default", "1.0", "end")
    chat_input.tag_config("default", foreground="darkgrey")  # Change the color of the default message
    chat_input.bind("<Button-1>", clear_default_message)
        # Bind mousewheel event to enable scrolling
    chat_input.bind("<MouseWheel>", on_mousewheel)
    
    # Create the "Post" button
    post_button = tk.Button(chatbox_frame, text="Post", command=post_message)
    post_button.grid(row=1, column=0, padx=10, pady=5,sticky="sw")  # Adjust padding as needed

    # Create the "Cancel" button
    cancel_button = tk.Button(chatbox_frame, text="Cancel", command=cancel_message)
    cancel_button.grid(row=1, column=1, padx=10, pady=5,sticky="se")  # Adjust padding as needed
    # Configure row to make the text box expandable
    chatbox_frame.grid_rowconfigure(0, weight=1)   
def post_message():
    print("Post button clicked")

def cancel_message():
    print("Cancel button clicked")  

    
def clear_default_message(event):
    """Clears the default message when the user clicks on the text box"""
    if chat_input.get("1.0", "end-1c") == "Announce something to the class":
        chat_input.delete("1.0", tk.END)   
 
def show_chatbox_and_upload_button():
    show_chatbox()
    show_upload_button()    

root = tk.Tk()
root.title("Dashboard")
root.geometry("935x588")

widgets = []

frame3 = tk.Frame(root, width=700, height=80, bg="lightcoral")
frame3.grid(row=0, column=0, columnspan=2, sticky="nsew")
widgets.append(frame3)

frame1 = tk.Frame(root, width=200, height=540, bg="white")
frame1.grid(row=1, column=0, sticky="nsew")
widgets.append(frame1)

frame2 = tk.Frame(root, width=690, height=900, bg="white")
frame2.grid(row=1, column=1, sticky="nsew")
widgets.append(frame2)

canvasd10a=tk.Canvas(frame2, width=690, height=540, bg="white")
canvasd10a.grid(row=0, column=0, sticky="nsew")
framed10a_upper= tk.Frame(canvasd10a, width=690, height=80, bg='dimgrey')
# Place the frame on the canvas using the grid method
canvasd10a.create_window(0, 0, anchor='center', window=framed10a_upper)

framed10a_upper.grid()
# Calculate the horizontal center of the frame
center_x = framed10a_upper.winfo_reqwidth() // 2

#Create the buttons
button_width = 200  # Adjust the width of the buttons as needed
button_height = 45  # Increased height
gap = 100  # Adjust the gap between the buttons as needed

# Create the buttons
button1 = tk.Button(framed10a_upper, text="Announcement", command=show_chatbox_and_upload_button)
button2 = tk.Button(framed10a_upper, text="Lectures")

# Place the buttons horizontally centered with a gap between them
button1_x = center_x - button_width - gap // 2
button2_x = center_x + gap // 2
button_y = 20 
button1.place(x=button1_x, y=button_y, width=button_width, height=button_height)
button2.place(x=button2_x, y=button_y, width=button_width, height=button_height)

# Create the chatbox textbox
chatbox_textbox = tk.Text(root, bg="lightgrey")
upload_button = tk.Button(canvasd10a, text="upload",font=("arial",10),width=15,height=3,background="LIGHTBLUE")
canvas1 = tk.Canvas(frame1, bg="lightblue", width=200, height=100, highlightthickness=0)
canvas1.grid(row=0, column=0, sticky="nsew")
widgets.append(canvas1)

scrollbar_y3 = Scrollbar(frame1, orient=tk.VERTICAL, command=canvas1.yview)
scrollbar_y3.grid(row=0, column=1, sticky="ns")  # Corrected placement
canvas1.configure(yscrollcommand=scrollbar_y3.set)

canvas2 = tk.Canvas(frame1, bg="pink", width=200, height=420, highlightthickness=0)
canvas2.grid(row=1, column=0, sticky="nsew")
widgets.append(canvas2)

scrollbar_y1 = Scrollbar(frame1, orient=tk.VERTICAL, command=canvas2.yview)
scrollbar_y1.grid(row=1, column=1, sticky="ns")  # Corrected placement
canvas2.configure(yscrollcommand=scrollbar_y1.set)

canvas3 = tk.Canvas(frame1, bg="light green", width=200, height=100, highlightthickness=0)
canvas3.grid(row=2, column=0, sticky="nsew")
widgets.append(canvas3)

scrollbar_y4 = Scrollbar(frame1, orient=tk.VERTICAL, command=canvas3.yview)
scrollbar_y4.grid(row=2, column=1, sticky="ns")  # Corrected placement
canvas3.configure(yscrollcommand=scrollbar_y4.set)

canvas4 = tk.Canvas(frame2, bg="lightyellow", width=690, height=540, highlightthickness=0)
canvas4.grid(row=0, column=0, sticky="nsew") 
widgets.append(canvas4)


scrollbar_y2 = Scrollbar(frame2, orient=tk.VERTICAL, command=canvas4.yview)
scrollbar_y2.grid(row=0, column=1, sticky="ns")  # Corrected placement
canvas4.configure(yscrollcommand=scrollbar_y2.set)

canvas4.bind("<Configure>", lambda e: canvas4.configure(scrollregion=canvas4.bbox("all")))
canvas1.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))
canvas3.bind("<Configure>", lambda e: canvas3.configure(scrollregion=canvas3.bbox("all")))
canvas2.bind("<Configure>", lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))

home_button = tk.Button(canvas1, text="Home",font=("arial",10),width=25,height=3,background="LIGHTBLUE")
home_button.grid(row=0,column=0)

# Create dropdown button with border and white background
dropdown_button = canvas2.create_text(150, 20, text="Classes", font=("Arial", 10), fill="pink", anchor="center")
# Add border and white background
canvas2.itemconfigure(dropdown_button, font=("Arial", 10, "bold"), fill="black")  # Change text color to black and add bold font
canvas2.coords(dropdown_button, 110, 20)


# Create a rectangle behind the text for the button appearance
button_coords = canvas2.bbox(dropdown_button)

# Position the button towards the left
canvas2.coords(dropdown_button, 110, 20)  # Adjust the x-coordinate as needed
setting_button = tk.Button(canvas3, text="Setting",font=("arial",10),width=25,height=3,background="lightgreen")
setting_button.grid(row=0,column=2)
# Position the rectangle behind the text with an offset to prevent overlapping
rect_offset = 4  # Adjust the offset as needed
rect_coords = (button_coords[0] - rect_offset, button_coords[1] - rect_offset, button_coords[2] + rect_offset, button_coords[3] + rect_offset)

# Bind the dropdown button to toggle_dropdown function
canvas2.tag_bind(dropdown_button, "<Button-1>", lambda event: toggle_dropdown())

dropdown_frame = tk.Frame(canvas2)
tk.Label(dropdown_frame, text="Enrolled Classes",width=28,height=3).pack()
heading_line = tk.Frame(dropdown_frame, height=2, bg="black")
heading_line.pack(fill=tk.X)
tk.Button(dropdown_frame, text="D10A",width=25,height=3, command=lambda: switch_canvas(canvas4, canvasd10a)).pack()
tk.Button(dropdown_frame, text="D10B",width=25,height=3).pack()
tk.Button(dropdown_frame, text="D10C",width=25,height=3).pack()


def show_buttons():
    """Displays the buttons in the middle of frame2"""
    global button_list

    # Clear any existing buttons
    for button in button_list:
        button.destroy()
    button_list.clear()

    # Calculate the center coordinates of frame2
    frame2_width = frame2.winfo_width()
    frame2_height = frame2.winfo_height()

    # Define the number and spacing of buttons (adjust as needed)
    num_buttons = 3
    button_spacing = 200 # Adjust spacing between buttons
       # Set the size of the buttons
    button_width = 18
    button_height = 4
     # Set the left shift offset
    left_shift = 70  # Adjust as needed
    # Set the upward shift offset
    upward_shift = 30  # Adjust as neede
    # Create buttons and position them in the center of frame2

    # Custom names and background colors for the buttons
    button_data = [("D10A -> COA", "hotpink", lambda: switch_canvas(canvas4, canvasd10a)),
               ("D10B -> CN", "lightsalmon", lambda: print("Command for D10B -> CN button")),
               ("D10C -> OS", "aquamarine", lambda: print("Command for D10C -> OS button"))]

    for i, (name, color,command) in enumerate(button_data):
        button = tk.Button(canvas4, text=name, width=button_width, height=button_height, bg=color,command=command)
        button_x = (frame2_width // 2) - ((len(button_data) - 1) * button_spacing // 2) + (i * button_spacing) - left_shift
        button_y = frame2_height // 2 - upward_shift
        button.place(x=button_x, y=button_y)
        button_list.append(button)  # Add button to list


def hide_buttons():
    """Hides the buttons in canvas4"""
    show_buttons()  # Call show_buttons to clear existing buttons

def home_button_clicked():
    switch_canvas(canvasd10a,canvas4)
    """Handles click on the home button"""
    
    show_buttons()  # Display buttons


home_button = tk.Button(canvas1, text="Home",font=("arial",10),width=25,height=3,background="LIGHTBLUE", command=home_button_clicked)
home_button.grid(row=0,column=0)
widgets = [frame1, frame2, frame3, canvas1, canvas2, canvas3, canvas4]

frame1_visible = True  # Initialize frame1 visibility state

mainmenu = tk.Button(frame3, text="Main Menu", command=toggle_frame_visibility)
mainmenu.pack(side=tk.LEFT, padx=10, pady=10)

# Create a button to show account details
show_details_button = tk.Button(frame3, text="Show Account Details", command=show_account_details)
show_details_button.pack(side=tk.RIGHT, padx=10, pady=10)

root.bind("<Button-1>", hide_details)  # Bind left mouse click to hide_details function
# root.bind("<Button-2>", hide_details)  # Bind left mouse click to hide_details function

root.resizable(False, False)  # Disable resizing
root.grid_columnconfigure(0, weight=1)  # Ensure frame1 initially takes full width
root.grid_columnconfigure(1, weight=0)  # Ensure frame2 initially takes no width

root.bind("<Configure>", on_configure)
# Bind the mousewheel event to each canvas
canvas1.bind("<MouseWheel>", on_mousewheel)
canvas2.bind("<Button-1>", toggle_dropdown)
canvas2.bind("<Configure>", on_configure)
canvas3.bind("<Configure>", on_configure)
canvas4.bind("<MouseWheel>", on_mousewheel)

root.mainloop()
