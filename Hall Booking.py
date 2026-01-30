import subprocess
import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkcalendar import DateEntry
import pandas as pd
import os
import random
from datetime import datetime
from fpdf import FPDF
import webbrowser
import sys

logged_in_user=sys.argv[1] if len(sys.argv)>1 else "Guest"
# File path for hall booking data
FILE_PATH = "hall_bookings.xlsx"
def back():
    root.destroy()
    subprocess.Popen(["python","hotel.py",logged_in_user])
# Available halls
PARTY_HALLS = ['P1', 'P2', 'P3']
CONFERENCE_HALLS = ['C1', 'C2']

# Ensure the Excel file exists with correct column headers
if not os.path.exists(FILE_PATH):
    df = pd.DataFrame(columns=["Username","Booking ID", "Name", "Contact", "Date", "Hours", "Guests", "Hall Type", "Hall Number",
                               "Estimated Cost ($)"])
    df.to_excel(FILE_PATH, index=False)


# Function to generate a unique Booking ID
def generate_booking_id():
    return "HB" + str(random.randint(1000, 9999))


# Function to check if a hall is available on a given date
def check_hall_availability(hall_number, date):
    if os.path.exists(FILE_PATH):
        hall_df = pd.read_excel(FILE_PATH)
        # Ensure necessary columns exist
        if "Hall Number" in hall_df.columns and "Date" in hall_df.columns:
            existing_bookings = hall_df[(hall_df["Hall Number"] == hall_number) & (hall_df["Date"] == date)]
            return existing_bookings.empty  # Returns True if hall is available
    return True  # Hall is available if no file exists


# Function to save booking data
def save_to_excel(data):
    df = pd.DataFrame([data])
    if os.path.exists(FILE_PATH):
        existing_df = pd.read_excel(FILE_PATH)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_excel(FILE_PATH, index=False)


# Function to book a hall
def book_hall():
    name = name_var.get().strip()
    contact = contact_var.get().strip()
    date = date_var.get()
    hours = hours_var.get().strip()
    guests = guests_var.get().strip()
    hall_type = hall_type_var.get().strip()

    # Input validation
    if not (name and contact and date and hours and guests and hall_type):
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    if not (contact.isdigit() and len(contact) == 10):
        messagebox.showwarning("Input Error", "Contact number must be 10 digits!")
        return
    if not hours.isdigit() or not guests.isdigit():
        messagebox.showwarning("Input Error", "Hours and Guests must be numbers!")
        return

    # Assign hall based on type
    available_halls = PARTY_HALLS if hall_type == "Party" else CONFERENCE_HALLS
    available_halls = [hall for hall in available_halls if check_hall_availability(hall, date)]

    if not available_halls:
        messagebox.showwarning("No Available Halls", f"No available {hall_type} halls for the selected date.")
        return

    hall_number = available_halls[0]  # Assign the first available hall
    booking_id = generate_booking_id()
    estimated_cost = int(hours) * int(guests) * 10  # Cost calculation

    # Save booking details
    booking_data = {
        "Username":logged_in_user,
        "Booking ID": booking_id,
        "Name": name,
        "Contact": contact,
        "Date": date,
        "Hours": hours,
        "Guests": guests,
        "Hall Type": hall_type,
        "Hall Number": hall_number,
        "Estimated Cost ($)": estimated_cost
    }
    save_to_excel(booking_data)

    # Generate PDF receipt
    generate_pdf_receipt(booking_data)

    messagebox.showinfo("Success", f"Hall {hall_number} booked successfully!\nBooking ID: {booking_id}")
    clear_entries()

# Function to generate and open PDF receipt
def generate_pdf_receipt(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "SERENISTAY HOTEL", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Hall Booking Receipt", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0,10,f"Username:{logged_in_user}",ln=True)
    for key, value in data.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)

    receipt_filename = f"Hall_Booking_{data['Booking ID']}.pdf"
    pdf.output(receipt_filename)

    # Open the PDF in the default browser
    try:
        if os.name == 'nt':  # For Windows
            os.startfile(receipt_filename)
        else:  # For Mac/Linux
            webbrowser.open_new(receipt_filename)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open PDF: {e}")
# Function to clear input fields
def clear_entries():
    name_var.set("")
    contact_var.set("")
    date_var.set("")
    hours_var.set("")
    guests_var.set("")
    hall_type_var.set("")


# Create main application window
root = tk.Tk()
root.title("Hall Booking System - SERENISTAY HOTEL")
root.state('zoomed')
root.configure(bg="#f0f0f0")

# Header Frame for Logo & Hotel Name
header_frame = tk.Frame(root, bg="#f0f0f0", pady=10)
header_frame.pack(fill="x", padx=20)

# Load and Resize Hotel Logo
try:
    logo_image = PhotoImage(file=r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png")
    small_logo = logo_image.subsample(5, 5)
    logo_label = tk.Label(header_frame, image=small_logo, bg="#f0f0f0")
    logo_label.pack(side="left", padx=10)
except Exception as e:
    print("Logo not found:", e)

hotel_name_label = tk.Label(header_frame, text="SERENISTAY HOTEL", font=("Arial", 22, "bold"), bg="#f0f0f0", fg="blue")
hotel_name_label.pack(side="left", padx=10)

# Title
tk.Label(root, text="Hall Booking System", font=("Arial", 20, "bold"), bg="blue", fg="white").pack(pady=5, fill="x")
# *Display Logged-in Username*

logged_in_user =sys.argv[1] if len(sys.argv)>1 else "Guest"
username_label = tk.Label(root, text=f"Logged in as: {logged_in_user}", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="black")
username_label.pack(pady=10)
# Form Fields Frame
frame = tk.Frame(root, bg="white", padx=30, pady=20, relief="ridge", borderwidth=3)
frame.pack(pady=20)

fields = [
    ("Name:", name_var := tk.StringVar()),
    ("Contact:", contact_var := tk.StringVar()),
    ("Date:", date_var := tk.StringVar(), DateEntry),
    ("Hours:", hours_var := tk.StringVar()),
    ("Guests:", guests_var := tk.StringVar()),
    ("Hall Type:", hall_type_var := tk.StringVar(), ["Party", "Conference"])
]

for i, (label, var, *extra) in enumerate(fields):
    tk.Label(frame, text=label, font=("Arial", 14), bg="white").grid(row=i, column=0, padx=10, pady=5, sticky="e")
    if extra:
        if isinstance(extra[0], list):  # Dropdown
            option_menu = tk.OptionMenu(frame, var, *extra[0])
            option_menu.config(font=("Arial", 12), width=15)
            option_menu.grid(row=i, column=1, padx=10, pady=5)
        else:  # Date picker
            extra[0](frame, textvariable=var, font=("Arial", 12), width=17).grid(row=i, column=1, padx=10, pady=5)
    else:
        tk.Entry(frame, textvariable=var, font=("Arial", 12)).grid(row=i, column=1, padx=10, pady=5)

tk.Button(frame, text="Book Hall", font=("Arial", 14), bg="green", fg="white", width=15, command=book_hall).grid(
    row=len(fields), columnspan=2, pady=15)
btn_back = tk.Button(root, text="Back", font=("Arial", 14), bg="red", fg="white", command=back)
btn_back.place(x=600, y=600)


root.mainloop()