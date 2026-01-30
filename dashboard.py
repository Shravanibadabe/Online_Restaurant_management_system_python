from tkinter import *
from tkinter import ttk, messagebox
from tkinter.messagebox import showinfo
import tkinter as tk
from Chatbot import Chatbot
from PIL import Image, ImageTk
import os
import itertools
import pandas as pd

# Initialize main window
root = Tk()
root.title("Hotel Management System - SereniStay Hotel")
root.geometry("1366x768")
root.state("zoomed")
root.configure(bg="#f4f4f4")  # Light background color


# Function to clear panels
def clear_panels():
    for widget in root.winfo_children():
        if widget not in (header_frame, footer_frame, menu_frame):
            widget.destroy()
        menu_frame.lift()



# Load and resize images
def load_image(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


# Header with Logo and Menu
header_frame = Frame(root, bg="#D4E6F1", height=80, bd=2, relief="solid")
header_frame.pack(fill="x")

hotel_logo = load_image(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png", (80, 80))
Label(header_frame, image=hotel_logo, bg="#f8f9fa").pack(side="left", padx=20)

Label(header_frame, text="SERENISTAY HOTEL", font=("Georgia", 24, "bold"), fg="#154360", bg="#D4E6F1").place(relx=0.5,rely=0.5,anchor="center")


# Sidebar Menu
def toggle_menu():
    if menu_frame.winfo_ismapped():
        menu_frame.place_forget()
    else:
        menu_frame.place(x=root.winfo_width() - 220, y=80)  # Show menu on top-right
        menu_frame.lift()


menu_icon = Button(header_frame, text="☰", font=("Arial", 20, "bold"), bg="#f8f9fa", fg="#2c3e50", bd=0,
                   command=toggle_menu)
menu_icon.pack(side="right", padx=20)

menu_frame = Frame(root, bg="#e9ecef", width=200, height=220, bd=2, relief="solid")


def open_login():
    os.system("python login.py")


menu_options = [
    ("Login/Registration", open_login),
    ("Review", lambda: review_panel()),
    ("About Us", lambda: about_us_panel()),
    ("Contact", lambda: contact_panel())

]

for text, command in menu_options:
    Button(menu_frame, text=text, font=("Arial", 14), bg="#dee2e6", fg="#2c3e50", bd=0, padx=20, pady=10,
           command=command).pack(fill="x", pady=2)

# ---------------- CAROUSEL FUNCTIONALITY ---------------- #
# ---------------- BACK-TO-BACK CAROUSEL WITH TIMED IMAGE SWITCHING ---------------- #
carousel_frame = Frame(root, bg="#f4f4f4", height=500)
carousel_frame.pack(fill="both", expand=True)

# List of images for the carousel
hotel_images = [
    r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\6.jpeg",
    r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\room.jpeg",
    r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\dining.jpeg",
    r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\3.jpeg",
    r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\8.jpeg",
    r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\10.jpeg"
]

# Load and resize images
carousel_photos = [load_image(img, (1366, 500)) for img in hotel_images]

# Label to display images
carousel_label = Label(carousel_frame, image=carousel_photos[0], bg="white")
carousel_label.pack(fill="both", expand=True)

# Dot indicators
dot_frame = Frame(carousel_frame, bg="#f4f4f4")
dot_frame.pack(side="bottom", pady=10)

dots = []
for i in range(len(carousel_photos)):
    dot = Label(dot_frame, text="●", font=("Arial", 14), fg="gray", bg="#f4f4f4")
    dot.pack(side="left", padx=5)
    dots.append(dot)

# Function to update dots
def update_dots(active_index):
    for i, dot in enumerate(dots):
        dot.config(fg="black" if i == active_index else "gray")

# Function to change images at a fixed time interval
def switch_image(index=0):
    carousel_label.config(image=carousel_photos[index])  # Update image
    update_dots(index)  # Update dots

    root.after(3000, switch_image, (index + 1) % len(carousel_photos))  # Switch after 3 sec

# Start the image switch loop
root.after(1000, switch_image)

"""##*def show_dashboard():
    # Image Carousel
    carousel_frame = Frame(root, bg="#f4f4f4", height=400)
    carousel_frame.pack(fill="both", expand=True)

    carousel_label = Label(carousel_frame, image=carousel_photos[0], bg="white")
    carousel_label.pack()

    def switch_image():
        for img in itertools.cycle(carousel_photos):
            for i in range(0, 255, 10):  # Fade-in effect
                carousel_label.config(image=img)
                carousel_label.update()
                root.after(50)  # Delay for smooth transition
            root.after(3000)  # Delay before next image

    root.after(1000, switch_image)*##"""




root.after(1000, switch_image)


# About Us Panel
def about_us_panel():
    global about_frame
    about_frame = Frame(root, bg="#d6eaf8", width=800, height=600)
    about_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Close button at the top-right inside the frame
    close_button = Button(about_frame, text="❌", font=("Arial", 12, "bold"), fg="red", bg="#d6eaf8",
                          command=about_frame.destroy, bd=0)
    close_button.pack(anchor="ne", padx=10, pady=5)  # Align top-right

    Label(about_frame, text="About SereniStay Hotel", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#d6eaf8").pack(
        pady=10)

    about_text = """Welcome to SereniStay Hotel, your perfect getaway!
        SereniStay Hotel - A Place of Luxury & Comfort

        🏨 Hotel Manager: Ms. Shravani Badabe
        Experience: 15+ years in the hospitality industry
        Award-winning service and customer satisfaction.
        📍 Location: 5-star luxury hotel in the heart of the city
        🏆 Award-winning hospitality with world-class facilities
        🛏️ 200+ deluxe & premium rooms
        🍽️ Multi-cuisine restaurants and spa facilities
        🎉 Perfect for business meetings, vacations & events

        Visit us for an unforgettable experience!


        """

    Label(about_frame, text=about_text, font=("Arial", 12), fg="#2c3e50", bg="white", justify="left").pack(pady=20)
# Contact Panel
def contact_panel():
    global contact_frame
    contact_frame = Frame(root, bg="#b4edda", width=400, height=250)
    contact_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Close button at the top-right inside the frame
    close_button = Button(contact_frame, text="❌", font=("Arial", 12, "bold"), fg="red", bg="#b4edda",
                          command=contact_frame.destroy, bd=0)
    close_button.pack(anchor="ne", padx=5, pady=5)  # Aligns top-right

    Label(contact_frame, text="Contact Us", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#b4edda").pack(pady=10)

    contact_text = """ Phone: +91 81042 26072
    Email: contact@serenistay.com
    Address: 45, Marine Drive, Mumbai, India."""

    Label(contact_frame, text=contact_text, font=("Arial", 12), fg="#2c3e50", bg="white", justify="left").pack()
# Review Panel
def review_panel():
    global review_frame
    review_frame = Frame(root, bg="#fff3cd", width=500, height=400)
    review_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Close button at the top-right inside the frame
    close_button = Button(review_frame, text="❌", font=("Arial", 12, "bold"), fg="red", bg="#fff3cd",
                          command=review_frame.destroy, bd=0)
    close_button.pack(anchor="ne", padx=5, pady=5)  # Aligns top-right

    Label(review_frame, text="Submit a Review", font=("Arial", 18, "bold"), fg="#2c3e50", bg="#fff3cd").pack(pady=10)

    Label(review_frame, text="Name:", bg="white").pack(anchor="w", padx=10)
    entry_name = Entry(review_frame, width=40)
    entry_name.pack(pady=5)

    Label(review_frame, text="Contact:", bg="white").pack(anchor="w", padx=10)
    entry_contact = Entry(review_frame, width=40)
    entry_contact.pack(pady=5)

    Label(review_frame, text="Review:", bg="white").pack(anchor="w", padx=10)
    entry_review = Text(review_frame, width=50, height=5)
    entry_review.pack(pady=5)

    def save_review():
        name = entry_name.get().strip()
        contact = entry_contact.get().strip()
        review_text = entry_review.get("1.0", END).strip()

        if not name or not contact or not review_text:
            messagebox.showerror("Error", "All fields are required!")
            return

        data = {"Name": [name], "Contact": [contact], "Review": [review_text]}
        df = pd.DataFrame(data)

        file_path = "hotel_reviews.xlsx"
        if os.path.exists(file_path):
            existing_data = pd.read_excel(file_path, engine="openpyxl")
            df = pd.concat([existing_data, df], ignore_index=True)

        df.to_excel(file_path, index=False)
        messagebox.showinfo("Success", "Review submitted successfully!")
        entry_name.delete(0, END)
        entry_contact.delete(0, END)
        entry_review.delete("1.0", END)

    Button(review_frame, text="Submit Review", font=("Arial", 12), bg="#28a745", fg="white", command=save_review).pack(pady=10)

def open_chatbot():
    Chatbot(root)
chatbot_icon = load_image(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\Chatbot.png", (40, 40))  # Load chatbot icon

# Footer
footer_frame = Frame(root, bg="#f8f9fa", height=60, bd=2, relief="solid")
footer_frame.pack(fill="x", side="bottom")
footer_buttons = [
    ("About Us", about_us_panel),
    ("Contact", contact_panel),
    ("Review", review_panel)
]

for i, (btn_text, command) in enumerate(footer_buttons):
    btn = Button(footer_frame, text=btn_text, font=("Arial", 14), bg="#dee2e6", fg="#2c3e50",
                 bd=0, padx=20, pady=10, command=command)
    btn.place(relx=0.2 + (i * 0.2), rely=0.5, anchor="center")

# Add Chatbot Button with Only Icon
chatbot_btn = Button(footer_frame, image=chatbot_icon, bg="#dee2e6", bd=0, command=open_chatbot)
chatbot_btn.place(relx=0.8, rely=0.5, anchor="center")  # Adjust position as needed

for i, btn_data in enumerate(footer_buttons):
    if len(btn_data) == 2:  # Normal buttons (About Us, Contact, Review)
        btn_text, command = btn_data
        btn = Button(footer_frame, text=btn_text, font=("Arial", 14), bg="#dee2e6", fg="#2c3e50",
                     bd=0, padx=20, pady=10, command=command)
    else:  # Chatbot button with icon
        btn_text, command, icon = btn_data
        btn = Button(footer_frame, text=btn_text, image=icon, compound="left", font=("Arial", 14), bg="#dee2e6",
                     fg="#2c3e50", bd=0, padx=20, pady=10, command=command)

    btn.place(relx=0.2 + (i * 0.2), rely=0.5, anchor="center")  # Center buttons evenly
root.mainloop()