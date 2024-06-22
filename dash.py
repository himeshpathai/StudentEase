import tkinter as tk
from tkinter import Label, SUNKEN, LEFT, RIGHT, BOTH, Y, messagebox
from PIL import Image, ImageTk

class Title:
    def __init__(self, root):
        self.root = root

        # Frame for label
        label_frame = tk.Frame(self.root, bg="blue", bd=20, relief=SUNKEN)
        label_frame.grid(row=0, column=0, sticky="ew")

        # Label for the title
        lbl_title = tk.Label(label_frame, text="STUDENTEASE", fg="red", bg="white",
                            font="Baskerville  30 italic bold", padx=10, pady=10)
        lbl_title.pack(fill="x")  # Pack the label onto the title frame

        # Frame for image sliding   
        image_frame = tk.Frame(self.root, bg="red", relief=SUNKEN)
        image_frame.grid(row=1, column=0, sticky="nsew")

        # Load images
        self.images = ["d3.jpg","d4.jpg", "d2.jpg"]
        self.current_image_index = 0
        self.original_positions = {}  # Dictionary to store original positions

        self.image_label = tk.Label(image_frame)
        self.image_label.pack(fill="both", expand=True)

        # Create and configure buttons frame
        button_frame = tk.Frame(root)
        button_frame.grid(row=2, column=0, sticky="ew")

        # Create and configure "Next" button
        next_button = tk.Button(button_frame, text="Next", command=self.show_next_image)
        next_button.pack(side=tk.RIGHT, padx=5, pady=20)

        # Create and configure "Back" button
        back_button = tk.Button(button_frame, text="Back", command=self.show_previous_image)
        back_button.pack(side=tk.LEFT, padx=10, pady=20)

        # Show the first image at its original position
        self.show_next_image()

        # Frame for additional content below image frame
        f3 = tk.Frame(self.root, bg="white", relief=SUNKEN, borderwidth=10)
        f3.grid(row=3, column=0, sticky="ew")

        l=Label(f3,text="One stop destination to make study ease...",font="Baskerville 40 bold",bg="white")
        l.pack(padx=150, pady=20)

        # fourth frame
        f4 = tk.Frame(self.root, bg="white", relief=SUNKEN, borderwidth=10)
        f4.grid(row=4, column=0, sticky="ew")

        # Add content to the fourth frame
        left_image_path = "p1n.png"
        right_image_path = "p2n.png"

        left_image = Image.open(left_image_path)
        right_image = Image.open(right_image_path)

        left_photo = ImageTk.PhotoImage(left_image)
        right_photo = ImageTk.PhotoImage(right_image)

        left_label = Label(f4, image=left_photo, bg="white")
        left_label.grid(row=0, column=0, padx=(400, 250), pady=10, sticky='w')

        right_label = Label(f4, image=right_photo, bg="white")
        right_label.grid(row=0, column=1, padx=(20, 50), pady=10, sticky='e')

        # Create and place buttons
        button1 = tk.Button(f4, text="Teacher login", command=self.teacher_login)
        button1.grid(row=1, column=0, padx=(430, 0), pady=(0, 10), sticky='w')

        button2 = tk.Button(f4, text="Student login", command=self.Login)
        button2.grid(row=1, column=1, padx=(0,75), pady=(0, 10), sticky='e')

        # Keep a reference to prevent garbage collection
        left_label.image = left_photo
        right_label.image = right_photo

        # Set a fixed height for the fourth frame
        root.rowconfigure(4, weight=12)

        self.root.update_idletasks()
        root.bind("<MouseWheel>", self.on_mousewheel)

    def Login(self):
        messagebox.showinfo("Login", "Redirecting to student login")
        root.destroy()
        import login_page_s


    def teacher_login(self):
        messagebox.showinfo("Login", "Redirecting to teacher login")
        root.destroy()
        import login_page_t

    def show_next_image(self):
        # Load image and get original position
        image_path = self.images[self.current_image_index]
        if image_path not in self.original_positions:
            self.original_positions[image_path] = self.image_label.winfo_geometry()  # Store initial position
        original_position = self.original_positions[image_path]

        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        # Update label with new image
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference to prevent garbage collection

        # Change label position if not already on the first image
        if self.current_image_index > 0:
            self.image_label.geometry(original_position)

        # Increment image index and handle overflow
        self.current_image_index = (self.current_image_index + 1) % len(self.images)

    def show_previous_image(self):
        # Decrement image index and handle underflow (loop back to last image)
        self.current_image_index = (self.current_image_index - 1) % len(self.images)

        # Load image and get original position
        image_path = self.images[self.current_image_index]
        original_position = self.original_positions[image_path]

        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        # Update label with new image
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference to prevent garbage collection

        # Change label position to the original position
        self.image_label.geometry(original_position)

    def on_mousewheel(self, event):
        canvas.yview_scroll(-1*(event.delta//120), "units")

root = tk.Tk()
root.geometry("1420x750")  # Screen sizing
root.minsize(200, 100)
root.title("Dashboard")

main_frame = tk.Frame(root)
main_frame.pack(fill=BOTH, expand=True)

canvas = tk.Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 0), pady=(0, 0))

canvas.configure(yscrollcommand=scrollbar.set)

second_frame = tk.Frame(canvas)
second_frame_id = canvas.create_window((0, 0), window=second_frame, anchor="nw", width=canvas.winfo_width())

def configure_canvas(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(second_frame_id, width=event.width)

canvas.bind('<Configure>', configure_canvas)

for i in range(5):  # For example, create 10 labels
    label = Label(second_frame, text=f"Label {i}")
    label.grid(row=i, column=0, sticky="ew")

Title(second_frame)
# root.resizable(False, True)
root.mainloop()