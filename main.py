import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import math
import time
from PIL import Image, ImageTk
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- DATABASE LAYER ---
class Database:
    def __init__(self):
        self.con = sqlite3.connect(database="srms.db")
        self.cur = self.con.cursor()
        self.create_tables()

    def create_tables(self):
        # 1. User Table for Auth (Fixed)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            fname text, 
            lname text, 
            contact text, 
            email text, 
            question text, 
            answer text, 
            password text)""")
        
        # 2. Course Table (With UNIQUE name constraint)
        self.cur.execute("""CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY AUTOINCREMENT, 
            name text UNIQUE, 
            duration text, 
            charges text, 
            description text)""")
            
        # 3. Student Table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS student(
            roll INTEGER PRIMARY KEY, 
            name text, 
            email text, 
            gender text, 
            dob text, 
            contact text, 
            admission text, 
            course text, 
            state text, 
            city text, 
            pin text, 
            address text)""")
            
        # 4. Result Table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS result(
            rid INTEGER PRIMARY KEY AUTOINCREMENT, 
            roll text, 
            name text, 
            course text, 
            marks text, 
            full_marks text, 
            per text)""")
            
        self.con.commit()

# --- REGISTRATION MODULE ---
class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")
        self.root.focus_force()
        self.db = Database()

        # Variables
        self.var_fname, self.var_lname = tk.StringVar(), tk.StringVar()
        self.var_contact, self.var_email = tk.StringVar(), tk.StringVar()
        self.var_question, self.var_answer = tk.StringVar(), tk.StringVar()
        self.var_password, self.var_conf_password = tk.StringVar(), tk.StringVar()
        self.var_chk = tk.IntVar()

        # UI Layout - UPDATED PATH
        self.side_img = ImageTk.PhotoImage(file=resource_path("images/side.png"))
        tk.Label(self.root, image=self.side_img, bd=0).place(x=50, y=100, width=400, height=500)

        reg_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.RIDGE)
        reg_frame.place(x=450, y=100, width=800, height=500)

        tk.Label(reg_frame, text="REGISTER HERE", font=("times new roman", 30, "bold"), bg="white", fg="green").place(x=50, y=30)

        # Fields (Simplified placement for clarity)
        fields = [
            ("First Name", self.var_fname, 50, 100), ("Last Name", self.var_lname, 370, 100),
            ("Contact No.", self.var_contact, 50, 170), ("Email", self.var_email, 370, 170),
            ("Answer", self.var_answer, 370, 240), ("Password", self.var_password, 50, 310),
            ("Confirm Password", self.var_conf_password, 370, 310)
        ]
        for label, var, x, y in fields:
            tk.Label(reg_frame, text=label, font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=x, y=y)
            tk.Entry(reg_frame, textvariable=var, font=("times new roman", 15), bg="lightgray", show="*" if "Password" in label else "").place(x=x, y=y+30, width=250)

        # Question Dropdown
        tk.Label(reg_frame, text="Security Question", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=240)
        self.cmb_quest = ttk.Combobox(reg_frame, textvariable=self.var_question, font=("times new roman", 13), state='readonly', justify=tk.CENTER)
        self.cmb_quest['values'] = ("Select", "Your First Pet Name", "Your Birth Place", "Your Best Friend Name")
        self.cmb_quest.place(x=50, y=270, width=250)
        self.cmb_quest.current(0)

        tk.Checkbutton(reg_frame, text="I Agree The Terms & Conditions", variable=self.var_chk, onvalue=1, offvalue=0, bg="white", font=("times new roman", 12)).place(x=50, y=380)
        
        # UPDATED PATH
        self.btn_img = ImageTk.PhotoImage(file=resource_path("images/register.png"))
        tk.Button(reg_frame, image=self.btn_img, bd=0, cursor="hand2", command=self.register_data).place(x=50, y=420)

    def register_data(self):
        if self.var_fname.get() == "" or self.var_email.get() == "" or self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please fill all fields and agree to terms", parent=self.root)
        elif self.var_password.get() != self.var_conf_password.get():
            messagebox.showerror("Error", "Passwords do not match", parent=self.root)
        else:
            self.db.cur.execute("INSERT INTO user (fname, lname, contact, email, question, answer, password) VALUES(?,?,?,?,?,?,?)",
                                (self.var_fname.get(), self.var_lname.get(), self.var_contact.get(), self.var_email.get(), self.var_question.get(), self.var_answer.get(), self.var_password.get()))
            self.db.con.commit()
            messagebox.showinfo("Success", "Registration Successful!", parent=self.root)
            self.root.destroy()

# --- LOGIN SYSTEM ---
class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1350x700+0+0")
        self.db = Database()

        self.var_email, self.var_password = tk.StringVar(), tk.StringVar()

        # Background - UPDATED PATH
        self.bg_img = ImageTk.PhotoImage(file=resource_path("images/bg.png"))
        tk.Label(self.root, image=self.bg_img).place(x=0, y=0, relwidth=1, relheight=1)

        login_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="white")
        login_frame.place(x=400, y=100, width=500, height=450)

        tk.Label(login_frame, text="LOGIN", font=("times new roman", 30, "bold"), bg="white", fg="#00759E").pack(pady=30)
        
        tk.Label(login_frame, text="Email Address", font=("times new roman", 15), bg="white").pack()
        tk.Entry(login_frame, textvariable=self.var_email, font=("times new roman", 15), bg="lightgray").pack(pady=10, padx=50, fill=tk.X)

        tk.Label(login_frame, text="Password", font=("times new roman", 15), bg="white").pack()
        tk.Entry(login_frame, textvariable=self.var_password, show="*", font=("times new roman", 15), bg="lightgray").pack(pady=10, padx=50, fill=tk.X)

        tk.Button(login_frame, text="Login", command=self.login, font=("times new roman", 18), bg="#00759E", fg="white", cursor="hand2").pack(pady=20, padx=50, fill=tk.X)
        tk.Button(login_frame, text="Register New Account?", command=self.register_window, bd=0, bg="white", fg="red", cursor="hand2").pack()

    def register_window(self):
        self.new_win = tk.Toplevel(self.root)
        self.reg_obj = Register(self.new_win)

    def login(self):
        self.db.cur.execute("SELECT * FROM user WHERE email=? AND password=?", (self.var_email.get(), self.var_password.get()))
        row = self.db.cur.fetchone()
        if row:
            self.root.destroy()
            dashboard_root = tk.Tk()
            Dashboard(dashboard_root)
        else:
            messagebox.showerror("Error", "Invalid Credentials")

# --- DASHBOARD ---
class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        self.db = Database()
        
        # --- HEADER - UPDATED PATH ---
        self.logo_p = ImageTk.PhotoImage(file=resource_path("images/logo_p.png"))
        tk.Label(self.root, text="Student Result Management System", image=self.logo_p, compound=tk.LEFT, 
                 font=("goudy old style", 40, "bold"), bg="#033054", fg="white", padx=20).place(x=0, y=0, relwidth=1, height=70)

        # --- MENU BAR ---
        M_Frame = tk.LabelFrame(self.root, text="Menus", font=("times new roman", 15), bg="white")
        M_Frame.place(x=10, y=70, width=1330, height=80)
        
        # Navigation Buttons
        btn_course = tk.Button(M_Frame, text="Course", command=self.add_course, font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2").place(x=20, y=5, width=200, height=40)
        btn_student = tk.Button(M_Frame, text="Student", command=self.add_student, font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2").place(x=240, y=5, width=200, height=40)
        btn_result = tk.Button(M_Frame, text="Result", command=self.add_result, font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2").place(x=460, y=5, width=200, height=40)
        btn_view = tk.Button(M_Frame, text="View Student Result", command=self.view_result, font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2").place(x=680, y=5, width=200, height=40)
        btn_logout = tk.Button(M_Frame, text="Logout", command=self.logout, font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2").place(x=900, y=5, width=200, height=40)
        btn_exit = tk.Button(M_Frame, text="Exit", command=self.exit_app, font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2").place(x=1120, y=5, width=190, height=40)

        # --- CONTENT AREA ---
        # Left Side: Static Image (Using clock_new.png or similar from your assets)
        self.lbl_clock_container = tk.Label(self.root, text="\nWebCode Clock", font=("Book Antiqua", 25, "bold"), fg="white", compound=tk.BOTTOM, bg="#081923", bd=10, relief=tk.RIDGE)
        self.lbl_clock_container.place(x=10, y=180, width=350, height=450)
        
        self.clock_canvas = tk.Canvas(self.lbl_clock_container, bg="#081923", bd=0, highlightthickness=0)
        self.clock_canvas.place(x=25, y=50, width=300, height=300)
        
        # Center: Main Background Image - UPDATED PATH
        self.bg_img = ImageTk.PhotoImage(file=resource_path("images/bg.png"))
        tk.Label(self.root, image=self.bg_img).place(x=400, y=180, width=920, height=350)

        # --- STATS WIDGETS ---
        self.lbl_student = tk.Label(self.root, text="Total Students\n[ 0 ]", font=("goudy old style", 20, "bold"), bd=10, relief=tk.RIDGE, bg="#e43b06", fg="white")
        self.lbl_student.place(x=400, y=530, width=300, height=100)
        
        self.lbl_course = tk.Label(self.root, text="Total Course\n[ 0 ]", font=("goudy old style", 20, "bold"), bd=10, relief=tk.RIDGE, bg="#0676ad", fg="white")
        self.lbl_course.place(x=710, y=530, width=300, height=100)
        
        self.lbl_result = tk.Label(self.root, text="Total Results\n[ 0 ]", font=("goudy old style", 20, "bold"), bd=10, relief=tk.RIDGE, bg="#038074", fg="white")
        self.lbl_result.place(x=1020, y=530, width=300, height=100)

        # --- FOOTER ---
        footer_text = "SRMS-Student Result Management System | Developed By YourName\nEmail Us: WebCode867@gmail.com"
        tk.Label(self.root, text=footer_text, font=("times new roman", 12), bg="#262626", fg="white").pack(side=tk.BOTTOM, fill=tk.X)

        self.update_details()
        self.update_clock()
    
    def add_course(self):
        self.new_win = tk.Toplevel(self.root)
        self.course_obj = CourseClass(self.new_win)

    def add_student(self):
        self.new_win = tk.Toplevel(self.root)
        self.student_obj = StudentClass(self.new_win)

    def add_result(self):
        self.new_win = tk.Toplevel(self.root)
        self.result_obj = ResultClass(self.new_win)

    def view_result(self):
        self.new_win = tk.Toplevel(self.root)
        self.view_obj = ViewResultClass(self.new_win)

    def logout(self):
        op = messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root)
        if op:
            self.root.destroy()           
            login_root = tk.Tk()          
            LoginSystem(login_root)       

    def exit_app(self):
        op = messagebox.askyesno("Confirm", "Do you really want to Exit?")
        if op:
            self.root.destroy()

    def update_details(self):
        try:
            # 1. Fetch Total Students
            self.db.cur.execute("SELECT * FROM student")
            st = self.db.cur.fetchall()
            self.lbl_student.config(text=f"Total Students\n[ {str(len(st))} ]")

            # 2. Fetch Total Courses
            self.db.cur.execute("SELECT * FROM course")
            cr = self.db.cur.fetchall()
            self.lbl_course.config(text=f"Total Course\n[ {str(len(cr))} ]")

            # 3. Fetch Total Results
            self.db.cur.execute("SELECT * FROM result")
            rs = self.db.cur.fetchall()
            self.lbl_result.config(text=f"Total Results\n[ {str(len(rs))} ]")

            # 4. Auto-refresh every 2 seconds (2000 milliseconds)
            self.lbl_student.after(2000, self.update_details)
            
        except Exception as ex:
            pass # If the window closes, it silently catches the error

    def update_clock(self):
        try:
            # Get Current Time
            h = int(time.strftime("%I"))
            m = int(time.strftime("%M"))
            s = int(time.strftime("%S"))

            # Calculate Angles for hands
            hr_angle = (h + m/60) * (360/12) - 90
            min_angle = (m + s/60) * (360/60) - 90
            sec_angle = s * (360/60) - 90

            cx, cy = 150, 150
            radius = 120

            # Clear the canvas every second before redrawing
            self.clock_canvas.delete("all")
            
            # Draw Clock Outline
            self.clock_canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, outline="white", width=4)

            # Draw Numbers
            self.clock_canvas.create_text(cx, cy - radius + 20, text="12", fill="white", font=("Arial", 14, "bold"))
            self.clock_canvas.create_text(cx + radius - 20, cy, text="3", fill="white", font=("Arial", 14, "bold"))
            self.clock_canvas.create_text(cx, cy + radius - 20, text="6", fill="white", font=("Arial", 14, "bold"))
            self.clock_canvas.create_text(cx - radius + 20, cy, text="9", fill="white", font=("Arial", 14, "bold"))

            # Draw Hour Hand (White, thick, short)
            hx = cx + (radius * 0.5) * math.cos(math.radians(hr_angle))
            hy = cy + (radius * 0.5) * math.sin(math.radians(hr_angle))
            self.clock_canvas.create_line(cx, cy, hx, hy, fill="white", width=6, capstyle=tk.ROUND)

            # Draw Minute Hand (Yellow, medium length)
            mx = cx + (radius * 0.8) * math.cos(math.radians(min_angle))
            my = cy + (radius * 0.8) * math.sin(math.radians(min_angle))
            self.clock_canvas.create_line(cx, cy, mx, my, fill="yellow", width=4, capstyle=tk.ROUND)

            # Draw Second Hand (Red, thin, long)
            sx = cx + (radius * 0.9) * math.cos(math.radians(sec_angle))
            sy = cy + (radius * 0.9) * math.sin(math.radians(sec_angle))
            self.clock_canvas.create_line(cx, cy, sx, sy, fill="#ff0000", width=2, capstyle=tk.ROUND)

            # Draw Center Dot
            self.clock_canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#00ffff", outline="white")

            # Loop function every 1000ms (1 second)
            self.lbl_clock_container.after(1000, self.update_clock)
            
        except Exception as ex:
            pass # Silently catch errors if the window closes

class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Course Details")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        self.db = Database()

        # --- Variables ---
        self.var_cid = tk.StringVar() # Hidden ID for backend operations
        self.var_course = tk.StringVar()
        self.var_duration = tk.StringVar()
        self.var_charges = tk.StringVar()
        self.var_search = tk.StringVar()

        # --- Title ---
        tk.Label(self.root, text="Manage Course Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # --- Left Side Widgets ---
        tk.Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        tk.Label(self.root, text="Duration", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        tk.Label(self.root, text="Charges", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        tk.Label(self.root, text="Description", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)

        # Entry Fields
        tk.Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=60, width=200)
        tk.Entry(self.root, textvariable=self.var_duration, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=100, width=200)
        tk.Entry(self.root, textvariable=self.var_charges, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=140, width=200)
        self.txt_description = tk.Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_description.place(x=150, y=180, width=420, height=130)

        # --- Buttons ---
        tk.Button(self.root, text="Save", command=self.add, font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2").place(x=150, y=400, width=110, height=40)
        tk.Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2").place(x=270, y=400, width=110, height=40)
        tk.Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2").place(x=390, y=400, width=110, height=40)
        tk.Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2").place(x=510, y=400, width=110, height=40)

        # --- Right Side (Search & Table) ---
        tk.Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg="white").place(x=720, y=60)
        tk.Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=850, y=60, width=180)
        tk.Button(self.root, text="Search", command=self.search, font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2").place(x=1040, y=60, width=120, height=28)

        # Table (Treeview)
        self.C_Frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        self.C_Frame.place(x=720, y=100, width=460, height=340)

        scrolly = tk.Scrollbar(self.C_Frame, orient=tk.VERTICAL)
        scrollx = tk.Scrollbar(self.C_Frame, orient=tk.HORIZONTAL)

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("cid", "name", "duration", "charges", "description"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        
        scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="Course ID")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = "headings"
        self.CourseTable.column("cid", width=80)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)
        self.CourseTable.pack(fill=tk.BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # --- Backend Functions ---
    def clear(self):
        self.show()  # This calls the show function below to refresh the table
        self.var_cid.set("")
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0', tk.END)

    def show(self):
        try:
            self.db.cur.execute("SELECT * FROM course")
            rows = self.db.cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', tk.END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.CourseTable.focus()
        content = self.CourseTable.item(f)
        row = content['values']
        if row:
            self.var_cid.set(row[0]) # Capture the specific ID
            self.var_course.set(row[1])
            self.var_duration.set(row[2])
            self.var_charges.set(row[3])
            self.txt_description.delete('1.0', tk.END)
            self.txt_description.insert(tk.END, row[4])

    def add(self):
        course_name = self.var_course.get().strip() # Removes accidental spaces
        if course_name == "":
            messagebox.showerror("Error", "Course name is required", parent=self.root)
            return

        try:
            # Proactively check if the course already exists
            self.db.cur.execute("SELECT * FROM course WHERE name=?", (course_name,))
            row = self.db.cur.fetchone()
            if row != None:
                messagebox.showerror("Error", f"The course '{course_name}' already exists!", parent=self.root)
                return

            self.db.cur.execute("INSERT INTO course (name, duration, charges, description) VALUES(?,?,?,?)", (
                course_name, 
                self.var_duration.get(), 
                self.var_charges.get(), 
                self.txt_description.get('1.0', tk.END).strip()
            ))
            self.db.con.commit()
            messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def update(self):
        course_name = self.var_course.get().strip()
        if self.var_cid.get() == "":
            messagebox.showerror("Error", "Please select a course from the list to update", parent=self.root)
            return
            
        try:
            # Check if the NEW name already exists on a DIFFERENT course ID
            self.db.cur.execute("SELECT * FROM course WHERE name=? AND cid!=?", (course_name, int(self.var_cid.get())))
            row = self.db.cur.fetchone()
            if row != None:
                messagebox.showerror("Error", f"The course '{course_name}' already exists!", parent=self.root)
                return

            self.db.cur.execute("UPDATE course SET name=?, duration=?, charges=?, description=? WHERE cid=?", (
                course_name,
                self.var_duration.get(),
                self.var_charges.get(),
                self.txt_description.get('1.0', tk.END).strip(),
                int(self.var_cid.get()) # <--- Explicit Integer Cast
            ))
            self.db.con.commit()
            messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def delete(self):
        if self.var_cid.get() == "":
            messagebox.showerror("Error", "Please select a course from the list to delete", parent=self.root)
            return
            
        try:
            op = messagebox.askyesno("Confirm", "Do you really want to delete this course?", parent=self.root)
            if op:
                # Explicit integer cast to ensure SQLite finds the exact row
                self.db.cur.execute("DELETE FROM course WHERE cid=?", (int(self.var_cid.get()),))
                self.db.con.commit()
                messagebox.showinfo("Delete", "Course Deleted Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def search(self):
        self.db.cur.execute(f"SELECT * FROM course WHERE name LIKE '%{self.var_search.get()}%'")
        rows = self.db.cur.fetchall()
        self.CourseTable.delete(*self.CourseTable.get_children())
        for row in rows:
            self.CourseTable.insert('', tk.END, values=row)

class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Student Details")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        self.db = Database()

        # --- Variables ---
        self.var_roll = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_gender = tk.StringVar()
        self.var_dob = tk.StringVar()
        self.var_contact = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_a_date = tk.StringVar()
        self.var_state = tk.StringVar()
        self.var_city = tk.StringVar()
        self.var_pin = tk.StringVar()
        self.var_search = tk.StringVar()

        # Fetch courses from database for the dropdown
        self.course_list = []
        self.fetch_course()

        # --- Title ---
        tk.Label(self.root, text="Manage Student Details", font=("goudy old style", 20, "bold"), bg="#033054", fg="white").place(x=10, y=15, width=1180, height=35)

        # --- Left Side Widgets ---
        # Column 1
        tk.Label(self.root, text="Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        tk.Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        tk.Label(self.root, text="Email", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        tk.Label(self.root, text="Gender", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)
        tk.Label(self.root, text="State", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=220)
        tk.Label(self.root, text="Address", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=260)

        # Entries Col 1
        tk.Entry(self.root, textvariable=self.var_roll, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=60, width=200)
        tk.Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=100, width=200)
        tk.Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=140, width=200)
        
        self.cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), font=("goudy old style", 15, "bold"), state='readonly', justify=tk.CENTER)
        self.cmb_gender.place(x=150, y=180, width=200)
        self.cmb_gender.current(0)
        
        tk.Entry(self.root, textvariable=self.var_state, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=220, width=150)

        # Column 2
        tk.Label(self.root, text="D.O.B", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=60)
        tk.Label(self.root, text="Contact No.", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=100)
        tk.Label(self.root, text="Select Course", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=140)
        tk.Label(self.root, text="Admission Date", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=180)
        tk.Label(self.root, text="City", font=("goudy old style", 15, "bold"), bg="white").place(x=310, y=220)
        tk.Label(self.root, text="Pin Code", font=("goudy old style", 15, "bold"), bg="white").place(x=500, y=220)

        # Entries Col 2
        tk.Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=500, y=60, width=200)
        tk.Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=500, y=100, width=200)
        
        self.cmb_course = ttk.Combobox(self.root, textvariable=self.var_course, values=self.course_list, font=("goudy old style", 15, "bold"), state='readonly', justify=tk.CENTER)
        self.cmb_course.place(x=500, y=140, width=200)
        self.cmb_course.set("Select")
        
        tk.Entry(self.root, textvariable=self.var_a_date, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=500, y=180, width=200)
        tk.Entry(self.root, textvariable=self.var_city, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=360, y=220, width=130)
        tk.Entry(self.root, textvariable=self.var_pin, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=590, y=220, width=110)

        # Text Address
        self.txt_address = tk.Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_address.place(x=150, y=260, width=550, height=100)

        # --- Buttons ---
        tk.Button(self.root, text="Save", command=self.add, font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2").place(x=150, y=400, width=110, height=40)
        tk.Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2").place(x=270, y=400, width=110, height=40)
        tk.Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2").place(x=390, y=400, width=110, height=40)
        tk.Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2").place(x=510, y=400, width=110, height=40)

        # --- Right Side (Search & Table) ---
        tk.Label(self.root, text="Search | Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=720, y=60)
        tk.Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=880, y=60, width=150)
        tk.Button(self.root, text="Search", command=self.search, font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2").place(x=1040, y=60, width=120, height=28)

        # Table (Treeview)
        self.C_Frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        self.C_Frame.place(x=720, y=100, width=460, height=340)

        scrolly = tk.Scrollbar(self.C_Frame, orient=tk.VERTICAL)
        scrollx = tk.Scrollbar(self.C_Frame, orient=tk.HORIZONTAL)

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "pin", "address"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        
        scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        # Configure headings
        self.CourseTable.heading("roll", text="Roll No.")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("email", text="Email")
        self.CourseTable.heading("gender", text="Gender")
        self.CourseTable.heading("dob", text="D.O.B")
        self.CourseTable.heading("contact", text="Contact")
        self.CourseTable.heading("admission", text="Admission")
        self.CourseTable.heading("course", text="Course")
        self.CourseTable.heading("state", text="State")
        self.CourseTable.heading("city", text="City")
        self.CourseTable.heading("pin", text="Pin")
        self.CourseTable.heading("address", text="Address")
        self.CourseTable["show"] = "headings"
        
        # Configure columns width
        for col in ("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "pin", "address"):
            self.CourseTable.column(col, width=100)
            
        self.CourseTable.pack(fill=tk.BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # --- Backend Functions ---
    def fetch_course(self):
        try:
            self.db.cur.execute("SELECT name FROM course")
            rows = self.db.cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.course_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.show()
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_course.set("Select")
        self.var_a_date.set("")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.var_search.set("")
        self.txt_address.delete('1.0', tk.END)

    def add(self):
        roll_no = self.var_roll.get().strip()
        if roll_no == "":
            messagebox.showerror("Error", "Roll Number is required", parent=self.root)
            return

        try:
            # Check if Roll No already exists
            self.db.cur.execute("SELECT * FROM student WHERE roll=?", (roll_no,))
            row = self.db.cur.fetchone()
            if row != None:
                messagebox.showerror("Error", f"Student with Roll No. '{roll_no}' already exists!", parent=self.root)
                return

            self.db.cur.execute("INSERT INTO student (roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (
                roll_no, self.var_name.get(), self.var_email.get(), self.var_gender.get(), self.var_dob.get(),
                self.var_contact.get(), self.var_a_date.get(), self.var_course.get(), self.var_state.get(),
                self.var_city.get(), self.var_pin.get(), self.txt_address.get('1.0', tk.END).strip()
            ))
            self.db.con.commit()
            messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def show(self):
        try:
            self.db.cur.execute("SELECT * FROM student")
            rows = self.db.cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', tk.END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.CourseTable.focus()
        content = self.CourseTable.item(f)
        row = content['values']
        if row:
            self.var_roll.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_dob.set(row[4])
            self.var_contact.set(row[5])
            self.var_a_date.set(row[6])
            self.var_course.set(row[7])
            self.var_state.set(row[8])
            self.var_city.set(row[9])
            self.var_pin.set(row[10])
            self.txt_address.delete('1.0', tk.END)
            self.txt_address.insert(tk.END, row[11])

    def update(self):
        roll_no = self.var_roll.get().strip()
        if roll_no == "":
            messagebox.showerror("Error", "Please select a student from the list to update", parent=self.root)
            return
            
        try:
            # Check if the student actually exists first
            self.db.cur.execute("SELECT * FROM student WHERE roll=?", (roll_no,))
            row = self.db.cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "No student found with this Roll Number.", parent=self.root)
                return

            # Update the record (Using int(roll_no) to guarantee a match)
            self.db.cur.execute("UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, admission=?, course=?, state=?, city=?, pin=?, address=? WHERE roll=?", (
                self.var_name.get(), 
                self.var_email.get(), 
                self.var_gender.get(), 
                self.var_dob.get(),
                self.var_contact.get(), 
                self.var_a_date.get(), 
                self.var_course.get(), 
                self.var_state.get(),
                self.var_city.get(), 
                self.var_pin.get(), 
                self.txt_address.get('1.0', tk.END).strip(),
                int(roll_no) # <--- Explicit Integer Cast
            ))
            self.db.con.commit()
            messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
            self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def delete(self):
        roll_no = self.var_roll.get().strip()
        if roll_no == "":
            messagebox.showerror("Error", "Please select a student from the list to delete", parent=self.root)
            return
            
        try:
            # Check if the student exists before deleting
            self.db.cur.execute("SELECT * FROM student WHERE roll=?", (roll_no,))
            row = self.db.cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "No student found with this Roll Number.", parent=self.root)
                return

            op = messagebox.askyesno("Confirm", "Do you really want to delete this student?", parent=self.root)
            if op:
                # Explicit integer cast to ensure SQLite finds the exact row
                self.db.cur.execute("DELETE FROM student WHERE roll=?", (int(roll_no),))
                self.db.con.commit()
                messagebox.showinfo("Delete", "Student Deleted Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    def search(self):
        try:
            self.db.cur.execute(f"SELECT * FROM student WHERE roll LIKE '%{self.var_search.get()}%'")
            rows = self.db.cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', tk.END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Student Result")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        self.db = Database()

        # --- Variables ---
        self.var_roll = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_course = tk.StringVar()
        self.var_marks = tk.StringVar()
        self.var_full_marks = tk.StringVar()
        
        self.roll_list = []
        self.fetch_roll()

        # --- Title ---
        tk.Label(self.root, text="Add Student Result", font=("goudy old style", 20, "bold"), bg="orange", fg="black").place(x=10, y=15, width=1180, height=50)

        # --- Widgets ---
        # Labels
        tk.Label(self.root, text="Select Student", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=100)
        tk.Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=160)
        tk.Label(self.root, text="Course", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=220)
        tk.Label(self.root, text="Marks Obtained", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=280)
        tk.Label(self.root, text="Full Marks", font=("goudy old style", 15, "bold"), bg="white").place(x=50, y=340)

        # Entries & Dropdown
        self.cmb_student = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list, font=("goudy old style", 15, "bold"), state='readonly', justify=tk.CENTER)
        self.cmb_student.place(x=280, y=100, width=200)
        self.cmb_student.set("Select")

        self.cmb_student.bind("<<ComboboxSelected>>", self.search)

        # Name and Course are readonly because they auto-fill from the search
        tk.Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15, "bold"), bg="lightgray", state='readonly').place(x=280, y=160, width=320)
        tk.Entry(self.root, textvariable=self.var_course, font=("goudy old style", 15, "bold"), bg="lightgray", state='readonly').place(x=280, y=220, width=320)
        
        tk.Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=280, y=280, width=320)
        tk.Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=280, y=340, width=320)

        # --- Buttons ---
        tk.Button(self.root, text="Submit", command=self.add, font=("times new roman", 15, "bold"), bg="lightgreen", cursor="hand2").place(x=300, y=420, width=120, height=35)
        tk.Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15, "bold"), bg="lightgray", cursor="hand2").place(x=430, y=420, width=120, height=35)

        # --- Image - UPDATED PATH ---
        self.res_img = ImageTk.PhotoImage(file=resource_path("images/result.jpg"))
        tk.Label(self.root, image=self.res_img, bd=0).place(x=650, y=100, width=500, height=300)

    # --- Backend Functions ---
    def fetch_roll(self):
        try:
            self.db.cur.execute("SELECT roll, name FROM student")
            rows = self.db.cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    # Combines Roll No and Name (e.g., "101 - Rahul Kumar")
                    self.roll_list.append(f"{row[0]} - {row[1]}") 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self, ev=None):
        try:
            selected_val = self.var_roll.get()
            if selected_val == "Select":
                return
                
            # Splits "101 - Rahul" at the dash and grabs the first part ("101")
            roll_no = selected_val.split(" - ")[0] 

            self.db.cur.execute("SELECT name, course FROM student WHERE roll=?", (roll_no,))
            row = self.db.cur.fetchone()
            if row != None:
                self.var_name.set(row[0])
                self.var_course.set(row[1])
            else:
                messagebox.showerror("Error", "No student found", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def add(self):
        if self.var_name.get() == "":
            messagebox.showerror("Error", "Please select a student record", parent=self.root)
            return
        if self.var_marks.get() == "" or self.var_full_marks.get() == "":
            messagebox.showerror("Error", "Marks fields are required", parent=self.root)
            return

        try:
            # Extract just the roll number for the database
            roll_no = self.var_roll.get().split(" - ")[0]

            # Check if this student already has a result for this course
            self.db.cur.execute("SELECT * FROM result WHERE roll=? AND course=?", (roll_no, self.var_course.get()))
            row = self.db.cur.fetchone()
            if row != None:
                messagebox.showerror("Error", "Result already present for this student and course", parent=self.root)
                return

            # Math calculation for percentage
            marks_obt = float(self.var_marks.get())
            full_marks = float(self.var_full_marks.get())
            
            if full_marks == 0:
                messagebox.showerror("Error", "Full marks cannot be zero", parent=self.root)
                return
                
            per = (marks_obt / full_marks) * 100
            percentage = f"{round(per, 2)}%" 

            # Insert into database using the clean roll_no
            self.db.cur.execute("INSERT INTO result (roll, name, course, marks, full_marks, per) VALUES(?,?,?,?,?,?)", (
                roll_no,
                self.var_name.get(),
                self.var_course.get(),
                self.var_marks.get(),
                self.var_full_marks.get(),
                percentage
            ))
            self.db.con.commit()
            messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
            self.clear()
            
        except ValueError:
            messagebox.showerror("Error", "Marks must be valid numbers", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)
    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")


class ViewResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("View Student Results")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()
        self.db = Database()

        # --- Variables ---
        # --- Variables ---
        self.var_search = tk.StringVar()
        self.var_id = "" 
        self.roll_list = []
        self.fetch_roll()

        # --- Title ---
        tk.Label(self.root, text="View Student Results", font=("goudy old style", 20, "bold"), bg="orange", fg="black").place(x=10, y=15, width=1180, height=50)

        # --- Search Section (Upgraded to Auto-Dropdown) ---
        tk.Label(self.root, text="Search By | Roll No.", font=("goudy old style", 20, "bold"), bg="white").place(x=250, y=100)
        
        self.cmb_search = ttk.Combobox(self.root, textvariable=self.var_search, values=self.roll_list, font=("goudy old style", 20), state='readonly', justify=tk.CENTER)
        self.cmb_search.place(x=500, y=100, width=300)
        self.cmb_search.set("Select Student")
        
        # Bind the auto-search event
        self.cmb_search.bind("<<ComboboxSelected>>", self.search)

        # Only the Clear button remains
        tk.Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), bg="lightgray", cursor="hand2").place(x=820, y=100, width=100, height=38)

        # --- Result Table ---
        self.C_Frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        self.C_Frame.place(x=150, y=200, width=900, height=80) 

        self.CourseTable = ttk.Treeview(self.C_Frame, columns=("roll", "name", "course", "marks", "full_marks", "per"), show='headings')
        
        self.CourseTable.heading("roll", text="Roll No")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("course", text="Course")
        self.CourseTable.heading("marks", text="Marks Obtained")
        self.CourseTable.heading("full_marks", text="Total Marks")
        self.CourseTable.heading("per", text="Percentage")
        
        self.CourseTable.column("roll", width=100, anchor=tk.CENTER)
        self.CourseTable.column("name", width=150, anchor=tk.CENTER)
        self.CourseTable.column("course", width=150, anchor=tk.CENTER)
        self.CourseTable.column("marks", width=150, anchor=tk.CENTER)
        self.CourseTable.column("full_marks", width=150, anchor=tk.CENTER)
        self.CourseTable.column("per", width=150, anchor=tk.CENTER)

        self.CourseTable.pack(fill=tk.BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        # --- Delete Button ---
        tk.Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2").place(x=520, y=350, width=150, height=35)

    # --- Backend Functions ---
    def fetch_roll(self):
        try:
            # We use DISTINCT so if a student has 2 courses, their name only appears once in the dropdown
            self.db.cur.execute("SELECT DISTINCT roll, name FROM result")
            rows = self.db.cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    self.roll_list.append(f"{row[0]} - {row[1]}")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self, ev=None):
        selected_val = self.var_search.get()
        if selected_val == "Select Student" or selected_val == "":
            return
            
        try:
            # Split the string to grab just the Roll Number
            roll_no = selected_val.split(" - ")[0]

            self.db.cur.execute("SELECT roll, name, course, marks, full_marks, per FROM result WHERE roll=?", (roll_no,))
            rows = self.db.cur.fetchall() # Using fetchall to show all courses a student took
            
            if len(rows) > 0:
                self.CourseTable.delete(*self.CourseTable.get_children())
                for row in rows:
                    self.CourseTable.insert('', tk.END, values=row)
                self.var_id = roll_no # Store the roll number for deletion
            else:
                messagebox.showerror("Error", "No result found for this student", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_search.set("Select Student")
        self.var_id = ""
        self.CourseTable.delete(*self.CourseTable.get_children())

    def get_data(self, ev):
        f = self.CourseTable.focus()
        content = self.CourseTable.item(f)
        row = content['values']
        if row:
            self.var_id = str(row[0]) # Securely track the selected record

    def delete(self):
        if self.var_id == "":
            messagebox.showerror("Error", "Please search and select a result first", parent=self.root)
            return
            
        try:
            op = messagebox.askyesno("Confirm", "Do you really want to delete this result?", parent=self.root)
            if op:
                self.db.cur.execute("DELETE FROM result WHERE roll=?", (self.var_id,))
                self.db.con.commit()
                messagebox.showinfo("Success", "Result Deleted Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)



if __name__ == "__main__":
    root = tk.Tk()
    obj = LoginSystem(root)
    root.mainloop()