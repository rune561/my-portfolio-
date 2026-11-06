import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import date


class DeviceRepairTracker:

   
    # COLORS
    
    NAVY = "#12355B"
    BLUE = "#1976D2"
    LIGHT_BLUE = "#EAF4FF"
    BG = "#F4F7FB"
    WHITE = "#FFFFFF"
    TEXT = "#1F2937"
    GRAY = "#6B7280"
    GREEN = "#2E9B5B"
    RED = "#D64545"
    ORANGE = "#E58A00"
    PURPLE = "#7952B3"
    BORDER = "#D9E2EC"

    def __init__(self, root):
        self.root = root

        self.root.title("Device Repair Tracker")

        # ADMIN DASHBOARD SIZE - DO NOT CHANGE
        self.root.geometry("1150x700")
        self.root.minsize(1000, 650)

        self.root.configure(bg=self.BG)

        
        # DATABASE
       
        self.db = sqlite3.connect("device_repair_tracker.db")
        self.cursor = self.db.cursor()

       
        # LOGIN INFORMATION
       
        self.current_user_id = None
        self.current_username = ""
        self.current_role = ""

        self.selected_id = None
        self.last_customer_username = ""

        self.create_database()

        self.root.protocol("WM_DELETE_WINDOW", self.close_database)

        self.show_login()

   
    # DATABASE
    

    def create_database(self):

        # USERS TABLE
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # REPAIRS TABLE
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS repairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_username TEXT,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                device_type TEXT NOT NULL,
                device_model TEXT NOT NULL,
                problem TEXT NOT NULL,
                repair_status TEXT NOT NULL,
                repair_cost REAL NOT NULL,
                repair_date TEXT NOT NULL
            )
        """)

        
        # DATABASE MIGRATION
        
        # Check USERS columns
        self.cursor.execute("PRAGMA table_info(users)")
        user_columns = [column[1] for column in self.cursor.fetchall()]

        if "role" not in user_columns:
            self.cursor.execute(
                "ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'Customer'"
            )

        # Check REPAIRS columns
        self.cursor.execute("PRAGMA table_info(repairs)")
        repair_columns = [column[1] for column in self.cursor.fetchall()]

        if "customer_username" not in repair_columns:
            self.cursor.execute(
                "ALTER TABLE repairs ADD COLUMN customer_username TEXT DEFAULT 'customer'"
            )

        
        # DEFAULT ADMIN
       
        self.cursor.execute(
            "SELECT * FROM users WHERE username=?",
            ("admin",)
        )

        if self.cursor.fetchone() is None:
            self.cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            """, ("admin", "admin123", "Admin"))

        
        # DEFAULT CUSTOMER
       

        self.cursor.execute(
            "SELECT * FROM users WHERE username=?",
            ("customer",)
        )

        if self.cursor.fetchone() is None:
            self.cursor.execute("""
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
            """, ("customer", "customer123", "Customer"))

        self.db.commit()

   
    # CLEAR WINDOW
   

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

   
    # LOGIN PAGE
    

    def show_login(self):

        self.clear_window()

        # LOGIN PAGE SIZE
        self.root.geometry("950x600")
        self.root.minsize(850, 550)

        
        # MAIN FRAME
        
        main = tk.Frame(
            self.root,
            bg=self.BG
        )
        main.pack(fill="both", expand=True)

       
        # LEFT PANEL
        

        left = tk.Frame(
            main,
            bg=self.NAVY,
            width=430
        )
        left.pack(side="left", fill="y")

        left.pack_propagate(False)

        tk.Label(
            left,
            text="DEVICE",
            font=("Segoe UI", 28, "bold"),
            bg=self.NAVY,
            fg=self.WHITE
        ).pack(pady=(125, 0))

        tk.Label(
            left,
            text="REPAIR TRACKER",
            font=("Segoe UI", 28, "bold"),
            bg=self.NAVY,
            fg="#8FD3FF"
        ).pack()

        tk.Label(
            left,
            text="Smart • Simple • Organized",
            font=("Segoe UI", 12),
            bg=self.NAVY,
            fg="#D9EAF7"
        ).pack(pady=15)

        tk.Label(
            left,
            text="Manage device repairs easily\n"
                 "with our simple repair tracking system.",
            font=("Segoe UI", 11),
            bg=self.NAVY,
            fg="#D9EAF7",
            justify="center"
        ).pack(pady=20)

       
        # RIGHT PANEL
       

        right = tk.Frame(
            main,
            bg=self.BG
        )
        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        card = tk.Frame(
            right,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=410,
            height=500
        )

        tk.Label(
            card,
            text="Welcome Back!",
            font=("Segoe UI", 24, "bold"),
            bg=self.WHITE,
            fg=self.NAVY
        ).pack(pady=(35, 5))

        tk.Label(
            card,
            text="Login to your account",
            font=("Segoe UI", 10),
            bg=self.WHITE,
            fg=self.GRAY
        ).pack(pady=(0, 25))

        
        # ROLE
      
        tk.Label(
            card,
            text="Login As",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=40)

        self.login_role = ttk.Combobox(
            card,
            values=["Admin", "Customer"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.login_role.pack(
            fill="x",
            padx=40,
            pady=(5, 15),
            ipady=5
        )
        self.login_role.set("Customer")

       
        # USERNAME
       

        tk.Label(
            card,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=40)

        self.login_username = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.login_username.pack(
            fill="x",
            padx=40,
            pady=(5, 15),
            ipady=7
        )

        
        # PASSWORD
      

        tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=40)

        self.login_password = tk.Entry(
            card,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            relief="solid",
            bd=1,
            show="*"
        )
        self.login_password.pack(
            fill="x",
            padx=40,
            pady=(5, 8),
            ipady=7
        )

        # SHOW PASSWORD

        self.show_pass_var = tk.BooleanVar()

        tk.Checkbutton(
            card,
            text="Show Password",
            variable=self.show_pass_var,
            command=self.toggle_password,
            bg=self.WHITE,
            fg=self.GRAY,
            activebackground=self.WHITE,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=38
        )

       
        # LOGIN BUTTON
       

        tk.Button(
            card,
            text="LOGIN",
            command=self.login,
            bg=self.BLUE,
            fg=self.WHITE,
            activebackground=self.NAVY,
            activeforeground=self.WHITE,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            fill="x",
            padx=40,
            pady=(18, 12),
            ipady=8
        )

        
        # REGISTER
        

        register_frame = tk.Frame(
            card,
            bg=self.WHITE
        )
        register_frame.pack()

        tk.Label(
            register_frame,
            text="Don't have an account?",
            bg=self.WHITE,
            fg=self.GRAY,
            font=("Segoe UI", 9)
        ).pack(side="left")

        tk.Button(
            register_frame,
            text="Register",
            command=self.show_registration,
            bg=self.WHITE,
            fg=self.BLUE,
            activebackground=self.WHITE,
            activeforeground=self.NAVY,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(side="left")

        
        # DEMO LOGIN
       

        tk.Label(
            card,
            text="Demo Admin: admin / admin123\n"
                 "Demo Customer: customer / customer123",
            bg=self.WHITE,
            fg=self.GRAY,
            font=("Segoe UI", 8),
            justify="center"
        ).pack(pady=10)

    
    # TOGGLE PASSWORD
   
    def toggle_password(self):

        if self.show_pass_var.get():
            self.login_password.config(show="")
        else:
            self.login_password.config(show="*")

    
    # LOGIN
   

    def login(self):

        username = self.login_username.get().strip()
        password = self.login_password.get()
        role = self.login_role.get()

        if username == "" or password == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter username and password."
            )
            return

        self.cursor.execute("""
            SELECT id, username, role
            FROM users
            WHERE username=? AND password=? AND role=?
        """, (username, password, role))

        user = self.cursor.fetchone()

        if user:

            self.current_user_id = user[0]
            self.current_username = user[1]
            self.current_role = user[2]

            if role == "Admin":
                self.show_admin_dashboard()
            else:
                self.show_customer_dashboard()

        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username, password, or role."
            )

   
    # REGISTRATION PAGE
    

    def show_registration(self):

        self.clear_window()

        self.root.geometry("650x680")
        self.root.minsize(600, 620)

        main = tk.Frame(
            self.root,
            bg=self.BG
        )
        main.pack(
            fill="both",
            expand=True
        )

        card = tk.Frame(
            main,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=500,
            height=620
        )

        tk.Label(
            card,
            text="Create Account",
            font=("Segoe UI", 24, "bold"),
            bg=self.WHITE,
            fg=self.NAVY
        ).pack(pady=(25, 5))

        tk.Label(
            card,
            text="Register for Device Repair Tracker",
            font=("Segoe UI", 10),
            bg=self.WHITE,
            fg=self.GRAY
        ).pack(pady=(0, 20))

       
        # FULL NAME
       
        tk.Label(
            card,
            text="Full Name",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=50)

        self.reg_name = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.reg_name.pack(
            fill="x",
            padx=50,
            pady=(4, 10),
            ipady=5
        )

       
        # PHONE
       

        tk.Label(
            card,
            text="Phone Number",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=50)

        self.reg_phone = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.reg_phone.pack(
            fill="x",
            padx=50,
            pady=(4, 10),
            ipady=5
        )

      
        # ROLE
       
        tk.Label(
            card,
            text="Choose Role",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=50)

        self.reg_role = ttk.Combobox(
            card,
            values=["Customer", "Admin"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.reg_role.pack(
            fill="x",
            padx=50,
            pady=(4, 10),
            ipady=4
        )
        self.reg_role.set("Customer")

       
        # USERNAME
       

        tk.Label(
            card,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=50)

        self.reg_username = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.reg_username.pack(
            fill="x",
            padx=50,
            pady=(4, 10),
            ipady=5
        )

       
        # PASSWORD
    

        tk.Label(
            card,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=50)

        self.reg_password = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="solid",
            bd=1,
            show="*"
        )
        self.reg_password.pack(
            fill="x",
            padx=50,
            pady=(4, 10),
            ipady=5
        )

        
        # CONFIRM PASSWORD
       
        tk.Label(
            card,
            text="Confirm Password",
            font=("Segoe UI", 10, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(anchor="w", padx=50)

        self.reg_confirm = tk.Entry(
            card,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="solid",
            bd=1,
            show="*"
        )
        self.reg_confirm.pack(
            fill="x",
            padx=50,
            pady=(4, 15),
            ipady=5
        )

        
        # CREATE ACCOUNT
       

        tk.Button(
            card,
            text="CREATE ACCOUNT",
            command=self.register_user,
            bg=self.GREEN,
            fg=self.WHITE,
            activebackground="#247A49",
            activeforeground=self.WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            fill="x",
            padx=50,
            pady=5,
            ipady=7
        )

       
        # BACK
      

        tk.Button(
            card,
            text="Back to Login",
            command=self.show_login,
            bg=self.WHITE,
            fg=self.BLUE,
            activebackground=self.WHITE,
            activeforeground=self.NAVY,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(pady=8)

   
    # REGISTER USER
   
    def register_user(self):

        full_name = self.reg_name.get().strip()
        phone = self.reg_phone.get().strip()
        role = self.reg_role.get()
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()

        if not full_name or not phone or not username or not password:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        if len(username) < 3:
            messagebox.showwarning(
                "Invalid Username",
                "Username must contain at least 3 characters."
            )
            return

        if " " in username:
            messagebox.showwarning(
                "Invalid Username",
                "Username cannot contain spaces."
            )
            return

        if len(password) < 4:
            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 4 characters."
            )
            return

        if password != confirm:
            messagebox.showerror(
                "Password Error",
                "Passwords do not match."
            )
            return

        # CHECK USERNAME
        self.cursor.execute(
            "SELECT id FROM users WHERE username=?",
            (username,)
        )

        if self.cursor.fetchone():
            messagebox.showerror(
                "Username Exists",
                "This username is already registered."
            )
            return

        # INSERT USER
        self.cursor.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))

        self.db.commit()

        messagebox.showinfo(
            "Registration Successful",
            "Account created successfully.\n"
            "You can now login."
        )

        self.show_login()

        # Fill username
        self.login_username.insert(0, username)
        self.login_role.set(role)

   
    # ADMIN DASHBOARD
   

    def show_admin_dashboard(self):

        self.clear_window()

        # IMPORTANT:
        # KEEP ADMIN DASHBOARD DESIGN AND SIZE
        self.root.geometry("1150x700")
        self.root.minsize(1000, 650)

       
        # HEADER
      

        header = tk.Frame(
            self.root,
            bg=self.NAVY,
            height=85
        )
        header.pack(
            fill="x"
        )
        header.pack_propagate(False)

        title_frame = tk.Frame(
            header,
            bg=self.NAVY
        )
        title_frame.pack(
            side="left",
            padx=25
        )

        tk.Label(
            title_frame,
            text="Device Repair Tracker",
            font=("Segoe UI", 22, "bold"),
            bg=self.NAVY,
            fg=self.WHITE
        ).pack(anchor="w", pady=(13, 0))

        tk.Label(
            title_frame,
            text="Admin Dashboard • Manage all repair records",
            font=("Segoe UI", 9),
            bg=self.NAVY,
            fg="#C9D9E8"
        ).pack(anchor="w")

       
        # LOGOUT
       

        tk.Button(
            header,
            text="LOGOUT",
            command=self.logout,
            bg=self.RED,
            fg=self.WHITE,
            activebackground="#A92F2F",
            activeforeground=self.WHITE,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=18
        ).pack(
            side="right",
            padx=20,
            pady=25
        )

        tk.Label(
            header,
            text="ADMIN",
            font=("Segoe UI", 10, "bold"),
            bg=self.NAVY,
            fg="#8FD3FF"
        ).pack(
            side="right",
            padx=10
        )

        
        # MAIN
        

        main = tk.Frame(
            self.root,
            bg=self.BG
        )
        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

       
        # FORM CARD
       

        form_card = tk.Frame(
            main,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        form_card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            form_card,
            text="Repair Information",
            font=("Segoe UI", 13, "bold"),
            bg=self.WHITE,
            fg=self.NAVY
        ).grid(
            row=0,
            column=0,
            columnspan=6,
            sticky="w",
            padx=15,
            pady=(10, 8)
        )

       
        # CUSTOMER NAME
    

        tk.Label(
            form_card,
            text="Customer Name",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(15, 5),
            pady=3
        )

        self.customer_name = tk.Entry(
            form_card,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.customer_name.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=(15, 5),
            pady=(0, 8),
            ipady=4
        )

       
        # PHONE
       
        tk.Label(
            form_card,
            text="Phone",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=5,
            pady=3
        )

        self.phone = tk.Entry(
            form_card,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.phone.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=5,
            pady=(0, 8),
            ipady=4
        )

       
        # DEVICE TYPE
        
        tk.Label(
            form_card,
            text="Device Type",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=5,
            pady=3
        )

        self.device_type = ttk.Combobox(
            form_card,
            values=[
                "Laptop",
                "Desktop",
                "Mobile Phone",
                "Tablet",
                "Printer",
                "Router",
                "Other"
            ],
            state="readonly",
            font=("Segoe UI", 9)
        )
        self.device_type.grid(
            row=2,
            column=2,
            sticky="ew",
            padx=5,
            pady=(0, 8),
            ipady=3
        )

       
        # DEVICE MODEL
       
        tk.Label(
            form_card,
            text="Device Model",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).grid(
            row=1,
            column=3,
            sticky="w",
            padx=5,
            pady=3
        )

        self.device_model = tk.Entry(
            form_card,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.device_model.grid(
            row=2,
            column=3,
            sticky="ew",
            padx=5,
            pady=(0, 8),
            ipady=4
        )

       
        # STATUS

        tk.Label(
            form_card,
            text="Repair Status",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).grid(
            row=1,
            column=4,
            sticky="w",
            padx=5,
            pady=3
        )

        self.repair_status = ttk.Combobox(
            form_card,
            values=[
                "Pending",
                "In Progress",
                "Ready",
                "Completed",
                "Cancelled"
            ],
            state="readonly",
            font=("Segoe UI", 9)
        )
        self.repair_status.grid(
            row=2,
            column=4,
            sticky="ew",
            padx=5,
            pady=(0, 8),
            ipady=3
        )

        
        # COST


        tk.Label(
            form_card,
            text="Repair Cost",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).grid(
            row=1,
            column=5,
            sticky="w",
            padx=(5, 15),
            pady=3
        )

        self.repair_cost = tk.Entry(
            form_card,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.repair_cost.grid(
            row=2,
            column=5,
            sticky="ew",
            padx=(5, 15),
            pady=(0, 8),
            ipady=4
        )

       
        # SECOND ROW

        tk.Label(
            form_card,
            text="Repair Date",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=(15, 5)
        )

        self.repair_date = tk.Entry(
            form_card,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.repair_date.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=(15, 5),
            pady=(3, 8),
            ipady=4
        )

        self.repair_date.insert(
            0,
            str(date.today())
        )

        
        # PROBLEM


        tk.Label(
            form_card,
            text="Problem",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).grid(
            row=3,
            column=1,
            columnspan=4,
            sticky="w",
            padx=5
        )

        self.problem = tk.Entry(
            form_card,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.problem.grid(
            row=4,
            column=1,
            columnspan=4,
            sticky="ew",
            padx=5,
            pady=(3, 8),
            ipady=4
        )

       
        # FORM BUTTONS

        button_frame = tk.Frame(
            form_card,
            bg=self.WHITE
        )
        button_frame.grid(
            row=4,
            column=5,
            padx=(5, 15),
            pady=3,
            sticky="ew"
        )

        tk.Button(
            button_frame,
            text="ADD RECORD",
            command=self.add_record,
            bg=self.GREEN,
            fg=self.WHITE,
            activebackground="#247A49",
            activeforeground=self.WHITE,
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            padx=2,
            fill="x",
            expand=True
        )

        tk.Button(
            button_frame,
            text="UPDATE",
            command=self.update_record,
            bg=self.BLUE,
            fg=self.WHITE,
            activebackground=self.NAVY,
            activeforeground=self.WHITE,
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            padx=2,
            fill="x",
            expand=True
        )

        tk.Button(
            button_frame,
            text="DELETE",
            command=self.delete_record,
            bg=self.RED,
            fg=self.WHITE,
            activebackground="#A92F2F",
            activeforeground=self.WHITE,
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            padx=2,
            fill="x",
            expand=True
        )

        tk.Button(
            button_frame,
            text="CLEAR",
            command=self.clear_form,
            bg=self.GRAY,
            fg=self.WHITE,
            activebackground="#4B5563",
            activeforeground=self.WHITE,
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            padx=2,
            fill="x",
            expand=True
        )

        for i in range(6):
            form_card.columnconfigure(i, weight=1)

       
        # SEARCH CARD
       

        search_card = tk.Frame(
            main,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        search_card.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            search_card,
            text="Search:",
            font=("Segoe UI", 9, "bold"),
            bg=self.WHITE,
            fg=self.TEXT
        ).pack(
            side="left",
            padx=(15, 5),
            pady=9
        )

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            search_card,
            textvariable=self.search_var,
            font=("Segoe UI", 9),
            bg="#F8FAFC",
            relief="solid",
            bd=1
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5,
            pady=7,
            ipady=4
        )

        self.search_var.trace_add(
            "write",
            lambda *args: self.load_admin_records()
        )

        tk.Button(
            search_card,
            text="EXPORT CSV",
            command=self.export_csv,
            bg=self.PURPLE,
            fg=self.WHITE,
            activebackground="#5D3E89",
            activeforeground=self.WHITE,
            font=("Segoe UI", 8, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            side="right",
            padx=15,
            pady=7,
            ipadx=10,
            ipady=4
        )

       
        # TABLE
       

        table_card = tk.Frame(
            main,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        table_card.pack(
            fill="both",
            expand=True
        )

        columns = (
            "ID",
            "Customer",
            "Phone",
            "Device",
            "Model",
            "Problem",
            "Status",
            "Cost",
            "Date"
        )

        self.admin_tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings"
        )

        widths = {
            "ID": 45,
            "Customer": 120,
            "Phone": 100,
            "Device": 100,
            "Model": 110,
            "Problem": 180,
            "Status": 100,
            "Cost": 80,
            "Date": 95
        }

        for col in columns:

            self.admin_tree.heading(
                col,
                text=col,
                command=lambda c=col: self.sort_admin_tree(c, False)
            )

            self.admin_tree.column(
                col,
                width=widths[col],
                anchor="center"
            )

        scrollbar_y = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=self.admin_tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_card,
            orient="horizontal",
            command=self.admin_tree.xview
        )

        self.admin_tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.admin_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        scrollbar_x.pack(
            side="bottom",
            fill="x"
        )

        self.admin_tree.bind(
            "<<TreeviewSelect>>",
            self.select_record
        )

        self.load_admin_records()

    
    # LOAD ADMIN RECORDS
   

    def load_admin_records(self):

        if not hasattr(self, "admin_tree"):
            return

        for item in self.admin_tree.get_children():
            self.admin_tree.delete(item)

        search = self.search_var.get().strip()

        if search:

            search_value = f"%{search}%"

            self.cursor.execute("""
                SELECT
                    id,
                    customer_name,
                    phone,
                    device_type,
                    device_model,
                    problem,
                    repair_status,
                    repair_cost,
                    repair_date
                FROM repairs
                WHERE
                    customer_name LIKE ?
                    OR phone LIKE ?
                    OR device_type LIKE ?
                    OR device_model LIKE ?
                    OR problem LIKE ?
                    OR repair_status LIKE ?
                    OR repair_date LIKE ?
                ORDER BY id DESC
            """, (
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value,
                search_value
            ))

        else:

            self.cursor.execute("""
                SELECT
                    id,
                    customer_name,
                    phone,
                    device_type,
                    device_model,
                    problem,
                    repair_status,
                    repair_cost,
                    repair_date
                FROM repairs
                ORDER BY id DESC
            """)

        records = self.cursor.fetchall()

        for record in records:

            self.admin_tree.insert(
                "",
                "end",
                values=record
            )

   
    # SELECT ADMIN RECORD
    
    def select_record(self, event=None):

        selected = self.admin_tree.selection()

        if not selected:
            return

        item = self.admin_tree.item(selected[0])

        values = item["values"]

        if not values:
            return

        self.selected_id = values[0]

        self.customer_name.delete(0, tk.END)
        self.customer_name.insert(0, values[1])

        self.phone.delete(0, tk.END)
        self.phone.insert(0, values[2])

        self.device_type.set(values[3])

        self.device_model.delete(0, tk.END)
        self.device_model.insert(0, values[4])

        self.problem.delete(0, tk.END)
        self.problem.insert(0, values[5])

        self.repair_status.set(values[6])

        self.repair_cost.delete(0, tk.END)
        self.repair_cost.insert(0, values[7])

        self.repair_date.delete(0, tk.END)
        self.repair_date.insert(0, values[8])

        # Get username internally
        self.cursor.execute(
            "SELECT customer_username FROM repairs WHERE id=?",
            (self.selected_id,)
        )

        result = self.cursor.fetchone()

        if result:
            self.last_customer_username = result[0]

    
    # ADD RECORD
    
    def add_record(self):

        customer_name = self.customer_name.get().strip()
        phone = self.phone.get().strip()
        device_type = self.device_type.get()
        device_model = self.device_model.get().strip()
        problem = self.problem.get().strip()
        status = self.repair_status.get()
        cost = self.repair_cost.get().strip()
        repair_date = self.repair_date.get().strip()

        if not customer_name:
            messagebox.showwarning(
                "Missing Information",
                "Please enter customer name."
            )
            return

        if not phone:
            messagebox.showwarning(
                "Missing Information",
                "Please enter phone number."
            )
            return

        if not device_type:
            messagebox.showwarning(
                "Missing Information",
                "Please select device type."
            )
            return

        if not device_model:
            messagebox.showwarning(
                "Missing Information",
                "Please enter device model."
            )
            return

        if not problem:
            messagebox.showwarning(
                "Missing Information",
                "Please enter the problem."
            )
            return

        if not status:
            messagebox.showwarning(
                "Missing Information",
                "Please select repair status."
            )
            return

        if not cost:
            messagebox.showwarning(
                "Missing Information",
                "Please enter repair cost."
            )
            return

        try:
            cost = float(cost)

            if cost < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Cost",
                "Repair cost must be a valid positive number."
            )
            return

       
        # SELECT CUSTOMER ACCOUNT
      

        customer_username = self.select_customer()

        if customer_username is None:
            return

        self.cursor.execute("""
            INSERT INTO repairs (
                customer_username,
                customer_name,
                phone,
                device_type,
                device_model,
                problem,
                repair_status,
                repair_cost,
                repair_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_username,
            customer_name,
            phone,
            device_type,
            device_model,
            problem,
            status,
            cost,
            repair_date
        ))

        self.db.commit()

        messagebox.showinfo(
            "Success",
            "Repair record added successfully."
        )

        self.clear_form()
        self.load_admin_records()


    # SELECT CUSTOMER

    def select_customer(self):

        popup = tk.Toplevel(self.root)

        popup.title("Select Customer")

        popup.geometry("400x450")

        popup.configure(
            bg=self.BG
        )

        popup.transient(self.root)
        popup.grab_set()

        tk.Label(
            popup,
            text="Select Customer Account",
            font=("Segoe UI", 16, "bold"),
            bg=self.BG,
            fg=self.NAVY
        ).pack(pady=20)

        list_frame = tk.Frame(
            popup,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        list_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 11),
            bg=self.WHITE,
            fg=self.TEXT,
            selectbackground=self.BLUE,
            selectforeground=self.WHITE,
            relief="flat"
        )

        listbox.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.cursor.execute("""
            SELECT username
            FROM users
            WHERE role='Customer'
            ORDER BY username
        """)

        customers = self.cursor.fetchall()

        for customer in customers:
            listbox.insert(
                tk.END,
                customer[0]
            )

        selected_customer = {
            "username": None
        }

        def choose_customer():

            selection = listbox.curselection()

            if not selection:

                messagebox.showwarning(
                    "Select Customer",
                    "Please select a customer.",
                    parent=popup
                )

                return

            selected_customer["username"] = listbox.get(
                selection[0]
            )

            popup.destroy()

        tk.Button(
            popup,
            text="SELECT CUSTOMER",
            command=choose_customer,
            bg=self.GREEN,
            fg=self.WHITE,
            activebackground="#247A49",
            activeforeground=self.WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(
            fill="x",
            padx=20,
            pady=15,
            ipady=7
        )

        self.root.wait_window(popup)

        return selected_customer["username"]

   
    # UPDATE RECORD
   
    def update_record(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a record to update."
            )

            return

        customer_name = self.customer_name.get().strip()
        phone = self.phone.get().strip()
        device_type = self.device_type.get()
        device_model = self.device_model.get().strip()
        problem = self.problem.get().strip()
        status = self.repair_status.get()
        cost = self.repair_cost.get().strip()
        repair_date = self.repair_date.get().strip()

        if not customer_name or not phone or not device_type:
            messagebox.showwarning(
                "Missing Information",
                "Please complete the customer and device information."
            )
            return

        if not device_model or not problem:
            messagebox.showwarning(
                "Missing Information",
                "Please complete the repair information."
            )
            return

        try:

            cost = float(cost)

            if cost < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Cost",
                "Repair cost must be a valid number."
            )

            return

        self.cursor.execute("""
            UPDATE repairs
            SET
                customer_name=?,
                phone=?,
                device_type=?,
                device_model=?,
                problem=?,
                repair_status=?,
                repair_cost=?,
                repair_date=?
            WHERE id=?
        """, (
            customer_name,
            phone,
            device_type,
            device_model,
            problem,
            status,
            cost,
            repair_date,
            self.selected_id
        ))

        self.db.commit()

        messagebox.showinfo(
            "Success",
            "Repair record updated successfully."
        )

        self.clear_form()
        self.load_admin_records()

   
    # DELETE RECORD
   

    def delete_record(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "No Selection",
                "Please select a record to delete."
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this record?"
        )

        if not answer:
            return

        self.cursor.execute(
            "DELETE FROM repairs WHERE id=?",
            (self.selected_id,)
        )

        self.db.commit()

        messagebox.showinfo(
            "Deleted",
            "Repair record deleted successfully."
        )

        self.clear_form()
        self.load_admin_records()

   
    # CLEAR FORM
  

    def clear_form(self):

        self.selected_id = None
        self.last_customer_username = ""

        if hasattr(self, "customer_name"):
            self.customer_name.delete(0, tk.END)

        if hasattr(self, "phone"):
            self.phone.delete(0, tk.END)

        if hasattr(self, "device_type"):
            self.device_type.set("")

        if hasattr(self, "device_model"):
            self.device_model.delete(0, tk.END)

        if hasattr(self, "problem"):
            self.problem.delete(0, tk.END)

        if hasattr(self, "repair_status"):
            self.repair_status.set("Pending")

        if hasattr(self, "repair_cost"):
            self.repair_cost.delete(0, tk.END)

        if hasattr(self, "repair_date"):
            self.repair_date.delete(0, tk.END)
            self.repair_date.insert(
                0,
                str(date.today())
            )


    # SORT ADMIN TABLE

    def sort_admin_tree(self, column, reverse):

        data = [
            (
                self.admin_tree.set(item, column),
                item
            )
            for item in self.admin_tree.get_children("")
        ]

        try:

            data.sort(
                key=lambda x: float(x[0]),
                reverse=reverse
            )

        except ValueError:

            data.sort(
                key=lambda x: x[0].lower(),
                reverse=reverse
            )

        for index, (_, item) in enumerate(data):
            self.admin_tree.move(
                item,
                "",
                index
            )

        self.admin_tree.heading(
            column,
            command=lambda: self.sort_admin_tree(
                column,
                not reverse
            )
        )

   
    # EXPORT CSV


    def export_csv(self):

        records = []

        for item in self.admin_tree.get_children():

            records.append(
                self.admin_tree.item(item)["values"]
            )

        if not records:

            messagebox.showwarning(
                "No Records",
                "There are no records to export."
            )

            return

        filename = filedialog.asksaveasfilename(
            title="Save CSV File",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ]
        )

        if not filename:
            return

        headers = [
            "ID",
            "Customer",
            "Phone",
            "Device",
            "Model",
            "Problem",
            "Status",
            "Cost",
            "Date"
        ]

        try:

            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(headers)

                writer.writerows(records)

            messagebox.showinfo(
                "Export Successful",
                "Repair records exported successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

   
    # CUSTOMER DASHBOARD

    def show_customer_dashboard(self):

        self.clear_window()

        # CUSTOMER DASHBOARD CAN BE SMALLER
        self.root.geometry("950x600")
        self.root.minsize(850, 550)

       
        # HEADER


        header = tk.Frame(
            self.root,
            bg=self.NAVY,
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title_frame = tk.Frame(
            header,
            bg=self.NAVY
        )

        title_frame.pack(
            side="left",
            padx=25
        )

        tk.Label(
            title_frame,
            text="Device Repair Tracker",
            font=("Segoe UI", 21, "bold"),
            bg=self.NAVY,
            fg=self.WHITE
        ).pack(
            anchor="w",
            pady=(12, 0)
        )

        tk.Label(
            title_frame,
            text="Customer Dashboard • View your repair records",
            font=("Segoe UI", 9),
            bg=self.NAVY,
            fg="#C9D9E8"
        ).pack(
            anchor="w"
        )

    
        # ROLE
    

        tk.Label(
            header,
            text="CUSTOMER",
            font=("Segoe UI", 10, "bold"),
            bg=self.NAVY,
            fg="#8FD3FF"
        ).pack(
            side="right",
            padx=20
        )

        
        # MAIN
    

        main = tk.Frame(
            self.root,
            bg=self.BG
        )

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )


        # WELCOME

        tk.Label(
            main,
            text="Welcome!",
            font=("Segoe UI", 20, "bold"),
            bg=self.BG,
            fg=self.NAVY
        ).pack(
            anchor="w"
        )

        tk.Label(
            main,
            text="Here you can view the repair status of your devices.",
            font=("Segoe UI", 10),
            bg=self.BG,
            fg=self.GRAY
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

    
        # STATISTICS

        stats_frame = tk.Frame(
            main,
            bg=self.BG
        )

        stats_frame.pack(
            fill="x",
            pady=(0, 12)
        )

        # TOTAL
        total_card = tk.Frame(
            stats_frame,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        total_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        self.customer_total_label = tk.Label(
            total_card,
            text="0",
            font=("Segoe UI", 22, "bold"),
            bg=self.WHITE,
            fg=self.BLUE
        )

        self.customer_total_label.pack(
            pady=(10, 0)
        )

        tk.Label(
            total_card,
            text="Total Repairs",
            font=("Segoe UI", 9),
            bg=self.WHITE,
            fg=self.GRAY
        ).pack(
            pady=(0, 10)
        )

        # IN PROGRESS
        progress_card = tk.Frame(
            stats_frame,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        progress_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=7
        )

        self.customer_progress_label = tk.Label(
            progress_card,
            text="0",
            font=("Segoe UI", 22, "bold"),
            bg=self.WHITE,
            fg=self.ORANGE
        )

        self.customer_progress_label.pack(
            pady=(10, 0)
        )

        tk.Label(
            progress_card,
            text="In Progress",
            font=("Segoe UI", 9),
            bg=self.WHITE,
            fg=self.GRAY
        ).pack(
            pady=(0, 10)
        )

        # READY
        ready_card = tk.Frame(
            stats_frame,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        ready_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        self.customer_ready_label = tk.Label(
            ready_card,
            text="0",
            font=("Segoe UI", 22, "bold"),
            bg=self.WHITE,
            fg=self.GREEN
        )

        self.customer_ready_label.pack(
            pady=(10, 0)
        )

        tk.Label(
            ready_card,
            text="Ready",
            font=("Segoe UI", 9),
            bg=self.WHITE,
            fg=self.GRAY
        ).pack(
            pady=(0, 10)
        )

        # =========================
        # TABLE
        # =========================

        table_card = tk.Frame(
            main,
            bg=self.WHITE,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        table_card.pack(
            fill="both",
            expand=True
        )

        # IMPORTANT:
        # CUSTOMER DOES NOT SEE:
        # - OTHER CUSTOMER NAMES
        # - PHONE NUMBERS
        #
        # CUSTOMER ONLY SEES THEIR OWN:
        # ID, DEVICE, MODEL, PROBLEM, STATUS, COST, DATE

        columns = (
            "ID",
            "Device",
            "Model",
            "Problem",
            "Status",
            "Cost",
            "Date"
        )

        self.customer_tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings"
        )

        widths = {
            "ID": 50,
            "Device": 130,
            "Model": 150,
            "Problem": 250,
            "Status": 120,
            "Cost": 100,
            "Date": 110
        }

        for col in columns:

            self.customer_tree.heading(
                col,
                text=col
            )

            self.customer_tree.column(
                col,
                width=widths[col],
                anchor="center"
            )

        scrollbar_y = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=self.customer_tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_card,
            orient="horizontal",
            command=self.customer_tree.xview
        )

        self.customer_tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.customer_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        scrollbar_x.pack(
            side="bottom",
            fill="x"
        )

       
        # BOTTOM BUTTONS
        
        bottom = tk.Frame(
            main,
            bg=self.BG
        )

        bottom.pack(
            fill="x",
            pady=(10, 0)
        )

        tk.Button(
            bottom,
            text="REFRESH",
            command=self.load_customer_records,
            bg=self.BLUE,
            fg=self.WHITE,
            activebackground=self.NAVY,
            activeforeground=self.WHITE,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20
        ).pack(
            side="left"
        )

        tk.Button(
            bottom,
            text="LOGOUT",
            command=self.logout,
            bg=self.RED,
            fg=self.WHITE,
            activebackground="#A92F2F",
            activeforeground=self.WHITE,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20
        ).pack(
            side="right"
        )

        # LOAD ONLY CURRENT CUSTOMER DATA
        self.load_customer_records()

    
    # LOAD CUSTOMER RECORDS
    

    def load_customer_records(self):

        if not hasattr(self, "customer_tree"):
            return

        
        # CLEAR TABLE
        

        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)

        
        # IMPORTANT PRIVACY QUERY
       
        # ONLY records belonging to
        # the logged-in username
        # are selected.
        #
        # Other customers' records
        # are never loaded.
        

        self.cursor.execute("""
            SELECT
                id,
                device_type,
                device_model,
                problem,
                repair_status,
                repair_cost,
                repair_date
            FROM repairs
            WHERE customer_username=?
            ORDER BY id DESC
        """, (self.current_username,))

        records = self.cursor.fetchall()


        # INSERT ONLY OWN RECORDS

        for record in records:

            self.customer_tree.insert(
                "",
                "end",
                values=record
            )

        # UPDATE STATISTICS
        total = len(records)

        in_progress = sum(
            1
            for record in records
            if record[4] == "In Progress"
        )

        ready = sum(
            1
            for record in records
            if record[4] == "Ready"
        )

        self.customer_total_label.config(
            text=str(total)
        )

        self.customer_progress_label.config(
            text=str(in_progress)
        )

        self.customer_ready_label.config(
            text=str(ready)
        )

    # LOGOUT

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if not answer:
            return


        # CLEAR LOGIN SESSION

        self.current_user_id = None
        self.current_username = ""
        self.current_role = ""

        self.selected_id = None
        self.last_customer_username = ""

       
        # RETURN TO LOGIN

        self.show_login()


    # CLOSE DATABASE
   

    def close_database(self):

        try:
            self.db.close()
        except:
            pass

        self.root.destroy()


# RUN APPLICATION


if __name__ == "__main__":

    root = tk.Tk()

    app = DeviceRepairTracker(root)

    root.mainloop()