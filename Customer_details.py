import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # For logo support
import pandas as pd
import os
import sys

# File Paths
ROOM_BOOKINGS_FILE = "booking_data.xlsx"
HALL_BOOKINGS_FILE = "hall_bookings.xlsx"
FOOD_ORDERS_FILE = "food_orders.xlsx"
LOGO_PATH = r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png"  # Ensure the logo is available

# Get Logged-in Username
username = sys.argv[1] if len(sys.argv) > 1 else "Guest"

# GUI Setup
root = tk.Tk()
root.title("Customer Details - SERENISTAY HOTEL")
root.geometry("950x650")
root.configure(bg="lightblue")

# Header with Hotel Name and Logo
header_frame = tk.Frame(root, bg="lightblue")
header_frame.pack(fill="x", pady=10)

# Load Hotel Logo
try:
    logo_image = Image.open(LOGO_PATH)
    logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)  # Resize logo
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(header_frame, image=logo_photo, bg="lightblue")
    logo_label.pack(side="left", padx=10)
except Exception as e:
    print("Error loading logo:", e)

# Hotel Name
tk.Label(header_frame, text="SERENISTAY HOTEL", font=("Arial", 22, "bold"), bg="lightblue", fg="darkblue").pack(
    side="left")
tk.Label(header_frame, text=f"Customer: {username}", font=("Arial", 14, "bold"), bg="lightblue").pack(side="right",
                                                                                                      padx=20)

# Dropdown Menu to Select Booking Type
selection_var = tk.StringVar()
selection_var.set("Room Booking")

options = ["Room Booking", "Hall Booking", "Food Orders"]
dropdown = ttk.Combobox(root, textvariable=selection_var, values=options, font=("Arial", 12), state="readonly")
dropdown.pack(pady=5)

# Table for Displaying Information
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=20, pady=10)

tree = ttk.Treeview(table_frame, columns=("ID", "Details", "Status"), show="headings", height=10)
tree.heading("ID", text="Booking ID / Order No")
tree.heading("Details", text="Details")
tree.heading("Status", text="Status")
tree.column("ID", width=150)
tree.column("Details", width=500)
tree.column("Status", width=150)
tree.pack(fill="both", expand=True)


# Function to Load Data
def load_data():
    tree.delete(*tree.get_children())  # Clear existing rows
    selection = selection_var.get()

    if selection == "Room Booking":
        file_path = ROOM_BOOKINGS_FILE
    elif selection == "Hall Booking":
        file_path = HALL_BOOKINGS_FILE
    else:
        file_path = FOOD_ORDERS_FILE

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)

        # Filter Data for Logged-in User
        if "Username" in df.columns:
            df = df[df["Username"] == username]

        if not df.empty:
            for _, row in df.iterrows():
                booking_id = row["Booking ID"] if "Booking ID" in row else row["Order No"]
                details = row.to_dict()
                details_str = ", ".join(
                    [f"{k}: {v}" for k, v in details.items() if k not in ["Username", "Booking ID", "Order No"]])
                status = row["Status"] if "Status" in row else "Confirmed"
                tree.insert("", "end", values=(booking_id, details_str, status))
        else:
            messagebox.showinfo("No Records", "No records found for this category.")


# Load data initially
load_data()


# Function to Cancel Booking
def cancel_order():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select an order to cancel!")
        return

    item_values = tree.item(selected_item, "values")
    order_id = item_values[0]

    selection = selection_var.get()

    if selection == "Room Booking":
        file_path = ROOM_BOOKINGS_FILE
    elif selection == "Hall Booking":
        file_path = HALL_BOOKINGS_FILE
    else:
        file_path = FOOD_ORDERS_FILE

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)

        # Check if ID Exists
        if "Booking ID" in df.columns and order_id in df["Booking ID"].values:
            df.loc[df["Booking ID"] == order_id, "Status"] = "Cancelled"
        elif "Order No" in df.columns and order_id in df["Order No"].values:
            df.loc[df["Order No"] == order_id, "Status"] = "Cancelled"
        else:
            messagebox.showerror("Error", "Order not found!")
            return

        df.to_excel(file_path, index=False)

        messagebox.showinfo("Success", "Order Cancelled Successfully!")
        load_data()


# Buttons
btn_frame = tk.Frame(root, bg="lightblue")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Load Data", font=("Arial", 12), command=load_data).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Cancel Order", font=("Arial", 12), bg="red", fg="white", command=cancel_order).grid(row=0,
                                                                                                               column=1,
                                                                                                               padx=10)


# Back Button
def go_back():
    root.destroy()


tk.Button(root, text="Back", font=("Arial", 12), bg="gray", fg="white", command=go_back).pack(pady=10)

root.mainloop()