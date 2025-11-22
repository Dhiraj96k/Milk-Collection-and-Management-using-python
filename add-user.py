import sqlite3
import re
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class UserInformationApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Database Management")
        # Set window size to 700x600 and position at (100, 100)
        self.window.geometry("700x600+250+50")
        self.window.config(bg="#f4f4f9")
        self.window.resizable(False, False)
        
        # Setup the UI
        self.create_widgets()

    # Establish connection to SQLite Database
    def connect_db(self):
        return sqlite3.connect('project_database.db')  # SQLite DB file

    # Validate Mobile Number (10 digits)
    def validate_mobno(self, mobno):
        return bool(re.match(r"^\d{10}$", mobno))

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zAZ0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(email_regex, email))

    # Helper to clear input fields
    def clear_fields(self):
        self.entry_code.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_mobno.delete(0, END)
        self.entry_email.delete(0, END)

    # Insert data into the database
    def insert_data(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Getting values from Entry widgets
            name = self.entry_name.get()
            mobno = self.entry_mobno.get()
            email = self.entry_email.get()

            # Check for empty fields
            if not name or not mobno or not email:
                messagebox.showerror("Input Error", "All fields must be filled out.")
                return

            # Validate mobile number and email
            if not self.validate_mobno(mobno):
                messagebox.showerror("Invalid Input", "Please enter a valid 10-digit mobile number.")
                return

            if not self.validate_email(email):
                messagebox.showerror("Invalid Input", "Please enter a valid email address.")
                return

            # SQL Insert query
            cursor.execute("INSERT INTO per_info (name, mobno, Email) VALUES (?, ?, ?)",
                           (name, mobno, email))
            conn.commit()

            # Get the last inserted code (the auto-incremented value)
            last_code = cursor.lastrowid

            # Clear the form
            self.clear_fields()

            # Show a message box with the generated code
            messagebox.showinfo("Success", f"User Added successfully!\nYour code is: {last_code}")
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

    # Update data based on code
    def update_data(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Getting values from Entry widgets
            code = self.entry_code.get()  # Code of the user to update
            name = self.entry_name.get()
            mobno = self.entry_mobno.get()
            email = self.entry_email.get()

            if not code.isdigit():
                messagebox.showerror("Error", "Please enter a valid code")
                return

            # Check for empty fields
            if not name or not mobno or not email:
                messagebox.showerror("Input Error", "All fields must be filled out.")
                return

            # Validate mobile number and email
            if not self.validate_mobno(mobno):
                messagebox.showerror("Invalid Input", "Please enter a valid 10-digit mobile number.")
                return

            if not self.validate_email(email):
                messagebox.showerror("Invalid Input", "Please enter a valid email address.")
                return

            # Update query
            cursor.execute("UPDATE per_info SET name = ?, mobno = ?, Email = ? WHERE code = ?",
                           (name, mobno, email, code))
            conn.commit()

            # Clear the form
            self.clear_fields()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"User with code {code} updated successfully!")
            else:
                messagebox.showerror("Error", "No user found with that code.")
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

    # Delete data based on code
    def delete_data(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Getting code to delete the user
            code = self.entry_code.get()

            if not code.isdigit():
                messagebox.showerror("Error", "Please enter a valid code")
                return

            # Delete query
            cursor.execute("DELETE FROM per_info WHERE code = ?", (code,))
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"User with code {code} deleted successfully!")
            else:
                messagebox.showerror("Error", "No user found with that code.")
            
            # Clear the form
            self.clear_fields()
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

    # Display all records from the database in a table (Treeview)
    def display_data(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM per_info")
            rows = cursor.fetchall()

            # Clear the treeview before displaying updated data
            for row in self.treeview.get_children():
                self.treeview.delete(row)

            # Insert each row into the treeview
            for row in rows:
                self.treeview.insert("", "end", values=row)
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

    # Create the UI components
    def create_widgets(self):
        # Add a header label
        header_label = Label(self.window, text="User Information Management", font=("Arial", 16, "bold"), bg="#f4f4f9")
        header_label.pack(pady=20)

        # Frame for the input fields
        frame_input = Frame(self.window, bg="#f4f4f9")
        frame_input.pack(pady=10)

        Label(frame_input, text="Code:", font=("Arial", 12), bg="#f4f4f9").grid(row=0, column=0, padx=10, pady=5)
        self.entry_code = Entry(frame_input, font=("Arial", 12), width=25)
        self.entry_code.grid(row=0, column=1, padx=10, pady=5)

        Label(frame_input, text="Name:", font=("Arial", 12), bg="#f4f4f9").grid(row=1, column=0, padx=10, pady=5)
        self.entry_name = Entry(frame_input, font=("Arial", 12), width=25)
        self.entry_name.grid(row=1, column=1, padx=10, pady=5)

        Label(frame_input, text="Mobile No:", font=("Arial", 12), bg="#f4f4f9").grid(row=2, column=0, padx=10, pady=5)
        self.entry_mobno = Entry(frame_input, font=("Arial", 12), width=25)
        self.entry_mobno.grid(row=2, column=1, padx=10, pady=5)

        Label(frame_input, text="Email:", font=("Arial", 12), bg="#f4f4f9").grid(row=3, column=0, padx=10, pady=5)
        self.entry_email = Entry(frame_input, font=("Arial", 12), width=25)
        self.entry_email.grid(row=3, column=1, padx=10, pady=5)

        # Buttons for inserting, updating, deleting, and displaying data
        frame_buttons = Frame(self.window, bg="#f4f4f9")
        frame_buttons.pack(pady=10)

        Button(frame_buttons, text="Insert Data", font=("Arial", 12), width=20, command=self.insert_data).grid(row=0, column=0, padx=10, pady=5)
        Button(frame_buttons, text="Update Data", font=("Arial", 12), width=20, command=self.update_data).grid(row=0, column=1, padx=10, pady=5)
        Button(frame_buttons, text="Delete Data", font=("Arial", 12), width=20, command=self.delete_data).grid(row=1, column=0, padx=10, pady=5)
        Button(frame_buttons, text="Show All Data", font=("Arial", 12), width=20, command=self.display_data).grid(row=1, column=1, padx=10, pady=5)

        # Treeview widget to display data in table format
        frame_treeview = Frame(self.window, bg="#f4f4f9")
        frame_treeview.pack(pady=20)

        self.treeview = ttk.Treeview(frame_treeview, columns=("Code", "Name", "Mobile No", "Email"), show="headings", height=10)
        self.treeview.pack(padx=10, pady=10)

        self.treeview.heading("Code", text="Code")
        self.treeview.heading("Name", text="Name")
        self.treeview.heading("Mobile No", text="Mobile No")
        self.treeview.heading("Email", text="Email")

        # Define column width
        self.treeview.column("Code", width=50, anchor="center")
        self.treeview.column("Name", width=150, anchor="center")
        self.treeview.column("Mobile No", width=100, anchor="center")
        self.treeview.column("Email", width=200, anchor="center")

# Create the Tkinter window and pass it to the class
window = Tk()
app = UserInformationApp(window)

# Start the GUI loop
window.mainloop()
