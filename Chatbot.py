import tkinter as tk
from tkinter import scrolledtext


class Chatbot(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("SereniStay Assistant")
        self.geometry("500x700")
        self.configure(bg="white")

        tk.Label(self, text="SereniStay Assistant", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # Chat display area
        self.chat_display = scrolledtext.ScrolledText(self, width=45, height=15, wrap=tk.WORD, state="disabled")
        self.chat_display.pack(padx=10, pady=5)

        # Predefined questions
        self.questions = {
            "How do I book a room?": "First, log in to the application. Then, click on 'Room Booking'. Fill in your details such as name, contact, check-in and check-out dates, and select a room type. Confirm the booking to complete the process.",
            "How do I book a hall for an event?": "Log in and click on 'Hall Booking'. Select the event date, hall type, and number of guests. Enter the required details and confirm your booking.",
            "How can I order food?":  "First, log in and ensure you have a booked room or hall. Then, click on 'Food' and select your food items. Confirm the order to proceed.",
            "How do I check my booking details?": "Log in and click on 'Customer Details'. Here, you can see your room, hall, and food orders.",
            "How can I contact customer support?": "Visit the 'Contact Us' section for customer support details."
        }

        tk.Label(self, text="Select a question:", font=("Arial", 12), bg="white").pack(pady=5)

        # Display predefined questions as buttons
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=5)

        for question in self.questions.keys():
            tk.Button(button_frame, text=question, command=lambda q=question: self.display_answer(q),
                      wraplength=350, justify="left", width=45, height=2, bg="#f0f0f0").pack(pady=3)

        # Close button
        tk.Button(self, text="Close", command=self.destroy, bg="red", fg="white").pack(pady=10)

    def display_answer(self, question):
        """Displays the chatbot response in the chat window."""
        answer = self.questions.get(question, "Sorry, I don't understand that question.")
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"You: {question}\nBot: {answer}\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.yview(tk.END)  # Auto-scroll to the latest message


# To test the chatbot independently
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    chatbot = Chatbot(root)
    chatbot.mainloop()