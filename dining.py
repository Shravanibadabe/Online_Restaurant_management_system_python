import tkinter as tk
from tkinter import ttk, messagebox
import os
import pandas as pd
from fpdf import FPDF
from PIL import Image, ImageTk
import sys


# File Paths
ROOM_BOOKINGS_FILE = "booking_data.xlsx"
HALL_BOOKINGS_FILE = "hall_bookings.xlsx"
FOOD_ORDERS_FILE = "food_orders.xlsx"

# Sample Menu
MENU_ITEMS = {
    "Starter": [("Spring Rolls", 150), ("Garlic Bread", 120)],
    "Soup": [("Tomato Soup", 100), ("Sweet Corn Soup", 110)],
    "Indian Bread": [("Butter Naan", 50), ("Stuffed Paratha", 70)],
    "Main Course": [("Paneer Butter Masala", 250), ("Dal Makhani", 200)],
    "Dessert": [("Gulab Jamun", 90), ("Chocolate Brownie", 180)],
    "Beverage": [("Tea", 30), ("Coffee", 50)]
}

username=sys.argv[1] if len(sys.argv)>1 else "Guest"

# GUI Setup
root = tk.Tk()
root.title("Dining Panel - SERENISTAY HOTEL")
root.geometry("1200x700+0+0")
root.state("zoomed")
root.configure(bg="lightblue")

# Left Panel (Customer Info)
left_panel = tk.Frame(root, width=400, bg="lightgray", padx=10, pady=10)
left_panel.pack(side="left", fill="y")

tk.Label(left_panel, text=f"Username:{username}", font=("Arial", 14, "bold"), bg="lightgray",fg="blue").pack(pady=5)
tk.Label(left_panel, text="Customer Information", font=("Arial", 14, "bold"), bg="lightgray").pack()

# Variables
name_var = tk.StringVar()
contact_var = tk.StringVar()
payment_var = tk.StringVar()
booking_id_var = tk.StringVar()

# Hotel Logo
logo_path = r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png"  # Replace with correct path
logo_img = Image.open(logo_path).resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_img)

header_frame = tk.Frame(root, bg="lightblue")
header_frame.pack(fill="x")

tk.Label(header_frame, image=logo_photo, bg="lightblue").pack(side="left", padx=10, pady=10)
tk.Label(header_frame, text="SERENISTAY HOTEL - Dining Panel", font=("Arial", 20, "bold"), bg="lightblue").pack(
    side="left", padx=20)

# Input Fields
tk.Label(left_panel, text="Room Booking ID / Hall Booking ID:", font=("Arial", 12), bg="lightgray").pack()
tk.Entry(left_panel, textvariable=booking_id_var, font=("Arial", 12)).pack()

tk.Label(left_panel, text="Customer Name:", font=("Arial", 12), bg="lightgray").pack()
tk.Entry(left_panel, textvariable=name_var, font=("Arial", 12)).pack()

tk.Label(left_panel, text="Contact:", font=("Arial", 12), bg="lightgray").pack()
tk.Entry(left_panel, textvariable=contact_var, font=("Arial", 12)).pack()

tk.Label(left_panel, text="Payment Method:", font=("Arial", 12), bg="lightgray").pack()
payment_menu = ttk.Combobox(left_panel, textvariable=payment_var, values=["Cash", "Card", "UPI"], font=("Arial", 12),
                            state="readonly")
payment_menu.pack()

# Right Panel (Menu)
right_panel = tk.Frame(root, bg="white", padx=10, pady=10)
right_panel.pack(side="right", fill="both", expand=True)

tk.Label(right_panel, text="Menu", font=("Arial", 14, "bold"), bg="white").pack()

