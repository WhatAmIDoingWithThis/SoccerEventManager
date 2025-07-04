import tkinter as tk
import os
from tkinter import messagebox, filedialog
from library.UserManager import UserManager
import bcrypt
from PIL import Image, ImageTk

# These credentials are only to be used if no admin user exists
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Static Variables
ALLOWED_ROLES = ["Coach", "Admin"]
DEFAULT_IMAGE_PATH = "assets/default.jpg"
WIDTH = 640
HEIGHT = 320

# Function that checks if the username and password match an existing admin user
def login():
	username = usernameEntry.get()
	password = passwordEntry.get()
	users = user_manager._load_users()
	
	# If no admins exist, use the hardcoded admin account
	hasAdmins = any(user["role"] == "Admin" for user in users.values())
	if not hasAdmins:
		if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
			messagebox.showinfo("First-Time Admin Login", "Default admin access granted. Please create an admin account.")
			open_user_creation_window()
			return
			
	# If admins exist, match the user to admin account
	user = users.get(username)
	if user and user["role"] == "Admin":
		stored_hash = user["password"]
		if bcrypt.checkpw(password.encode(), stored_hash.encode()):
			open_user_creation_window()
			return
			
	# Login Failure
	messagebox.showerror("Login Failed", "Invalid Credentials")
	
	
		

# Applies GUI for user creation
def open_user_creation_window():
	loginWindow.destroy()
	
	# Attempts to create a new user
	def create_user():
		uname = newUsername.get()
		pwd = newPassword.get()
		if user_manager.create_user(uname, pwd, selectedRole.get(), imagePath.get()):
			messagebox.showinfo("Success", f"User '{uname}' created!")
		else:
			messagebox.showerror("Error", f"User '{uname}' already exists.")
			
	# Shows the user profile picture
	def update_image_preview(path):
		try:
			img = Image.open(path)
		except:
			img = Image.open(DEFAULT_IMAGE_PATH)
			
		img = img.resize((320, 320))
		photo = ImageTk.PhotoImage(img)
		imageLabel.config(image = photo)
		imageLabel.image = photo
			
	# Window creation
	userWindow = tk.Tk()
	center_window(userWindow)
	userWindow.resizable(False, False)
	userWindow.title("Create User")
	
	# Framing
	centerGridFrame = tk.Frame(userWindow)
	centerGridFrame.pack(expand = True)
	leftFrame = tk.Frame(centerGridFrame)
	leftFrame.grid(row = 0, column = 0)
	rightFrame = tk.Frame(centerGridFrame)
	rightFrame.grid(row = 0, column = 1)
	formFrame = tk.Frame(rightFrame)
	formFrame.pack(expand = True)
	
	# Username Entry
	tk.Label(formFrame, text = "Username").pack(padx = 5)
	newUsername = tk.Entry(formFrame)
	newUsername.pack(padx = 5)
	
	# Password Entry
	tk.Label(formFrame, text = "Password").pack(padx = 5)
	newPassword = tk.Entry(formFrame, show = "*")
	newPassword.pack(padx = 5)
	
	# Role Selection
	tk.Label(formFrame, text = "Select Role").pack(padx = 5)
	selectedRole = tk.StringVar()
	selectedRole.set(ALLOWED_ROLES[0]) # Default
	tk.OptionMenu(formFrame, selectedRole, *ALLOWED_ROLES).pack(padx = 5)
	
	# Profile Picture
	tk.Label(formFrame, text = "Profile Picture").pack(padx = 5)
	imagePath = tk.StringVar()
	tk.Button(formFrame, text = "Upload Picture", command = lambda: [upload_image(imagePath), update_image_preview(imagePath.get())]).pack(padx = 5)
	
	# Enter button
	tk.Button(formFrame, text = "Create", command = create_user).pack(padx = 5)
	
	# User Image
	imageLabel = tk.Label(leftFrame)
	imageLabel.pack(expand = True)
	update_image_preview(DEFAULT_IMAGE_PATH)
	
	userWindow.mainloop()
	
# Handles file explorer dialogue
def upload_image(imageVar):
	path = filedialog.askopenfilename(
		title = "Select Profile Picture",
		filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
	)
	if path:
		imageVar.set(path)
		
# Takes the window and centers it on the users screen
def center_window(window, width = WIDTH, height = HEIGHT):
	screenWidth = window.winfo_screenwidth()
	screenHeight = window.winfo_screenheight()
	
	x = (screenWidth - width) // 2
	y = (screenHeight - height) // 2
	
	window.geometry(f"{width}x{height}+{x}+{y}")

	
# ------------------------------------- GUI For Login -------------------------

# Window creation and naming
loginWindow = tk.Tk()
center_window(loginWindow)
loginWindow.resizable(False, False)
loginWindow.title("Admin Login")

user_manager = UserManager("data/users.json")

# Center frame
loginFrame = tk.Frame(loginWindow)
loginFrame.pack(expand = True)

# Username entry
tk.Label(loginFrame, text = "Username").pack(pady = 5)
usernameEntry = tk.Entry(loginFrame)
usernameEntry.pack(pady = 5)

# Password Entry
tk.Label(loginFrame, text = "Password").pack(pady = 5)
passwordEntry = tk.Entry(loginFrame)
passwordEntry.pack(pady = 5)

# Enter button
tk.Button(loginFrame, text = "Login", command = login).pack(pady = 5)


loginWindow.mainloop()