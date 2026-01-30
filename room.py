import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import re
import random
import pandas as pd
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser
from PIL import Image, ImageTk
import sys
from datetime import date

# Get logged-in user
logged_in_user = sys.argv[1] if len(sys.argv) > 1 else "Guest"

# Fixed rates for each room type
room_types = {"Single": 1000, "Double": 2000, "Deluxe": 3000, "Suite": 5000}
available_rooms = [101, 102, 103, 104, 105]
id_proof_options = ["Aadhar", "Passport", "Driving License", "PAN"]

def generate_booking_id():
    return "RM" + str(random.randint(1000, 9999))

def validate_mobile():
    mobile = entry_contact.get()
    if not re.fullmatch(r"\d{10}", mobile):
        messagebox.showerror("Error", "Invalid Mobile Number! Must be 10 digits.")
        entry_contact.delete(0, tk.END)

def validate_email():
    email = entry_email.get()
    if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Error", "Invalid Email Format!")
        entry_email.delete(0, tk.END)


def calculate_total():
    room_type = entry_room_type.get()
    num_persons = entry_persons.get()

    if not num_persons.isdigit() or int(num_persons) < 1:
        messagebox.showerror("Error", "Enter a valid number of persons!")
        return

    try:
        checkin_date = entry_checkin_date.get_date()
        checkout_date = entry_checkout_date.get_date()

        if checkin_date >= checkout_date:
            messagebox.showerror("Error", "Check-out date must be after Check-in date!")
            return

        num_days = (checkout_date - checkin_date).days
    except Exception as e:
        messagebox.showerror("Error", "Invalid date selection!")
        return

    room_rate = room_types.get(room_type, 0)
    total_cost = room_rate * int(num_persons) * num_days  # Updated formula

    entry_total_cost.config(state="normal")
    entry_total_cost.delete(0, tk.END)
    entry_total_cost.insert(0, str(total_cost))
    entry_total_cost.config(state="readonly")

def generate_bill():
    booking_id = entry_booking_id.get()
    username = entry_username.get()
    name = entry_name.get()
    contact = entry_contact.get()
    email = entry_email.get()
    room_type = entry_room_type.get()
    num_persons = entry_persons.get()
    total_cost = entry_total_cost.get()
    id_proof = entry_id_proof.get()
    id_number = entry_id_number.get()
    checkin_date = entry_checkin_date.get_date()
    checkout_date = entry_checkout_date.get_date()
    if checkin_date >= checkout_date:
        messagebox.showerror("Error", "Check-out date must be after Check-in date!")
        return
    if not name or not contact or not email or not num_persons:
        messagebox.showerror("Error", "All fields are required!")
        return

    if available_rooms:
        room_number = available_rooms.pop(0)
    else:
        messagebox.showwarning("No Rooms Available", "All rooms are booked!")
        return

    bill_text = f"""
    ---- SERENISTAY HOTEL ----
    Booking ID: {booking_id}
    Username: {username}
    Name: {name}
    Contact: {contact}
    Email: {email}
    Room Type: {room_type}
    Room Number: {room_number}
    No. of Persons: {num_persons}
    Check-in Date: {checkin_date.strftime('%d-%m-%Y')}
    Check-out Date: {checkout_date.strftime('%d-%m-%Y')}
    ID Proof: {id_proof}
    ID Number: {id_number}
    Total Cost: ₹{total_cost}
    Thank you for staying with us!
    """

    def save_to_excel(data):
        file_path = "booking_data.xlsx"
        df = pd.DataFrame([data])

        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_excel(file_path, index=False)

    def save_to_pdf(booking_id, bill_text):
        pdf_file = f"bill_{booking_id}.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)

        # Draw the hotel name
        c.setFont("Helvetica-Bold", 16)
        c.drawString(220, 750, "SERENISTAY HOTEL")

        # Load and place the logo
        logo_path = r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png"  # Update this path
        if os.path.exists(logo_path):
            c.drawImage(logo_path, 50, 720, width=80, height=80)  # Adjust position and size

        # Set font for bill details
        c.setFont("Helvetica", 12)
        y = 680  # Adjusted starting position to avoid overlap with the logo

        for line in bill_text.strip().split("\n"):
            c.drawString(100, y, line)
            y -= 20

        c.save()
        webbrowser.open(pdf_file)

    data = {
        "Booking ID": booking_id,
        "Username": username,
        "Name": name,
        "Contact": contact,
        "Email": email,
        "Room Type": room_type,
        "Room Number": room_number,
        "No. of Persons": num_persons,
        "Check-in Date": checkin_date.strftime('%d-%m-%Y'),
        "Check-out Date": checkout_date.strftime('%d-%m-%Y'),
        "ID Proof": id_proof,
        "ID Number": id_number,
        "Total Cost": total_cost
    }
    save_to_excel(data)
    save_to_pdf(booking_id, bill_text)

    messagebox.showinfo("Bill Generated", bill_text)

def back():
    root.destroy()

root = tk.Tk()
root.title("Hotel Room Booking System")
root.state('zoomed')
root.configure(bg="#e6f7ff")

