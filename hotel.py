import subprocess
import sys
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import os


def get_latest_announcement():
    file = "announcements.xlsx"  # Ensure this file exists
    if not os.path.exists(file):
        return "No announcements available."

    df = pd.read_excel(file, dtype=str)  # Read the Excel file
    if df.empty:
        return "No announcements available."

    latest_announcement = df.iloc[-1]["Announcement"]  # Get the last row's "Announcement" column
    return latest_announcement

class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.username=sys.argv[1] if len(sys.argv)>1 else "Guest"
        self.root.title(f"Hotel Management System-{self.username}")
        self.root.geometry("1550x800+0+0")
        self.root.state("zoomed")
        # Header Image
        # Hotel Name at the place of the Header Image
        lbl_hotel_name = Label(self.root, text="SERENISTAY HOTEL", font=("times new roman", 50, "bold"), bg="#1E3A8A",
                               fg="gold", bd=4, relief=RIDGE)
        lbl_hotel_name.place(x=0, y=0, width=1550, height=140)

        # Logo Image
        img2 = Image.open(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png")  # Change to your image path
        img2 = img2.resize((230, 140), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lblImg = Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE)
        lblImg.place(x=0, y=0, width=230, height=140)

       
        # Fetch Latest Announcement
        self.announcement_text = get_latest_announcement()

        # Initial Position of Announcement (Start from left)
        self.announcement_x = self.root.winfo_screenwidth()# Start from the right edge

        # Moving Announcement Label
        self.lbl_announcement = Label(self.root, text=f"📢 {self.announcement_text}",
                                      font=("times new roman", 20, "bold"),  # <- Change this to 20
                                      bg="#FFDDDD",  # Light Pink Background
                                      fg="#6A0DAD",  # Dark Purple Text
                                      bd=4, relief=RIDGE)
        self.lbl_announcement.place(x=self.announcement_x, y=140, width=1900, height=50)
        self.announcement_width = self.lbl_announcement.winfo_reqwidth()
        self.lbl_announcement.config(width=self.announcement_width)
        # Start Moving Announcement
        self.move_announcement()

        # Left Menu Frame
        menu_frame = Frame(self.root, bd=4, relief=RIDGE, bg="black")
        menu_frame.place(x=0, y=190, width=230, height=600)

        lbl_menu = Label(menu_frame, text="MENU", font=("times new roman", 20, "bold"), bg="black", fg="gold")
        lbl_menu.pack(side=TOP, fill=X)

        # Buttons in Menu


        self.room_btn = Button(menu_frame, text="ROOM BOOKING", font=("times new roman", 14, "bold"), bg="black", fg="gold", width=20,command=self.open_room_panel)
        self.room_btn.pack(pady=5)

        self.hall_btn = Button(menu_frame, text="HALL BOOKING", font=("times new roman", 14, "bold"), bg="black", fg="gold",width=20, command=self.open_hall_panel)
        self.hall_btn.pack(pady=5)

        self.food_btn = Button(menu_frame, text="FOOD ", font=("times new roman", 14, "bold"), bg="black",fg="gold", width=20,command=self.open_food_panel)
        self.food_btn.pack(pady=5)

        self.details_btn = Button(menu_frame, text="DETAILS", font=("times new roman", 14, "bold"), bg="black", fg="gold", width=20,command=self.open_details_panel)
        self.details_btn.pack(pady=5)
        self.logout_btn = Button(menu_frame, text="LOG OUT", font=("times new roman", 14, "bold"), bg="red", fg="white", width=20,command=self.logout)
        self.logout_btn.pack(pady=5)

        self.exit_btn = Button(menu_frame, text="EXIT", command=self.root.quit, font=("times new roman", 14, "bold"), bg="red", fg="white", width=20)
        self.exit_btn.pack(pady=5)


        # Left side images
        img3 = Image.open(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\2.jpg")
        img3 = img3.resize((230, 200), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        lblImg = Label(menu_frame, image=self.photoimg3, bd=2, relief=RIDGE)
        lblImg.pack(pady=5)

        img4 = Image.open(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\7.jpeg")  # Change to your image path
        img4 = img4.resize((230, 200), Image.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)
        lblImg = Label(menu_frame, image=self.photoimg4, bd=2, relief=RIDGE)
        lblImg.pack(pady=5)

        # Right-side Content Frame
        self.content_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        self.content_frame.place(x=230, y=190, width=1320, height=600)

        # Right side main image
        img5 = Image.open(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\10.jpeg")  # Change to your image path
        img5 = img5.resize((1310, 590), Image.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)
        lblImg1 = Label(self.content_frame, image=self.photoimg5, bd=4, relief=RIDGE)
        lblImg1.place(x=5, y=5, width=1310, height=590)

    def move_announcement(self):
        """Moves the announcement continuously from right to left."""
        self.announcement_x -= 3  # Move left smoothly

        # Reset position after the text moves completely off-screen
        if self.announcement_x < -self.announcement_width:
            self.announcement_x = self.root.winfo_screenwidth() # Adjust based on text size

        # Update label position
        self.lbl_announcement.place(x=self.announcement_x, y=140, width=1900, height=50)

        # Repeat movement every 30ms for smooth scrolling
        self.root.after(30, self.move_announcement)
    def open_room_panel(self):
        subprocess.Popen(["python", "room.py",self.username])  # Ensure staff .py is in the same directory

    def logout(self):
        self.root.destroy()  # Close the current dashboard
        subprocess.Popen(["python", "login.py"])  # Open the login panel
    def open_hall_panel(self):
        subprocess.Popen(["python", "Hall Booking.py",self.username])
    def open_food_panel(self):
        subprocess.Popen(["python","dining.py",self.username])
    def open_details_panel(self):
        subprocess.Popen(["python","customer_details.py",self.username])



if __name__ == "__main__":
    username=sys.argv[1] if len(sys.argv)>1 else "Guest"
    root = Tk()
    obj = HotelManagementSystem(root)
    root.mainloop()