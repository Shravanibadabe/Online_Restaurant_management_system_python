from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import re  # For password validation
import os
import pandas as pd



# Initialize main window
root = Tk()
root.title("Login - SereniStay Hotel")
root.state("zoomed")
root.geometry("400x500")
root.configure(bg="white")

# Load and resize logo
def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

hotel_logo = load_image(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png", (80, 80))

# Header
header_frame = Frame(root, bg="white")
header_frame.pack(pady=10)

Label(header_frame, image =hotel_logo, bg="white").pack()
Label(header_frame, text="SereniStay Hotel", font=("Arial", 20, "bold"), fg="#2c3e50", bg="white").pack()

# Clear previous panels
def clear_panels():
    for widget in root.winfo_children():
        if widget != header_frame:
            widget.destroy()

# Password validation function
def validate_password(password):
    """ Check if the password meets security conditions """
    if (len(password) < 8 or
            not re.search(r"[A-Z]", password) or
            not re.search(r"[a-z]", password) or
            not re.search(r"[0-9]", password) or
            not re.search(r"[@#$%^&*!]", password)):
        return False
    return True
def open_dashboard():
    root.destroy()

# Run the application
# Login Panel
def login_panel():
    clear_panels()

    frame = Frame(root, bg="white", bd=2, relief="solid")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

    Label(frame, text="Login", font=("Arial", 16, "bold"), fg="#2c3e50", bg="white").pack(pady=10)

    Label(frame, text="Username:", bg="white").pack(anchor="w", padx=20, pady=2)
    entry_username = Entry(frame, width=35)
    entry_username.pack(pady=2)

    Label(frame, text="Password:", bg="white").pack(anchor="w", padx=20, pady=2)
    entry_password = Entry(frame, width=35, show="*")
    entry_password.pack(pady=2)
    logged_in_user=""
    import time
    import os
    import tkinter as tk
    from tkinter import messagebox

    def special_transition(next_panel):
        """Expands the login panel slightly, then fades out smoothly before switching."""
        step = 0
        while step < 15:
            new_width = root.winfo_width() + 10
            new_height = root.winfo_height() + 5
            root.geometry(f"{new_width}x{new_height}")
            root.attributes("-alpha", 1 - step * 0.05)  # Decrease opacity
            root.update()
            time.sleep(0.05)
            step += 1

        root.destroy()  # Close login window
        os.system(f"python {next_panel}")  # Open main dashboard

    def login():
        global logged_in_user
        username = entry_username.get().strip()
        password = entry_password.get().strip()

        # Hardcoded Admin Credentials
        ADMIN_USERNAME = "admin"
        ADMIN_PASSWORD = "Admin@22"

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            messagebox.showinfo("Success", "Admin login successful!")
            special_transition("staff_panel.py")  # Smooth transition before opening staff panel
            return

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        file_path = "users.xlsx"
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            user_row = df[df["Username"] == username]

            if not user_row.empty and user_row.iloc[0]["Password"] == password:
                logged_in_user = username
                messagebox.showinfo("Success", "Login successful!")
                special_transition(f"hotel.py {logged_in_user}")  # Smooth transition before opening hotel dashboard
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        else:
            messagebox.showerror("Error", "No users registered!")
    Button(frame, text="Login", font=("Arial", 12), bg="#28a745", fg="white", command=login).pack(pady=10)

    btn_frame = Frame(frame, bg="white")
    btn_frame.pack(pady=5)

    Button(btn_frame, text="New Registration", font=("Arial", 10), fg="#007bff", bg="white", bd=0,
           command=registration_panel).grid(row=0, column=0, padx=5)

    Button(btn_frame, text="Forgot Password?", font=("Arial", 10), fg="#dc3545", bg="white", bd=0,
           command=forgot_password_panel).grid(row=0, column=1, padx=5)
    # Back to Login Button
    Button(frame, text="Back", font=("Arial", 10), bg="#6c757d", fg="white",
           command=open_dashboard).pack(pady=5)

# Registration Panel
def registration_panel():
    clear_panels()

    frame = Frame(root, bg="white", bd=2, relief="solid")
    frame.place(relx=0.5, rely=0.6, anchor="center", width=450, height=550)

    Label(frame, text="Register", font=("Arial", 16, "bold"), fg="#2c3e50", bg="white").pack(pady=10)

    fields = ["Full Name", "Contact Number", "Email", "Username", "Password", "Security Question", "Security Answer"]
    entries = {}

    for field in fields:
        Label(frame, text=f"{field}:", bg="white").pack(anchor="w", padx=20, pady=2)
        entry = Entry(frame, width=40, show="*" if field == "Password" else "")
        entry.pack(pady=2)
        entries[field] = entry

    def validate_contact(contact):
        """Ensures the contact number is exactly 10 digits and numeric"""
        return bool(re.fullmatch(r"\d{10}", contact))

    def validate_email(email):
        """Checks if the email format is valid"""
        return bool(re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))

    def validate_password(password):
        """Checks if password meets security criteria"""
        return bool(re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&*!]).{8,}$", password))

    def register():
        user_data = {field: entries[field].get().strip() for field in fields}

        if any(value == "" for value in user_data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Validate contact number
        if not validate_contact(user_data["Contact Number"]):
            messagebox.showerror("Error", "Invalid contact number! Must be exactly 10 digits.")
            return

        # Validate email format
        if not validate_email(user_data["Email"]):
            messagebox.showerror("Error", "Invalid email format! Example: user@example.com")
            return

        # Validate password
        if not validate_password(user_data["Password"]):
            messagebox.showerror("Error", "Password must be at least 8 characters long, "
                                          "include an uppercase letter, a lowercase letter, "
                                          "a number, and a special character (@_#$%^&*! etc.).")
            return

        file_path = "users.xlsx"

        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            # Prevent duplicate usernames
            if user_data["Username"] in df["Username"].values:
                messagebox.showerror("Error", "Username already exists! Choose a different username.")
                return
        else:
            df = pd.DataFrame(columns=fields)

        # Convert user_data dictionary into a DataFrame with a single row
        new_user_df = pd.DataFrame([user_data])

        # Concatenate the new user to the existing DataFrame
        df = pd.concat([df, new_user_df], ignore_index=True)

        # Save updated DataFrame to Excel
        df.to_excel(file_path, index=False)

        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        login_panel()

    Button(frame, text="Register", font=("Arial", 12), bg="#007bff", fg="white", command=register).pack(pady=10)
    # Back to Login Button
    Button(frame, text="Back to Login", font=("Arial", 10), bg="#6c757d", fg="white",
           command=login_panel).pack(pady=5)
# Forgot Password Panel
def forgot_password_panel():
    clear_panels()

    frame = Frame(root, bg="white", bd=2, relief="solid")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=450)

    Label(frame, text="Reset Password", font=("Arial", 16, "bold"), fg="#2c3e50", bg="white").pack(pady=10)

    Label(frame, text="Username:", bg="white").pack(anchor="w", padx=20, pady=2)
    entry_username = Entry(frame, width=35)
    entry_username.pack(pady=2)

    security_question_label = Label(frame, text="", bg="white", font=("Arial", 10, "italic"))
    security_question_label.pack(pady=5)

    entry_security_answer = Entry(frame, width=35)
    entry_security_answer.pack(pady=2)
    entry_security_answer.pack_forget()  # Initially hidden

    entry_new_password = Entry(frame, width=35, show="*")
    entry_new_password.pack(pady=2)
    entry_new_password.pack_forget()  # Initially hidden

    def validate_password(password):
        """Checks if password meets security criteria"""
        if len(password) < 8:
            return "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", password):
            return "Password must include at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return "Password must include at least one lowercase letter."
        if not re.search(r"\d", password):
            return "Password must include at least one number."
        if not re.search(r"[@#_$%^&*!]", password):
            return "Password must include at least one special character (@#_$%^&*!)."
        return None  # No errors

    def fetch_security_question():
        username = entry_username.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter your username!")
            return

        file_path = "users.xlsx"
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            user_row = df[df["Username"] == username]

            if not user_row.empty:
                security_question = user_row.iloc[0]["Security Question"]
                security_question_label.config(text=f"Security Question: {security_question}")
                entry_security_answer.pack(pady=2)
                btn_verify.pack(pady=5)  # Show Verify button
            else:
                messagebox.showerror("Error", "Username not found!")
        else:
            messagebox.showerror("Error", "No users registered!")

    def verify_security_answer():
        username = entry_username.get().strip()
        security_answer = entry_security_answer.get().strip()

        file_path = "users.xlsx"
        df = pd.read_excel(file_path)
        user_row = df[df["Username"] == username]

        if not user_row.empty and user_row.iloc[0]["Security Answer"] == security_answer:
            entry_new_password.pack(pady=2)
            btn_reset.pack(pady=5)  # Show Reset Password button
        else:
            messagebox.showerror("Error", "Incorrect security answer!")

    def reset_password():
        username = entry_username.get().strip()
        new_password = entry_new_password.get().strip()

        if not new_password:
            messagebox.showerror("Error", "Please enter a new password!")
            return

        # Validate the new password
        password_error = validate_password(new_password)
        if password_error:
            messagebox.showerror("Error", password_error)
            return

        file_path = "users.xlsx"
        df = pd.read_excel(file_path)
        df.loc[df["Username"] == username, "Password"] = new_password
        df.to_excel(file_path, index=False)

        messagebox.showinfo("Success", "Password reset successfully!")
        login_panel()

    btn_fetch = Button(frame, text="Fetch Security Question", font=("Arial", 10), bg="#007bff", fg="white",
                       command=fetch_security_question)
    btn_fetch.pack(pady=5)

    btn_verify = Button(frame, text="Verify Answer", font=("Arial", 10), bg="#28a745", fg="white",
                        command=verify_security_answer)
    btn_verify.pack(pady=5)
    btn_verify.pack_forget()  # Initially hidden

    btn_reset = Button(frame, text="Reset Password", font=("Arial", 10), bg="#dc3545", fg="white",
                       command=reset_password)
    btn_reset.pack(pady=5)
    btn_reset.pack_forget()  # Initially hidden
    # Back to Login Button
    btn_back=Button(frame, text="Back to Login", font=("Arial", 10), bg="#6c757d", fg="white",
           command=login_panel)
    btn_back.pack(side="bottom",pady=10)
# Show Login Panel on Start
login_panel()

root.mainloop()