# Header
header_frame = tk.Frame(root, bg="yellow", height=100)
header_frame.pack(fill="x")

# Logo
logo_path = r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png"
if os.path.exists(logo_path):
    original_logo = Image.open(logo_path)
    resized_logo = original_logo.resize((100, 100))
    logo_img = ImageTk.PhotoImage(resized_logo)
    logo_label = tk.Label(header_frame, image=logo_img, bg="yellow")
    logo_label.place(x=10, y=0)

hotel_name_label = tk.Label(header_frame, text="SERENISTAY HOTEL", font=("Arial", 24, "bold"), bg="yellow")
hotel_name_label.place(relx=0.5, rely=0.5, anchor="center")

# Customer Details Frame
frame_customer = tk.Frame(root, padx=20, pady=20, bg="white", relief="groove", bd=5)
frame_customer.place(x=50, y=120, width=450, height=500)

# Booking Frame
frame_booking = tk.Frame(root, padx=20, pady=20, bg="white", relief="groove", bd=5)
frame_booking.place(x=550, y=120, width=450, height=500)

# Customer Details
tk.Label(frame_customer, text="Customer Details", font=("Arial", 14, "bold"), bg="white").grid(row=0, columnspan=2, pady=10)
tk.Label(frame_customer, text="Booking ID:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w")
entry_booking_id = tk.Entry(frame_customer, font=("Arial", 12))
entry_booking_id.insert(0, generate_booking_id())
entry_booking_id.config(state="readonly")
entry_booking_id.grid(row=1, column=1)
tk.Label(frame_customer, text="Username:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w")
entry_username = tk.Entry(frame_customer, font=("Arial", 12))
entry_username.insert(0, logged_in_user)
entry_username.config(state="readonly")
entry_username.grid(row=2, column=1)
tk.Label(frame_customer, text="Name:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w")
entry_name = tk.Entry(frame_customer, font=("Arial", 12))
entry_name.grid(row=3,column=1)

tk.Label(frame_customer, text="Contact:", font=("Arial", 12), bg="white").grid(row=4, column=0, sticky="w")
entry_contact = tk.Entry(frame_customer, font=("Arial", 12))
entry_contact.grid(row=4, column=1)
entry_contact.bind("<FocusOut>", lambda e: validate_mobile())

tk.Label(frame_customer, text="Email:", font=("Arial", 12), bg="white").grid(row=5, column=0, sticky="w")
entry_email = tk.Entry(frame_customer, font=("Arial", 12))
entry_email.grid(row=5, column=1)
entry_email.bind("<FocusOut>", lambda e: validate_email())

tk.Label(frame_customer, text="ID Proof:", font=("Arial", 12), bg="white").grid(row=6, column=0, sticky="w")
entry_id_proof = ttk.Combobox(frame_customer, values=id_proof_options, font=("Arial", 12), state="readonly")
entry_id_proof.grid(row=6, column=1)

tk.Label(frame_customer, text="ID Number:", font=("Arial", 12), bg="white").grid(row=7, column=0, sticky="w")
entry_id_number = tk.Entry(frame_customer, font=("Arial", 12))
entry_id_number.grid(row=7, column=1)

# Booking Details
tk.Label(frame_booking, text="Booking Details", font=("Arial", 14, "bold"), bg="white").grid(row=0, columnspan=2, pady=10)

tk.Label(frame_booking, text="Room Type:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w")
entry_room_type = ttk.Combobox(frame_booking, values=list(room_types.keys()), font=("Arial", 12), state="readonly")
entry_room_type.grid(row=1, column=1)

tk.Label(frame_booking, text="No. of Persons:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w")
entry_persons = tk.Entry(frame_booking, font=("Arial", 12))
entry_persons.grid(row=2, column=1)

tk.Label(frame_booking, text="Check-in Date:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w")
entry_checkin_date = DateEntry(frame_booking, font=("Arial", 12), date_pattern="dd-mm-yyyy")
entry_checkin_date.grid(row=3, column=1)

tk.Label(frame_booking, text="Check-out Date:", font=("Arial", 12), bg="white").grid(row=4, column=0, sticky="w")
entry_checkout_date = DateEntry(frame_booking, font=("Arial", 12), date_pattern="dd-mm-yyyy")
entry_checkout_date.grid(row=4, column=1)


tk.Label(frame_booking, text="Total Cost:", font=("Arial", 12), bg="white").grid(row=5, column=0, sticky="w")
entry_total_cost = tk.Entry(frame_booking, font=("Arial", 12), state="readonly")
entry_total_cost.grid(row=5, column=1)

btn_calculate = tk.Button(frame_booking, text="Calculate Cost", font=("Arial", 12), command=calculate_total)
btn_calculate.grid(row=6, columnspan=2, pady=10)

btn_generate = tk.Button(root, text="Generate Bill", font=("Arial", 14), bg="blue", fg="white", command=generate_bill)
btn_generate.place(x=650, y=620)

btn_back = tk.Button(root, text="Back", font=("Arial", 14), bg="red", fg="white", command=back)
btn_back.place(x=800, y=620)

root.mainloop()