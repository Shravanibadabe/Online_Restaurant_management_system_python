import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CustomerPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Serenistay Hotel - Customer Management")
        self.root.geometry("1366x768")
        self.root.configure(bg="lightgray")

        # Top Header (Logo & Hotel Name)
        header_frame = tk.Frame(root, bg="blue", height=80)
        header_frame.pack(fill="x")

        # Load and Resize Logo
        logo_image = Image.open(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png")
        logo_image = logo_image.resize((80, 80), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(header_frame, image=self.logo, bg="blue")
        logo_label.place(x=10, y=0)

        # Hotel Name Label (Centered)
        hotel_label = tk.Label(header_frame, text="SERENISTAY HOTEL", font=("Arial", 24, "bold"), bg="blue", fg="yellow")
        hotel_label.place(relx=0.5, rely=0.5, anchor="center")

        # Main Panel
        main_frame = tk.Frame(root, bd=3, relief="ridge", bg="white")
        main_frame.place(x=50, y=100, width=1260, height=550)

        # Left Panel (Customer Details)
        details_frame = tk.Frame(main_frame, bd=3, relief="ridge", bg="white")
        details_frame.place(x=20, y=20, width=550, height=500)

        labels = ["Customer Ref:", "Customer Name:", "Mother Name:", "Gender:", "PostCode:", "Mobile:",
                  "Email:", "Nationality:", "ID Proof Type:", "ID Number:", "Address:"]
        self.entries = {}

        for i, text in enumerate(labels):
            lbl = tk.Label(details_frame, text=text, font=("Arial", 12, "bold"), bg="white")
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if text == "Gender:":
                combo = ttk.Combobox(details_frame, font=("Arial", 12), width=22, state="readonly",
                                     values=["Male", "Female", "Other"])  # Gender options
                combo.grid(row=i, column=1, padx=10, pady=5)
                self.entries[text] = combo
            elif text == "Nationality:":
                combo = ttk.Combobox(details_frame, font=("Arial", 12), width=22, state="readonly",
                                     values=["India", "USA", "UK", "Canada", "Australia", "Germany", "France", "Japan", "China"])  # Nationality options
                combo.grid(row=i, column=1, padx=10, pady=5)
                self.entries[text] = combo
            elif text == "ID Proof Type:":
                combo = ttk.Combobox(details_frame, font=("Arial", 12), width=22, state="readonly",
                                     values=["Aadhaar Card", "Passport", "Licence"])  # ID proof options
                combo.grid(row=i, column=1, padx=10, pady=5)
                self.entries[text] = combo
            else:
                entry = tk.Entry(details_frame, font=("Arial", 12), width=24)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entries[text] = entry

        # Buttons Section
        button_frame = tk.Frame(details_frame, bg="white")
        button_frame.grid(row=11, columnspan=2, pady=10)

        btn_texts = ["Save", "Update", "Delete", "Reset"]
        for i, text in enumerate(btn_texts):
            btn = tk.Button(button_frame, text=text, font=("Arial", 12, "bold"), bg="black", fg="yellow", width=12, height=1)
            btn.grid(row=0, column=i, padx=5)

        # Right Panel (Search & Table)
        table_frame = tk.Frame(main_frame, bd=3, relief="ridge", bg="white")
        table_frame.place(x=600, y=20, width=620, height=500)

        # Search Section
        search_label = tk.Label(table_frame, text="Search By", font=("Arial", 12, "bold"), bg="white")
        search_label.place(x=10, y=10)

        search_combo = ttk.Combobox(table_frame, font=("Arial", 12), width=15, state="readonly",
                                    values=["Reference No", "Name", "Mobile"])
        search_combo.place(x=90, y=10)
        search_combo.current(0)

        search_entry = tk.Entry(table_frame, font=("Arial", 12), width=20)
        search_entry.place(x=250, y=10)

        search_button = tk.Button(table_frame, text="Search", font=("Arial", 12, "bold"), bg="black", fg="yellow", width=10)
        search_button.place(x=480, y=5)

        # Table (Customer Data)
        columns = ("Ref No", "Name", "Mobile", "Email")
        customer_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            customer_table.heading(col, text=col)
            customer_table.column(col, width=140)

        customer_table.place(x=10, y=50, width=600, height=400)

        # **Back Button - FIXED POSITION**
        back_button = tk.Button(root, text="Back", font=("Arial", 12, "bold"), bg="black", fg="yellow", width=12, height=1, command=self.root.destroy)
        back_button.place(x=300, y=570)  # **Ensured it's visible in the bottom-left corner**

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerPanel(root)
    root.mainloop()