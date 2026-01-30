import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import pandas as pd
import os
import subprocess

class StaffPanel(tk.Tk):
    def __init__(self, username=""):
        super().__init__()
        self.title("Staff Panel - SereniStay Hotel")
        self.geometry("1100x650+0+0")
        self.state("zoomed")
        self.configure(bg="white")

        self.username = username  # Logged-in staff username
        self.ensure_excel_files()

        # Top Bar (Logo & Hotel Name)
        self.logo_img = Image.open(r"C:\Users\dell\Desktop\SRB\HOTEL MANAGEMENT\logo1.png")
        self.logo_img = self.logo_img.resize((80, 80))
        self.logo_img = ImageTk.PhotoImage(self.logo_img)

        top_frame = tk.Frame(self, bg="white")
        top_frame.pack(fill="x")

        tk.Label(top_frame, image=self.logo_img, bg="white").pack(side="left", padx=10)
        tk.Label(top_frame, text="SereniStay Hotel - Staff Panel", font=("Arial", 18, "bold"), bg="white").pack(side="left")
        tk.Label(top_frame, text=f"Welcome, {self.username}", font=("Arial", 12), bg="white").pack(side="right", padx=10)

        # Navigation Buttons
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=10)

        buttons = [
            ("Customer Records", self.show_customer_records),
            ("Staff Management", self.show_staff_management),
            ("Finance Tracking", self.show_finance_tracking),
            ("User Information", self.show_user_info),
            ("Inventory Tracker", self.show_inventory_tracker),
            ("Make Announcement", self.show_announcements),
            ("Logout",self.logout),
        ]

        for text, command in buttons:
            ttk.Button(btn_frame, text=text, command=command).pack(side="left", padx=10)

        # Main Content Frame
        self.main_frame = tk.Frame(self, bg="white", relief="ridge", bd=2)
        self.main_frame.pack(pady=10, fill="both", expand=True)

        self.show_customer_records()

    def ensure_excel_files(self):
        """Ensures that necessary Excel files exist before reading them."""
        files = {
            "room_bookings.xlsx": ["ID", "Name", "Room Number", "Check-In", "Check-Out"],
            "hall_bookings.xlsx": ["ID", "Name", "Hall Name", "Booking Date", "Event Type"],
            "food_orders.xlsx": ["ID", "Customer Name", "Order Details", "Total Amount"],
            "staff.xlsx": ["ID", "Name", "Role", "Contact"],
            "finance.xlsx": ["ID", "Description", "Amount", "Type"],
            "users.xlsx": ["Full Name", "Contact Number", "Email", "Username", "Password"],
            "inventory.xlsx": ["Item", "Category", "Quantity", "Supplier"],
            "announcement.xlsx":["ID","Announcement","Date"]
        }
        for file, columns in files.items():
            if not os.path.exists(file):
                pd.DataFrame(columns=columns).to_excel(file, index=False)

    def clear_frame(self):
        """Clears the main frame before loading new content."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_announcements(self):
        """Allows staff to make announcements that users will see after login."""
        self.clear_frame()
        tk.Label(self.main_frame, text="Make Announcement", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        tk.Label(self.main_frame, text="Enter Announcement:", font=("Arial", 12), bg="white").pack(pady=5)
        self.announcement_entry = tk.Text(self.main_frame, height=4, width=60)
        self.announcement_entry.pack(pady=5)

        ttk.Button(self.main_frame, text="Post Announcement", command=self.post_announcement).pack(pady=5)

        self.announcement_tree = self.create_treeview(["ID", "Announcement", "Date"])
        self.load_data("announcements.xlsx", self.announcement_tree, ["ID", "Announcement", "Date"])

    def post_announcement(self):
        """Posts an announcement and saves it to announcements.xlsx."""
        try:
            announcement = self.announcement_entry.get("1.0", tk.END).strip()
            if not announcement:
                messagebox.showerror("Error", "Announcement cannot be empty!")
                return

            file = "announcements.xlsx"

            # Ensure the file exists
            if not os.path.exists(file):
                pd.DataFrame(columns=["ID", "Announcement", "Date"]).to_excel(file, index=False)

            # Read the existing data
            df = pd.read_excel(file, dtype=str)

            # Generate a new ID
            new_id = str(int(df["ID"].max()) + 1) if not df.empty and df["ID"].max() else "1"

            # Create new entry
            new_entry = pd.DataFrame([{
                "ID": new_id,
                "Announcement": announcement,
                "Date": pd.Timestamp.now().strftime("%Y-%m-%d")
            }])

            # Append the new entry using pd.concat()
            df = pd.concat([df, new_entry], ignore_index=True)

            # Save the updated data
            with pd.ExcelWriter(file, engine="openpyxl", mode="w") as writer:
                df.to_excel(writer, index=False)

            # Refresh treeview
            self.load_data(file, self.announcement_tree, ["ID", "Announcement", "Date"])

            messagebox.showinfo("Success", "Announcement posted successfully!")
            self.announcement_entry.delete("1.0", tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Could not post announcement: {e}")

    ## 🔹 CUSTOMER RECORDS (Room, Hall, Food Orders) ##
    def show_customer_records(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Customer Records", font=("Arial", 14, "bold"), bg="white").pack(pady=5)

        # Dropdown Menu to Choose Data Type
        tk.Label(self.main_frame, text="Select Data Type:", font=("Arial", 12), bg="white").pack(pady=5)

        self.record_type = ttk.Combobox(self.main_frame, values=["Room Booking", "Hall Booking", "Food Orders"],
                                        state="readonly")
        self.record_type.pack(pady=5)
        self.record_type.current(0)  # Default selection

        ttk.Button(self.main_frame, text="Fetch Data", command=self.fetch_customer_data).pack(pady=5)
        default_columns=["ID", "Name", "Room Number", "Check-In", "Check-Out"]

        # Treeview to Display Data
        self.tree = self.create_treeview(default_columns)

    def fetch_customer_data(self):
        """Fetches customer data based on the selected type."""
        selected_option = self.record_type.get()

        # 🔹 Correct file and column mappings
        if selected_option == "Room Booking":
            file = "booking_data.xlsx"
            columns = ["Booking ID", "Name", "Contact", "Room Type", "Room No", "No. of Persons",
                       "Check-in", "Check-out", "ID Proof", "ID Number", "Total Cost", "Status", "Username"]
        # Ensure these match the Excel headers
        elif selected_option == "Hall Booking":
            file = "hall_bookings.xlsx"
            columns = ["Booking ID", "Name","Contact", "Date","Guests", "Hall Type", "Estimated Cost ($)","Hall Number","Username"]
        elif selected_option == "Food Orders":
            file = "food_orders.xlsx"
            columns = [ "Customer Name","Booking ID","Contact", "Payment Method","Ordered Items", "Total Price"]
        else:
            messagebox.showerror("Error", "Invalid Selection!")
            return

        # 🔹 Clear only the Treeview, keeping navigation intact
        # Clear previous Treeview data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Update column headers dynamically
        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)  # Adjust width if needed

        # 🔹 Load new data
        self.load_data(file, self.tree, columns)

    ## 🔹 STAFF MANAGEMENT ##
    def show_staff_management(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Manage Staff", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        entry_frame = tk.Frame(self.main_frame, bg="white")
        entry_frame.pack(pady=5, fill="x")

        fields = ["Name", "Role", "Contact"]
        entries = [tk.Entry(entry_frame) for _ in fields]
        for field, entry in zip(fields, entries):
            tk.Label(entry_frame, text=field, bg="white").pack(side="left", padx=5)
            entry.pack(side="left", padx=5)

        ttk.Button(entry_frame, text="Add Staff",
                   command=lambda: self.add_record("staff.xlsx", entries, ["ID", "Name", "Role", "Contact"],
                                                   self.staff_tree)).pack(side="left", padx=5)

        self.staff_tree = self.create_treeview(["ID", "Name", "Role", "Contact"])
        self.load_data("staff.xlsx", self.staff_tree, ["ID", "Name", "Role", "Contact"])
        ttk.Button(entry_frame, text="Remove Staff",
                   command=lambda: self.remove_staff("staff.xlsx", self.staff_tree)).pack(side="left", padx=5)

    ## 🔹 FINANCE TRACKER ##
    def show_finance_tracking(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Finance Tracking", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        entry_frame = tk.Frame(self.main_frame, bg="white")
        entry_frame.pack(pady=5, fill="x")

        fields = ["Description", "Amount", "Type (Income/Expense)"]
        entries = [tk.Entry(entry_frame) for _ in fields]

        for field, entry in zip(fields, entries):
            tk.Label(entry_frame, text=field, bg="white").pack(side="left", padx=5)
            entry.pack(side="left", padx=5)

        ttk.Button(entry_frame, text="Add Record",
                   command=lambda: self.add_record("finance.xlsx", entries,
                                                   ["ID", "Description", "Amount", "Type"],
                                                   self.finance_tree)).pack(side="left", padx=5)

        self.finance_tree = self.create_treeview(["ID", "Description", "Amount", "Type"])
        self.load_data("finance.xlsx", self.finance_tree, ["ID", "Description", "Amount", "Type"])

    ## 🔹 USER INFORMATION ##

    def show_user_info(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="User Information", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        self.user_tree = self.create_treeview(["Full Name", "Contact Number", "Email", "Username"])
        self.load_data("users.xlsx", self.user_tree, ["Full Name", "Contact Number", "Email", "Username"])

    ## 🔹 INVENTORY TRACKER ##
    def show_inventory_tracker(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Hotel Inventory", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        entry_frame = tk.Frame(self.main_frame, bg="white")
        entry_frame.pack(pady=5, fill="x")

        fields = ["Item", "Category", "Quantity", "Supplier"]
        entries = [tk.Entry(entry_frame) for _ in fields]

        for field, entry in zip(fields, entries):
            tk.Label(entry_frame, text=field, bg="white").pack(side="left", padx=5)
            entry.pack(side="left", padx=5)

        ttk.Button(entry_frame, text="Add Item",
                   command=lambda: self.add_record("inventory.xlsx", entries,["Item", "Category", "Quantity", "Supplier"],self.inventory_tree)).pack(side="left", padx=5)

        self.inventory_tree = self.create_treeview(["Item", "Category", "Quantity", "Supplier"])
        self.load_data("inventory.xlsx", self.inventory_tree, ["Item", "Category", "Quantity", "Supplier"])

    ## 🔹 HELPER FUNCTIONS ##
    def create_treeview(self, columns):
        tree_frame = tk.Frame(self.main_frame, bg="white")
        tree_frame.pack(fill="both", expand=True, pady=10)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True)
        return tree

    def load_data(self, file, tree, columns):
        try:
            df = pd.read_excel(file, dtype=str)  # Read all data as strings to prevent conversion issues

            if df.empty:
                messagebox.showinfo("Info", f"No records found in {file}")
                return

            tree.delete(*tree.get_children())  # Clear existing entries

            for _, row in df.iterrows():
                tree.insert("", "end", values=[row[col] if col in df.columns else "" for col in columns])

        except Exception as e:
            messagebox.showerror("Error", f"Could not load data from {file}: {e}")

    def add_record(self, file, entries, columns, tree):
        try:
            # Read the existing data
            df = pd.read_excel(file, dtype=str)  # Ensure all columns are read as strings

            # Collect values from entry fields
            new_values = [e.get().strip() for e in entries]  # Remove extra spaces

            # Generate a unique ID if required
            if "ID" in columns:
                df["ID"] = pd.to_numeric(df["ID"], errors='coerce')  # Convert ID column to numeric
                new_id = int(df["ID"].max()) + 1 if not df.empty and df["ID"].max() >= 0 else 1
                new_values.insert(0, str(new_id))  # Convert ID to string and insert at index 0

            # **Validation for Contact Number (Only for Staff)**
            if file == "staff.xlsx":
                contact = new_values[3]  # Assuming contact is at index 3
                if not contact.isdigit() or len(contact) != 10:
                    messagebox.showerror("Error", "Invalid phone number! It must be exactly 10 digits.")
                    return

            # **Validation for Numeric Fields**
            if file == "finance.xlsx":
                amount = new_values[2]  # Assuming amount is at index 2
                if not amount.replace(".", "").isdigit():  # Allow decimal values
                    messagebox.showerror("Error", "Amount must be a numeric value!")
                    return

            if file == "inventory.xlsx":
                quantity = new_values[2]  # Assuming quantity is at index 2
                if not quantity.isdigit():
                    messagebox.showerror("Error", "Quantity must be a numeric value!")
                    return

            # Append the new data
            df.loc[len(df)] = new_values

            # **Save the file** (Fixes permission issues by using a different writer)
            with pd.ExcelWriter(file, engine="openpyxl", mode="w") as writer:
                df.to_excel(writer, index=False)

            # **Delay to allow file update before refreshing Treeview**
            self.after(500, lambda: self.load_data(file, tree, columns))

            # **Show success message after updating**
            messagebox.showinfo("Success", "Record added successfully!")

            # **Clear input fields**
            for e in entries:
                e.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Could not add record: {e}")

    def remove_staff(self, file, tree, id_column="ID"):
        try:
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a staff member to remove!")
                return

            record_id = tree.item(selected_item, "values")[0]  # Assuming ID is the first column

            df = pd.read_excel(file, dtype=str)

            if record_id not in df[id_column].values:
                messagebox.showerror("Error", "Staff record not found in database!")
                return

            df = df[df[id_column] != record_id]  # Remove the selected staff

            with pd.ExcelWriter(file, engine="openpyxl", mode="w") as writer:
                df.to_excel(writer, index=False)

            tree.delete(selected_item)

            messagebox.showinfo("Success", "Staff record removed successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Could not remove staff: {e}")
    def logout(self):
        self.destroy()  # Close the current dashboard
        subprocess.Popen(["python", "login.py"])  # Open the login panel
if __name__ == "__main__":
    app = StaffPanel(username="Admin")
    app.mainloop()