from tkinter import*
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import uuid

text_widget=None
current_user_id=None

# Function to toggle password visibility
def toggle_password(entry, button):
    """Toggle password visibility and change eye button icon"""
    if entry.cget('show') == '*':
        entry.config(show='')  # Show password
        button.config(image=eye_closed_icon)  # Change to closed eye
        button.image = eye_closed_icon  # Prevent garbage collection
    else:
        entry.config(show='*')  # Hide password
        button.config(image=eye_open_icon)  # Change to open eye
        button.image = eye_open_icon  # Prevent garbage collection

# Function to toggle between Login and Register
def toggle_mode():
    global is_login
    is_login = not is_login
    title_label.config(text="LOG IN / SIGN IN" if is_login else "SIGN UP / REGISTER")
    login_button.config(text="Login" if is_login else "Sign Up", command=login if is_login else register)
    toggle_button.config(text="New to favimark? Register ..." if is_login else "Already Registered? Sign In ...")
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    confirm_password_entry.delete(0,END)
    
    # Show/hide confirm password field dynamically
    if is_login:
        confirm_password_label.grid_remove()
        confirm_password_frame.grid_remove()
        frame.place(relwidth=0.6, relheight=0.7)  # Resize frame for login
    else:
        confirm_password_label.grid()
        confirm_password_frame.grid()
        frame.place(relwidth=0.6, relheight=0.8)  # Resize frame for signup

