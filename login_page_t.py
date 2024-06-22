import tkinter
from tkinter import messagebox



def toggle_password_visibility():
    if show_password.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

window = tkinter.Tk()
window.title("Teachers login")
window.geometry('900x600')
window.configure(bg='#659DBD')

import mysql.connector

def login():
    # Establish a connection to the database
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="050603",
            database="studentease"
        )
    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        return
    global global_username
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username and password match a record in the professor_details table
    cursor = connection.cursor()
    query = "SELECT * FROM professor_details WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    professor = cursor.fetchone()

    if professor:
        global_username = username
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        window.destroy()
        import pro2
    else:
        messagebox.showerror(title="Error", message="Invalid login.")

    # Close the cursor and connection
    cursor.close()
    connection.close()

frame = tkinter.Frame(bg='#659DBD')

# Creating widgets
login_label = tkinter.Label(
    frame, text="         login ", bg='#659DBD', fg="white", font=("impact", 35))
username_label = tkinter.Label(
    frame, text="Username:", bg='#659DBD', fg="#FFFFFF", font=("Arial", 16))
username_entry = tkinter.Entry(frame, font=("Arial", 16))
password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))
password_label = tkinter.Label(
    frame, text="Password:", bg='#659DBD', fg="#FFFFFF", font=("Arial", 16))
login_button = tkinter.Button(
    frame, text="Login", bg="white", fg="#659DBD", font=("Arial", 16), command=login)

# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=(40, 20))
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=1, columnspan=2, pady=30)

# Create a BooleanVar to track the state of whether to show the password
show_password = tkinter.BooleanVar()
show_password.set(False)

# Create a Checkbutton to toggle password visibility
show_password_checkbox = tkinter.Checkbutton(frame, text="Show Password", variable=show_password, bg='#659DBD', fg="#FFFFFF", font=("Arial", 12), command=toggle_password_visibility)
show_password_checkbox.grid(row=2, column=3, pady=5, sticky='w')

frame.pack(expand=True, pady=(window.winfo_reqheight() - frame.winfo_reqheight()) // 2)

def div_choose():
    # messagebox.showinfo("Login", "Redirecting to student login")
    window.destroy()
    import pro2

window.mainloop()