# Food Selection
food_vars = {}
for category, items in MENU_ITEMS.items():
    tk.Label(right_panel, text=category, font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
    for item, price in items:
        var = tk.BooleanVar()
        qty = tk.StringVar(value="1")
        row = tk.Frame(right_panel, bg="white")
        row.pack(anchor="w")
        tk.Checkbutton(row, text=f"{item} - Rs.{price}", variable=var, bg="white").pack(side="left")
        ttk.Spinbox(row, from_=1, to=10, textvariable=qty, width=3, font=("Arial", 12)).pack(side="left")
        food_vars.setdefault(category, []).append((item, var, qty, price))


# Function to Check Booking & Generate Bill
def generate_bill():
    booking_id = booking_id_var.get().strip()
    contact = contact_var.get().strip()

    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("Error", "Please enter a valid 10-digit contact number!")
        return

    # Load booking data
    room_bookings = pd.read_excel(ROOM_BOOKINGS_FILE) if os.path.exists(ROOM_BOOKINGS_FILE) else pd.DataFrame()
    hall_bookings = pd.read_excel(HALL_BOOKINGS_FILE) if os.path.exists(HALL_BOOKINGS_FILE) else pd.DataFrame()

    # Validate Booking ID
    if booking_id not in room_bookings.values and booking_id not in hall_bookings.values:
        messagebox.showerror("Error", "Invalid Room Booking ID or Hall Booking ID!")
        return

    if not name_var.get().strip() or not contact_var.get().strip() or not payment_var.get():
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    total_cost = 0
    ordered_items = []

    for category, items in food_vars.items():
        for item, var, qty, price in items:
            if var.get():
                quantity = int(qty.get()) if qty.get().isdigit() else 0
                if quantity > 0:
                    cost = quantity * price
                    total_cost += cost
                    ordered_items.append((booking_id, name_var.get(), contact, f"{item} x{quantity}", cost, payment_var.get()))

    if not ordered_items:
        messagebox.showwarning("Order Error", "Please select at least one item!")
        return

    # Save order to Excel
    df = pd.DataFrame(ordered_items, columns=["Booking ID", "Customer Name", "Contact", "Ordered Items", "Total Price", "Payment Method"])
    try:
        if os.path.exists(FOOD_ORDERS_FILE):
            existing_df = pd.read_excel(FOOD_ORDERS_FILE, engine="openpyxl")
            df = pd.concat([existing_df, df], ignore_index=True)

        with pd.ExcelWriter(FOOD_ORDERS_FILE, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False)

        messagebox.showinfo("Success", "Order saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save order: {e}")

    # Generate PDF Bill
    try:
        pdf = FPDF()
        pdf.add_page()

        # **Add Hotel Logo**
        logo_path = r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png"  # Update with correct path
        pdf.image(logo_path, x=10, y=10, w=30)  # Adjust x, y, and width as needed

        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "SERENISTAY HOTEL - Dining Bill", ln=True, align="C")
        pdf.ln(20)  # Space after the title

        pdf.set_font("Arial", "B", 12)
        pdf.cell(100, 10, f"Booking ID: {booking_id}", ln=True)
        pdf.cell(100, 10, f"Customer: {name_var.get()}", ln=True)
        pdf.cell(100, 10, f"Contact: {contact_var.get()}", ln=True)
        pdf.cell(100, 10, f"Payment Method: {payment_var.get()}", ln=True)

        pdf.ln(10)
        pdf.cell(60, 10, "Ordered Items", 1)
        pdf.cell(40, 10, "Total Price", 1)
        pdf.ln()

        pdf.set_font("Arial", "", 12)
        for _, _, _, items, total, _ in ordered_items:
            pdf.cell(60, 10, items, 1)
            pdf.cell(40, 10, f"Rs.{total}", 1)
            pdf.ln()

        pdf.cell(100, 10, f"Total Amount: Rs.{total_cost}", 1, ln=True)
        pdf_file = "Dining_Bill.pdf"
        pdf.output(pdf_file, "F")

        os.startfile(pdf_file) if os.name == "nt" else os.system(f"xdg-open {pdf_file}")
        messagebox.showinfo("Success", f"Order Placed Successfully!\nBill saved!")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate bill: {e}")

def back():
    root.destroy()
# Create a frame for the buttons at the bottom of the right panel
button_frame = tk.Frame(right_panel, bg="white")
button_frame.pack(side="bottom", pady=10)
# Submit Order Button
btn_submit = tk.Button(button_frame, text="Submit Order", font=("Arial", 14), command=generate_bill)
btn_submit.pack(side="left", padx=10)
# Back Button
btn_back = tk.Button(button_frame, text="Back", font=("Arial", 14), bg="red", fg="white", command=back)
btn_back.pack(side="left", padx=10)


root.mainloop()