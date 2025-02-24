from tkinter import*
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import uuid

text_widget=None
current_user_id=None

# Function to toggle password visibility
def toggle_password(entry, button):
    print('eye button toggle')

# Function to toggle between Login and Register
def toggle_mode():
    print('toggle from login to register')

def login():
    print('login function')

def register():
    print('register function')

# Create main window
root = Tk()
root.title("favimark | Login")
root.geometry('700x700')
root.iconbitmap('login.ico')
root.resizable(False, False)

try:
    eye_open_img = Image.open("eye_open.png").resize((20, 20))  # Resize image
    eye_open_icon = ImageTk.PhotoImage(eye_open_img)

    eye_closed_img = Image.open("eye_close.png").resize((20, 20))  
    eye_closed_icon = ImageTk.PhotoImage(eye_closed_img)
except Exception as e:
    print("Error loading images:", e)
    exit()

# Frame for login form
frame = Frame(root, bg='white', highlightbackground='grey', highlightthickness=2)
frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)

frame.grid_columnconfigure(0, weight=1)

# Title
title_label = Label(frame, text="LOG IN / SIGN IN", font=('Arial', 16, 'bold'), bg='white')
title_label.grid(row=0, column=0, pady=15, columnspan=2)

# Profile Image
image = PhotoImage(file="profile.png").subsample(4, 4)
image_label = Label(frame, image=image, bg='white')
image_label.grid(row=1, column=0, pady=10, columnspan=2)

# Username Entry
username_label = Label(frame, text="Username", font=('Arial', 12, 'bold'), bg='white', anchor='w')
username_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=40)
username_entry = Entry(frame, font=('Arial', 12), bd=3)
username_entry.grid(row=3, column=0, columnspan=2, padx=40, pady=5, ipadx=5, ipady=3, sticky="ew")

# Password Entry
password_label = Label(frame, text="Password", font=('Arial', 12, 'bold'), bg='white', anchor='w')
password_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=40)

# Password Frame (Entry + Eye Button)
password_frame = Frame(frame, bg="white")
password_frame.grid(row=5, column=0, columnspan=2, padx=40, pady=5, sticky="ew")

password_entry = Entry(password_frame, show='*', font=('Arial', 12), bd=3, width=20)
password_entry.pack(side="left", fill="x", expand=True, ipadx=5, ipady=3)

eye_button = Button(password_frame, image=eye_open_icon, command=lambda: toggle_password(password_entry, eye_button), bd=0, bg='white', activebackground='white')
eye_button.pack(side="right", padx=5)

# Confirm Password Entry (Only for Signup)
confirm_password_label = Label(frame, text="Confirm Password", font=('Arial', 12, 'bold'), bg='white', anchor='w')
confirm_password_label.grid(row=6, column=0, columnspan=2, sticky="w", padx=40)

confirm_password_frame = Frame(frame, bg="white")
confirm_password_frame.grid(row=7, column=0, columnspan=2, padx=40, pady=5, sticky="ew")

confirm_password_entry = Entry(confirm_password_frame, show='*', font=('Arial', 12), bd=3, width=20)
confirm_password_entry.pack(side="left", fill="x", expand=True, ipadx=5, ipady=3)

confirm_eye_button = Button(confirm_password_frame, image=eye_open_icon, command=lambda: toggle_password(confirm_password_entry, confirm_eye_button), bd=0, bg='white', activebackground='white')
confirm_eye_button.pack(side="right", padx=5)

# Hide confirm password initially
confirm_password_label.grid_remove()
confirm_password_frame.grid_remove()

# Login/Signup Button
is_login = True
login_button = Button(frame, text="Login", command=login, font=('Arial', 12), bg='grey', fg='white', bd=3)
login_button.grid(row=8, column=0, columnspan=2, padx=40, pady=15, ipadx=15, ipady=5, sticky="ew")

# Toggle Button
toggle_button = Button(frame, text="New to favimark? Register ...", command=toggle_mode, font=('Arial', 10), fg='blue', bg='white', bd=0)
toggle_button.grid(row=9, column=0, columnspan=2, pady=10)

#   FUNCTION TO DISPLAY DASHBOARD OF FAVIMARK
#->CONTAINS 4 BUTTONS AND ONE INTERFACE BELOW IT
#->MADE FULL SCREEN FOR BETTER UI
#->ROOTS IS USED AS THE WINDOW HERE.
       
def dashboard():
    print('dashboard')

#   FUNCTION TO DISPLAY ITEMS IN DASHBOARD
#->CREATES AN INTERFACE TO DISPLAY ITEMS IN SHORT LISTS IF DOESNT EXIST
#->OVERWRITES NEWER DATA FROM DATABASE TO DASHBOARD

def display_items(roots):
    print('display items')
        
def add_item():
    print('add items')

def edit_prompt():
    print('edit items')

def delete_prompt():
    print('delete items')
        
def search_prompt():
    print('search items')
    
mainloop()