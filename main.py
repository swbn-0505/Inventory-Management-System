import tkinter as tk
from tkinter import messagebox

# Create the main application window
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("600x400")  # Width x Height

# Add a label
label = tk.Label(root, text="Welcome to Inventory Management System", font=("Arial", 14))
label.pack(pady=20)

# Run the application
root.mainloop()
