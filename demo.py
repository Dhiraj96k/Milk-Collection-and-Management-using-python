import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
import sqlite3 as sq
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from tkinter import simpledialog
import subprocess

class MilkManage:
    def __init__(self, root):
        self.root = root
        self.otp_code = None
        self.setup_ui()

        self.sender_email = 'email here'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.sender_password ='Insert your own password '    
        try:
            self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.starttls()
            self.server.login(self.sender_email, self.sender_password)
            print("Email server connected successfully!")
        except Exception as e:
            print(f"Failed to connect to email server: {e} \n Please check your Internet Connection")
            self.server = None  # If connection fails, set server to None for safety

    # Setup the main login screen (Admin Login)
    def setup_ui(self):
        self.root.title("Login to Admin")
        
        # Auto-detect screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set the window size (50% of the screen width and height)
        window_width = int(screen_width)
        window_height = int(screen_height)
        
        # Calculate the position to center the window
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.configure(bg="#f0f4f7")


        self.frame = tk.Frame(self.root, bg="#ffffff", bd=4, relief="groove", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=400)

        label_title = tk.Label(self.frame, text="Login To Admin", bg="#ffffff", fg="#333", 
                               font=("Helvetica", 20, "bold"))
        label_title.pack(pady=10)

        label_username = tk.Label(self.frame, text="Username", bg="#ffffff", fg="#555555", 
                                  font=("Arial", 12, "bold"))
        label_username.pack(pady=(5, 2))

        self.entry_username = tk.Entry(self.frame, width=30, bd=2, relief="solid", font=("Arial", 12))
        self.entry_username.pack(pady=5)

        label_password = tk.Label(self.frame, text="Password", bg="#ffffff", fg="#555555", 
                                  font=("Arial", 12, "bold"))
        label_password.pack(pady=(5, 2))

        self.entry_password = tk.Entry(self.frame, width=30, bd=2, relief="solid", font=("Arial", 12), show="*")
        self.entry_password.pack(pady=5)

        forgot_button = tk.Button(self.frame, text="I Am Farmer", bg="#ffffff", fg="#007bff",
                                  cursor="hand2", font=("Arial", 10, "underline"), command=self.farmer_login, borderwidth=0)
        forgot_button.pack(pady=5)

        self.remember_var = tk.IntVar()
        remember_check = tk.Checkbutton(self.frame, text="Remember me", variable=self.remember_var, 
                                        bg="#ffffff", font=("Arial", 10), fg="#333333")
        remember_check.pack(pady=(5, 10))

        sign_in_button = tk.Button(self.frame, text="Sign In", command=self.login, bg="#a525cc", fg="white", 
                                   width=14, height=2, font=("Arial", 12, "bold"), bd=0, relief="flat", cursor="hand2")
        sign_in_button.pack(pady=15)

    # Farmer login UI
    def farmer_login(self):
        self.root.destroy()
        farmer = tk.Tk()
        farmer.title("Farmer Login")

        # Auto-detect screen size for Farmer login
        screen_width = farmer.winfo_screenwidth()
        screen_height = farmer.winfo_screenheight()
        
        # Set the window size (40% of the screen width and 50% of the screen height)
        window_width = int(screen_width)
        window_height = int(screen_height)
        
        # Calculate the position to center the window
        x_position = int((screen_width - window_width) / 2)
        y_position = int((screen_height - window_height) / 2)
        
        farmer.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        farmer.configure(bg="#e9eff5")

        title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        label_font = tkFont.Font(family="Helvetica", size=12)
        entry_font = tkFont.Font(family="Helvetica", size=11)

        frame = tk.Frame(farmer, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Farmer Login", font=title_font, bg="#ffffff", fg="#333333").grid(row=0, column=0, columnspan=3, pady=(0, 20))

        tk.Label(frame, text="Mobile Number:", font=label_font, bg="#ffffff").grid(row=1, column=0, sticky="e", padx=10, pady=8)
        self.mobile_entry = tk.Entry(frame, font=entry_font, width=25, bd=1, relief="solid")
        self.mobile_entry.grid(row=1, column=1, padx=5, pady=8)

        tk.Label(frame, text="Code:", font=label_font, bg="#ffffff").grid(row=2, column=0, sticky="e", padx=10, pady=8)
        self.code_entry = tk.Entry(frame, font=entry_font, width=25, bd=1, relief="solid")
        self.code_entry.grid(row=2, column=1, padx=5, pady=8)
        
        # Bind the event to fetch data when 'code_entry' loses focus
        self.code_entry.bind("<Return>", self.fetch_data_by_code)

        tk.Label(frame, text="Email:", font=label_font, bg="#ffffff").grid(row=4, column=0, sticky="e", padx=10, pady=8)
        self.email_entry = tk.Entry(frame, font=entry_font, width=25, bd=1, relief="solid")
        self.email_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=8)

        login_button = tk.Button(frame, text="Login", font=("Helvetica", 12),command=self.send_otp,
                                width=20, bg="#4CAF50", fg="white", relief="solid", bd=1, cursor="hand2", activebackground="#45a049")
        login_button.grid(row=5, column=0, columnspan=3, pady=(20, 0))

        footer_frame = tk.Frame(farmer, bg="#4CAF50", height=20)
        footer_frame.pack(fill="x", side="bottom")

        farmer.mainloop()


    def fetch_data_by_code(self, event):
        # Get the code entered by the farmer
        self.code = self.code_entry.get()

        if not self.code:
            return

        # Query the database to get the mobile number and email for the entered code
        try:
            conn = sq.connect('project_database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT mobno, Email FROM per_info WHERE code = ?", (self.code,))
            result = cursor.fetchone()
            conn.close()

            if result:
                # If data found, set the values in the respective fields
                self.mobile_entry.delete(0, tk.END)
                self.mobile_entry.insert(0, result[0])

                self.email_entry.delete(0, tk.END)
                self.email_entry.insert(0, result[1])
            else:
                # If no data found for the entered code
                messagebox.showwarning("Code Not Found", "No information found for this code.")
                self.mobile_entry.delete(0, tk.END)
                self.email_entry.delete(0, tk.END)

        except sq.Error as e:
            messagebox.showerror("Database Error", f"Error while fetching data: {e}")

    def send_otp(self):
        # Generate a random OTP
        self.otp_code = str(random.randint(100000, 999999))
        
        # Get the email and mobile number entered by the farmer
        receiver_email = self.email_entry.get()
        mobile_number = self.mobile_entry.get()

        # Check if both email and mobile number are provided
        if not receiver_email or not mobile_number:
            messagebox.showwarning("Input Error", "Please enter both email and mobile number.")
            return

        # Send OTP via email and SMS
        self.send_email(receiver_email, self.otp_code)
    
        # After sending OTP, show message box to ask for OTP input
        self.ask_for_otp()

    def ask_for_otp(self):
        # Ask the farmer to enter the OTP they received
        entered_otp = simpledialog.askstring("Enter OTP", "Please enter the OTP sent to your email :")

        # Verify if the entered OTP matches the generated OTP
        if entered_otp == self.otp_code:
            messagebox.showinfo("Success", "Login successful!")
            # Proceed to the next screen or functionality
            self.farmerdashboard()
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")
    
    # Send OTP via email
    def send_email(self, receiver_email, otp):
        subject = 'Milk Center'
        message = f'Dear Customer, \n{otp} is Your one time password(otp).please do not share the otp with other.'

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
            messagebox.showerror("Email Error", "Unable to send the OTP email. Please check your email settings.")
        finally:
            # Ensure the server is quit only if it's successfully initialized
            if 'server' in locals() and server:
                server.quit()

    def farmerdashboard(self):
        # Create a new window for the farmer's dashboard
        dashboard = tk.Tk()
        dashboard.title("Farmer Dashboard")

        # Auto-detect screen size
        screen_width = dashboard.winfo_screenwidth()
        screen_height = dashboard.winfo_screenheight()

        window_width = int(screen_width)
        window_height = int(screen_height)

        # Center the window on the screen
        x_position = int((screen_width - window_width))
        y_position = int((screen_height - window_height))

        dashboard.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        dashboard.configure(bg="#f0f4f7")

        # Set font styles
        title_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
        subtitle_font = tkFont.Font(family="Helvetica", size=18, weight="bold")
        label_font = tkFont.Font(family="Helvetica", size=14)
        table_font = tkFont.Font(family="Helvetica", size=12)

        # Add a header with a title
        header = tk.Label(
            dashboard,
            text="Farmer Dashboard",
            font=title_font,
            bg="#2d98da",
            fg="white",
            pady=10,
        )
        header.pack(fill="x")

        # Create a frame for the main content
        content_frame = tk.Frame(dashboard, bg="#ffffff", padx=20, pady=20, relief="groove", bd=2)
        content_frame.place(relx=0.5, rely=0.5, anchor="center", width=window_width * 0.9, height=window_height * 0.85)

        # Fetch and display farmer information
        try:
            code = self.code

            # Connect to the database
            conn = sq.connect('project_database.db')
            cursor = conn.cursor()

            # Fetch farmer profile information
            cursor.execute("SELECT name, mobno, email FROM per_info WHERE code = ?", (code,))
            farmer_info = cursor.fetchone()

            if farmer_info:
                name, mobno, email = farmer_info

                # Profile Section
                profile_frame = tk.Frame(content_frame, bg="#f5f7fa", padx=10, pady=10, relief="solid", bd=1)
                profile_frame.pack(fill="x", pady=10)

                tk.Label(profile_frame, text="Farmer Profile", font=subtitle_font, bg="#f5f7fa", fg="#34495e").pack(
                    anchor="w", padx=10
                )
                tk.Label(profile_frame, text=f"Name: {name}", font=label_font, bg="#f5f7fa").pack(anchor="w", padx=10)
                tk.Label(profile_frame, text=f"Mobile: {mobno}", font=label_font, bg="#f5f7fa").pack(anchor="w", padx=10)
                tk.Label(profile_frame, text=f"Email: {email}", font=label_font, bg="#f5f7fa").pack(anchor="w", padx=10)

            else:
                messagebox.showwarning("No Data Found", "No farmer record found for the entered code.")

            # Milk Records Section
            cursor.execute("SELECT liter, fat, snf, rate, amount, date, time_period FROM milk_info WHERE code = ? ORDER BY date DESC LIMIT 6", (code,))
            milk_records = cursor.fetchall()

            if milk_records:
                records_frame = tk.Frame(content_frame, bg="#f5f7fa", padx=10, pady=10, relief="solid", bd=1)
                records_frame.pack(fill="both", expand=True, pady=10)

                tk.Label(records_frame, text="Milk Records", font=subtitle_font, bg="#f5f7fa", fg="#34495e").pack(
                    anchor="w", padx=10, pady=(0, 10)
                )

                # Table Header
                headers = ["Liter", "Fat", "SNF", "Rate", "Amount", "Date", "Time Period"]
                header_frame = tk.Frame(records_frame, bg="#34495e")
                header_frame.pack(fill="x")

                for header in headers:
                    tk.Label(
                        header_frame,
                        text=header,
                        font=label_font,
                        bg="#34495e",
                        fg="white",
                        width=12,
                        pady=5,
                    ).pack(side="left", padx=2)

                # Table Rows
                for idx, record in enumerate(milk_records):
                    row_bg = "#ffffff" if idx % 2 == 0 else "#f5f7fa"
                    row_frame = tk.Frame(records_frame, bg=row_bg)
                    row_frame.pack(fill="x")

                    for col in record:
                        tk.Label(
                            row_frame,
                            text=col,
                            font=table_font,
                            bg=row_bg,
                            width=12,
                            pady=5,
                        ).pack(side="left", padx=2)

            else:
                tk.Label(
                    content_frame,
                    text="No milk records found for this farmer.",
                    font=label_font,
                    bg="#ffffff",
                    fg="#e74c3c",
                ).pack()

            conn.close()

        except sq.Error as e:
            messagebox.showerror("Database Error", f"Error while fetching data: {e}")

        # Logout Button
        logout_button = tk.Button(
            dashboard,
            text="Logout",
            font=label_font,
            command=dashboard.destroy,
            bg="#e74c3c",
            fg="white",
            width=15,
            pady=5,
        )
        logout_button.pack(side="bottom", pady=20)

        dashboard.mainloop()



    def verify_login(self):
        entered_otp = self.otp_entry.get()
        if entered_otp == self.otp_code:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "OTP does not match.")


    # Admin login logic
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = sq.connect('project_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Login successful!")
            try:
                subprocess.Popen(["python","main_board.py"])
            except Exception as e:
                messagebox.showerror("Warning!", "Check Information!")
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

        conn.close()



if __name__ == "__main__":
    root = tk.Tk()
    app = MilkManage(root)
    root.mainloop()