def login():
    global current_user_id
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("favimark.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            current_user_id = user[0]
            print(f"user {current_user_id} logged in") #Debugging Purposes
            root.iconify() #imp
            dashboard()
        else:
            response = messagebox.askyesno("User Not Found", "Username does not exist. Do you want to sign up?")
            if response:  # If "Yes" is clicked
                toggle_mode()  # Switch to the signup screen

    except sqlite3.OperationalError as e:
            response = messagebox.askyesno("User Not Found", "User does not exist. Do you want to sign up?")
            if response:  # If "Yes" is clicked
                toggle_mode()  # Switch to the signup screen
    finally:
        conn.close()

def register():
    # Retrieve data from entry fields
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Check if fields are empty
    if username == "" or password == "" or confirm_password == "":
        messagebox.showerror("Error", "Fields cannot be empty")
        return

    # Check if passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match")
        return

    # Generate a unique user ID
    user_id = str(uuid.uuid4())[:8]

    try:
        # Connect to the database
        conn = sqlite3.connect("favimark.db")
        cursor = conn.cursor()

        # Create the users and favourites tables if they don't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id TEXT PRIMARY KEY, 
                            username TEXT UNIQUE, 
                            password TEXT)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS favourites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT, 
                    user_record_id INTEGER,  -- Unique record ID per user
                    fav_name TEXT, 
                    fav_type TEXT, 
                    fav_description TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(user_id))''')

        # Insert user data into the users table
        cursor.execute("INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)", 
                       (user_id, username, password))

        conn.commit()

        messagebox.showinfo("Success", "Registration Successful! Please log in.")
        toggle_mode() 

    except sqlite3.IntegrityError:
        # Catch integrity errors like duplicate usernames
        messagebox.showerror("Error", "Username already exists")
    except sqlite3.Error as e:
        # Catch any other database-related errors
        messagebox.showerror("Database Error", f"An error occurred: {e}")
    finally:
        # Ensure connection is closed
        conn.close()

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
    global roots  # Giving roots window a global scope to access it from other windows
    roots = Toplevel(root)
    roots.state('zoomed')
    roots.title("favimark/Dashboard")

    # Align everything at the top of the page
    top_frame = Frame(roots, bg='white')
    top_frame.pack(side=TOP, fill=BOTH, padx=1, pady=10, expand=True)

    # UI for buttons which aligns CRUD buttons at the top of the page using top_frame
    button_frame_crud = Frame(top_frame, bg='white')
    button_frame_crud.pack(side=LEFT, fill=X)  # Use fill=X to stretch horizontally

    # Use grid layout for buttons and align them to the left side
    add_button = Button(button_frame_crud, text="ADD", command=add_item, font=('Arial', 12), bg='grey', fg='white', bd=3)
    add_button.grid(row=0, column=0, padx=10, sticky='w')  # Align left

    edit_button = Button(button_frame_crud, text="EDIT", command=edit_prompt, font=('Arial', 12), bg='grey', fg='white', bd=3)
    edit_button.grid(row=0, column=1, padx=10, sticky='w')  # Align left

    search_button = Button(button_frame_crud, text=" SEARCH ", command=search_prompt, font=('Arial', 12), bg='grey', fg='white', bd=3)
    search_button.grid(row=0, column=2, padx=10, sticky='w')  # Align left

    delete_button = Button(button_frame_crud, text="DELETE", command=delete_prompt, font=('Arial', 12), bg='grey', fg='white', bd=3)
    delete_button.grid(row=0, column=3, padx=10, sticky='w')  # Align left

    # UI for exit button
    button_frame_exit = Frame(top_frame, bg='white')
    button_frame_exit.pack(side=RIGHT, fill=X, padx=10)  # This frame is only for the exit button

    # Load exit button image (exit.png should be in the same directory or specify the full path)
    exit_image = Image.open('exit.png').resize((50, 50))  # Make sure exit.png is in the correct location
    exit_icon = ImageTk.PhotoImage(exit_image)

    # Create an Exit button with the image
    exit_button = Button(button_frame_exit, image=exit_icon, command=logout, bd=0)
    exit_button.image = exit_icon  # Keep a reference to the image to prevent garbage collection

    # Grid the exit button in the far-right position
    exit_button.grid(row=0, column=999, padx=10, sticky='e')  # column=999 will push it to the far-right
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    # Display the items in the dashboard (assuming this function works as intended)
    display_items(roots)

#   FUNCTION TO DISPLAY ITEMS IN DASHBOARD
#->CREATES AN INTERFACE TO DISPLAY ITEMS IN SHORT LISTS IF DOESNT EXIST
#->OVERWRITES NEWER DATA FROM DATABASE TO DASHBOARD

def display_items(roots):
    global text_widget  # Declare text_widget as global to access it across functions
    # Create frame and text widget with scrollbar as before
    item_frame = Frame(roots)
    item_frame.pack(fill=BOTH, expand=True)

    text_widget = Text(item_frame, wrap=WORD, width=100, height=50)
    text_widget.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(item_frame, orient=VERTICAL, command=text_widget.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    text_widget.config(yscrollcommand=scrollbar.set)
        
#   FUNCTION TO ADD ITEMS TO DATABASE
#->CREATES A NEW WINDOW FOR ADDING ITEMS TO DATABASE
#->ASKS FOR ITEM NAME, TYPE AND DESCRIPTION
#->ADDS ITEM TO DATABASE IF ALL FIELDS ARE FILLED
#->IF ANY FIELD IS LEFT BLANK, A MESSAGE BOX APPEARS
#->UPON COMPLETION, SUCCESSFUL ADDITION MESSAGE BOX APPEARS
#->AFTER CLICKING OK ON IT, ADD WINDOW CLOSES AND DASHBOARD REDIRECTION
        
def add_item():
    global newe1, newe2, newe3, additem
    additem = Toplevel()
    additem.geometry('400x400')
    additem.iconbitmap('add.ico')
    additem.title("favimark/ADD-ITEMS")
    name_label=Label(additem,text="Mark your favourites",)
    name_label.pack(pady=10)
    newe1=Entry(additem,bd=5)
    newe1.pack()
    type_label=Label(additem,text="Type (Book/Movie/Anime/Manga/Manhua/Shows)")
    type_label.pack(pady=10)
    newe2=Entry(additem,bd=5)
    newe2.pack()
    desc_label=Label(additem,text="Review. eg:Good/Decent/Excellent")
    desc_label.pack(pady=10)
    newe3=Entry(additem,bd=5)
    newe3.pack()
    addnew=Button(additem,text=" ADD ",command=create, bg='grey', fg='white',bd=5)
    addnew.pack(pady=20)
    
#   SUB-FUNCTION OF ADD ITEM FUNCTIONALITY
#-> ADDS ITEMS TO THE DATABASE
#-> THIS FUNCTION PROVIDES THE SUCCESFUL COMPLETION MESSAGE BOX.

def create():

    # Check if any field is empty
    if not newe1.get() or not newe2.get() or not newe3.get():
        # If any field is empty, show a warning message
        messagebox.showwarning("Input Error", "Please enter values for all fields.")
        return  # Do not add the record if fields are empty

    try:
        # Connect to the database
        conn = sqlite3.connect('favimark.db')
        c = conn.cursor()

        # Create table if it doesn't exist (already done earlier)
        c.execute('''
            CREATE TABLE IF NOT EXISTS favourites(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                fav_name TEXT,
                fav_type TEXT,
                fav_description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        # Get the next record number for the user
        c.execute("SELECT COALESCE(MAX(user_record_id), 0) + 1 FROM favourites WHERE user_id=?", (current_user_id,))
        next_record_id = c.fetchone()[0]

        # Insert new record with the user-specific record ID
        c.execute('INSERT INTO favourites (user_id, user_record_id, fav_name, fav_type, fav_description) VALUES (?, ?, ?, ?, ?)',
                (current_user_id, next_record_id, newe1.get(), newe2.get(), newe3.get()))


        # Commit the transaction and close the connection
        conn.commit()

        # Success message
        messagebox.showinfo('Success', 'Item created successfully')
        
        # Close the connection
        conn.close()

        # Refresh the displayed items to show the new item
        display_items(roots)

        # Clear the input fields
        newe1.delete(0, END)
        newe2.delete(0, END)
        newe3.delete(0, END)

        # Close the add item window
        additem.destroy()

    except sqlite3.Error as e:
        # Handle any errors during database interaction
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def edit_prompt():
    print('edit items')

def delete_prompt():
    print('delete items')
        
def search_prompt():
    print('search items')
    
def logout():
    global current_user_id
    exit=messagebox.askyesno('Logout_prompt','Do you want to logout?')
    if exit:
        current_user_id = None  # Reset current user
        roots.destroy()  # Close the dashboard window
        root.deiconify()
    
mainloop()