import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database
import mysql.connector

class My_GUI(tk.Tk):
    def __init__(self,host,user,password):

        self.set_host = host
        self.set_user = user
        self.set_password = password

        super(My_GUI, self).__init__()
        self.createDatabaseAndData()
        self.init_log_in()

    def createDatabaseAndData(self):

        database.database_connection(self.set_host,self.set_user,self.set_password)

        con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
        cursor = con.cursor()
        query = "select * from `mydb`.`Course`"
        cursor.execute(query)
        rows = cursor.fetchall()
        con.commit()
        con.close()
        if (rows == []):
            database.add_random_data(self.set_host,self.set_user,self.set_password)

    def init_log_in(self):
        # top level frame for explanation
        self.top_frame_label = tk.Frame(self)
        self.label = tk.Label(self.top_frame_label, text="LAMBTON College User Login", fg="#FFFFFF", width=50)
        self.label.config(font=("consolas", 30), background="#2C3E50")
        self.label.grid(row=0, column=0)
        self.top_frame_label.grid(row=0, column=0)

        # middle level for Profile
        self.mid_frame = tk.Frame(self)
        self.img = tk.PhotoImage(file="../Image/profile.png")
        self.mid_panel = tk.Label(self.mid_frame, image=self.img)
        self.mid_panel.config(borderwidth="0", highlightthickness=0)
        self.mid_panel.grid(row=0, column=0)
        self.mid_frame.grid(row=1, column=0)

        # bottom level for password and everything
        self.bottom_frame = tk.Frame(self)
        self.bottom_Selection_text = tk.Label(self.bottom_frame, text="User Type", fg="#FFFFFF")
        self.bottom_Selection_text.config(font=("consolas", 16), background="#18BC9C")

        self.userLoginSelection = tk.StringVar()
        self.bottom_Selection_combo = ttk.Combobox(self.bottom_frame, width=27, textvariable=self.userLoginSelection)
        self.bottom_Selection_combo['values'] = ("Admin", "Professor", "Student")
        self.bottom_Selection_combo.config(font=(8))

        self.usernameText = tk.Label(self.bottom_frame, text="Username", fg="#FFFFFF", width=35)
        self.usernameText.config(font=("consolas", 16), background="#18BC9C")
        self.username = tk.Entry(self.bottom_frame, width=29)
        self.username.config(font=(8))

        self.myPasswordText = tk.Label(self.bottom_frame, text="Password", fg="#FFFFFF", width=35)
        self.myPasswordText.config(font=("consolas", 16), background="#18BC9C")
        self.myPassword = tk.Entry(self.bottom_frame, width=29, show="*")
        self.myPassword.config(font=(8))

        self.bottom_Selection_text.grid(row=0, column=0)
        self.bottom_Selection_combo.grid(row=0, column=1)

        self.usernameText.grid(row=1, column=0)
        self.username.grid(row=1, column=1)

        self.myPasswordText.grid(row=2, column=0)
        self.myPassword.grid(row=2, column=1)

        self.login_button = tk.Button(self.bottom_frame, text="Log in", fg="#FFFFFF", command=self.action)
        self.login_button.config(font=("consolas", 15), background="#2C3E50")
        self.login_button.grid(row=3, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))

        self.bottom_frame.config(background="#18BC9C")
        self.bottom_frame.grid(row=2, column=0)

        # menu option
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label="Exit", command=self.destroy)

        # Main window config and settings
        self.config(background="#18BC9C")
        self.config(menu=self.filemenu)
        self.geometry("1050x700+0+0")
        self.resizable(0,0)
        self.title("User Login")
        self.mainloop()

    def action(self):
        text = ""
        if (self.userLoginSelection.get() == "Admin"):
            self.selection = 1
            text = "Admin"
        elif (self.userLoginSelection.get() == "Professor"):
            self.selection = 2
            text = "Professor"
        elif (self.userLoginSelection.get() == "Student"):
            self.selection = 3
            text = "Student"


            
        if (text != ""):
            data = database.PasswordData(text,self.set_host,self.set_user,self.set_password)
            password = self.myPassword.get()
            username = self.username.get()
            if (data.user_exists(username)):
                if (data.username_matches_password(username,password)):
                    self.enteredUser = self.username.get()
                    self.destroy()
                    self.info_login()
                else:
                    errortext= "Password is wrong"
                    messagebox.showerror(title="Error", message=errortext)

            else:
                errortext = "There is no such a user name for {}".format(text)
                messagebox.showerror(title="Error",message = errortext)
        else:
            messagebox.showinfo(title="Warning",message = "Please select user type :)")

    def info_login(self):
        if(self.selection == 1):
            admin_window = AdminWindow(self.set_host,self.set_user,self.set_password)
        elif(self.selection == 2):
            professor_window = ProfessorWindow(self.enteredUser,self.set_host,self.set_user,self.set_password)
        elif (self.selection == 3):
            student_window = StudentWindow(self.enteredUser,self.set_host,self.set_user,self.set_password)

class AdminWindow:

    def __init__(self,host,user,password):

        self.set_host = host
        self.set_user = user
        self.set_password = password

        self.init_ui()


    def init_ui(self):
        self.window = tk.Tk()

        self.main_label = tk.Label(self.window, text="Welcome Admin to Management System",fg="#FFFFFF", width=50)
        self.main_label.config(font=("consolas", 30), background="#18BC9C")
        self.main_label.pack()

        self.top_frame = tk.Frame(self.window,bg = "#2C3E50")
        self.top_frame.place(x=10,y=100,width=1030, height=560)

        self.frameLabel = tk.Label(self.top_frame, text = "Now You can UPDATE the database please select by clicking options below to make any changes")
        self.frameLabel.config(font=("consolas",15),background = "#2C3E50",fg = "#FFFFFF")
        self.frameLabel.pack(side="top")

        self.mid_frame = tk.Frame(self.window, bg = "#18BC9C")
        self.mid_frame.place(x=270,y=200,width=500,height = 300)

        self.student = tk.Button(self.mid_frame, text="Student Information",bg = "#18BC9C", fg = "#FFFFFF",command = self.studentTable)
        self.student.config(width=34,height=5)
        self.student.grid(row=0,column=0)

        self.usernameAndPassword = tk.Button(self.mid_frame, text= "Username and Password Information",bg = "#18BC9C", fg = "#FFFFFF",command = self.usernameAndPasswordTable)
        self.usernameAndPassword.config(width=35,height=5)
        self.usernameAndPassword.grid(row=0, column=1)



        self.course = tk.Button(self.mid_frame, text="Course Information", bg="#18BC9C", fg="#FFFFFF",command = self.courseTable)
        self.course.config(width=34, height=5)
        self.course.grid(row=1, column=0)

        self.professor = tk.Button(self.mid_frame, text="Professor Information", bg="#18BC9C", fg="#FFFFFF",command = self.professorTable)
        self.professor.config(width=35, height=5)
        self.professor.grid(row=1, column=1)

        self.grade = tk.Button(self.mid_frame, text="Student Grade Information", bg="#18BC9C", fg="#FFFFFF", command = self.gradeTable)
        self.grade.config(width=70, height=8)
        self.grade.grid(row=2, column=0,columnspan =2)


        #main window config
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.filemenu.add_command(label="Logout", command=self.adminAction)
        self.window.config(background="#18BC9C")
        self.window.config(menu=self.filemenu)
        self.window.geometry("1050x700+0+0")
        self.window.resizable(0, 0)
        self.window.title("Admin Page")

        self.window.mainloop()

    def adminAction(self):
        self.window.destroy()
        returnIt = My_GUI(self.set_host,self.set_user,self.set_password)

    def studentTable(self):
        self.window.destroy()
        go_student_table = admin_student(self.set_host,self.set_user,self.set_password)

    def professorTable(self):
        self.window.destroy()
        go_professor_table = admin_professor(self.set_host,self.set_user,self.set_password)

    def gradeTable(self):
        self.window.destroy()
        go_grade_table = admin_grade(self.set_host,self.set_user,self.set_password)

    def usernameAndPasswordTable(self):
        self.window.destroy()
        go_usenameAndPasswordTable = admin_username_password(self.set_host,self.set_user,self.set_password)

    def courseTable(self):
        self.window.destroy()
        go_courseTable = admin_course(self.set_host,self.set_user,self.set_password)

class admin_student:

    def __init__(self,host,user,password):
        self.set_host = host
        self.set_user = user
        self.set_password = password


        self.window = tk.Tk()
        self.window.title("Admin Student Database")
        self.window.geometry("1530x1080+0+0")
        self.window.resizable(0, 0)

        title = tk.Label(self.window,text = "Admin >> Update Student Information", font = ("consolas",35,"bold")
                         ,background="#2C3E50",fg = "#fefefe",relief = "groove")
        title.pack(side = "top", fill = "x")

        #SET OF data============================================================================================
        self.instructionframe = tk.Frame(self.window,bd=4, relief = "ridge", background = "#2C3E50")
        self.instructionframe.place(x = 20, y=80, width = 500, height = 700)

        self.ins_title = tk.Label(self.instructionframe, text = "Update Student",font = ("consolas",25,"bold"),fg = "#fefefe"
                                  ,background="#2C3E50" )
        self.ins_title.grid(row = 0,columnspan = 2,pady = 20,padx=20,sticky = "w" )

        #>>>>Student ID
        self.student_id = tk.Label(self.instructionframe, text = "Student ID ",font = ("consolas",14,"bold"),fg = "#fefefe"
                                  ,background="#2C3E50" )
        self.student_id.grid(row = 1, column =0,pady = 10,padx=20,sticky = "w")
        
        self.student_id_text = tk.StringVar()
        self.student_id_entry = tk.Entry(self.instructionframe,font = ("consolas",14,"bold"),bd=4,relief = "ridge"
                                        ,textvariable = self.student_id_text)
        self.student_id_entry.grid(row = 1, column =1,pady = 10,padx=20,sticky = "w")

        # >>>>Student First Name

        self.student_firstName = tk.Label(self.instructionframe, text="Student First Name ", font=("consolas", 14, "bold"),
                                   fg="#fefefe"
                                   , background="#2C3E50")
        self.student_firstName.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        
        self.student_firstName_text = tk.StringVar()
        self.student_firstName_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4, relief="ridge",
                                             textvariable = self.student_firstName_text)
        self.student_firstName_entry.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # >>>>Student Second Name

        self.student_lastName = tk.Label(self.instructionframe, text="Student Last Name ",
                                          font=("consolas", 14, "bold"),
                                          fg="#fefefe"
                                          , background="#2C3E50")
        self.student_lastName.grid(row=3, column=0, pady=10, padx=20, sticky="w")
        
        
        self.student_lastName_text = tk.StringVar()
        self.student_lastName_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                                relief="ridge", textvariable = self.student_lastName_text)
        self.student_lastName_entry.grid(row=3, column=1, pady=10, padx=20, sticky="w")

        # >>>>Student Email

        self.student_email = tk.Label(self.instructionframe, text="Student Email ",
                                         font=("consolas", 14, "bold"),
                                         fg="#fefefe"
                                         , background="#2C3E50")
        self.student_email.grid(row=4, column=0, pady=10, padx=20, sticky="w")
        
        
        self.student_email_text = tk.StringVar()
        self.student_email_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                               relief="ridge",textvariable = self.student_email_text)
        self.student_email_entry.grid(row=4, column=1, pady=10, padx=20, sticky="w")

        # >>>>Student Program
        self.student_program = tk.Label(self.instructionframe, text="Student Program ",
                                      font=("consolas", 14, "bold"),
                                      fg="#fefefe"
                                      , background="#2C3E50")
        self.student_program.grid(row=5, column=0, pady=10, padx=20, sticky="w")
        
        self.student_program_text = tk.StringVar()
        self.student_program_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                            relief="ridge", textvariable = self.student_program_text)
        self.student_program_entry.grid(row=5, column=1, pady=10, padx=20, sticky="w")

        # >>>>Student Date of Join
        self.student_dateofJoin = tk.Label(self.instructionframe, text="Student Join Date ",
                                        font=("consolas", 14, "bold"),
                                        fg="#fefefe"
                                        , background="#2C3E50")
        self.student_dateofJoin.grid(row=6, column=0, pady=10, padx=20, sticky="w")
        
        
        self.student_dateofJoin_text = tk.StringVar()
        self.student_dateofJoin_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                              relief="ridge", textvariable = self.student_dateofJoin_text)
        self.student_dateofJoin_entry.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        # >>>>Student Term
        self.student_Term = tk.Label(self.instructionframe, text="Student Term ",
                                           font=("consolas", 14, "bold"),
                                           fg="#fefefe"
                                           , background="#2C3E50")
        self.student_Term.grid(row=7, column=0, pady=10, padx=20, sticky="w")
        
        self.student_Term_text = tk.StringVar()
        self.student_Term_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                                 relief="ridge", textvariable = self.student_Term_text)
        self.student_Term_entry.grid(row=7, column=1, pady=10, padx=20, sticky="w")

        # >>>>Student GPA

        self.student_GPA = tk.Label(self.instructionframe, text="Student GPA ",
                                     font=("consolas", 14, "bold"),
                                     fg="#fefefe"
                                     , background="#2C3E50")
        self.student_GPA.grid(row=8, column=0, pady=10, padx=20, sticky="w")
        
        self.student_GPA_text = tk.StringVar()
        self.student_GPA_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                           relief="ridge",textvariable = self.student_GPA_text)
        self.student_GPA_entry.grid(row=8, column=1, pady=10, padx=20, sticky="w")

        # SET OF INSTRUCTION============================================================================================
        self.commandFrame = tk.Frame(self.window,bd=4, relief = "ridge", background = "#2C3E50")
        self.commandFrame.place(x=20,y=630,width = 500,height = 150)

        # >>>>add
        self.add_btn = tk.Button(self.commandFrame,text="Add", font = ("consolas",15,"bold"), fg="#2C3E50", background="#fefefe",
                                 relief = "groove",width = 8,command = self.add_item)
        self.add_btn.grid(row=0, column = 0,pady=10, padx=10, sticky="w")

        # >>>>delete
        self.delete_btn = tk.Button(self.commandFrame, text="Delete", font=("consolas", 15, "bold"), fg="#2C3E50",
                                 background="#fefefe",
                                 relief="groove", width=8, command = self.delete_data)
        self.delete_btn.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # >>>>update
        self.update_btn = tk.Button(self.commandFrame, text="Update", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8,command = self.update_item)
        self.update_btn.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        # >>>>clear
        self.clear_btn = tk.Button(self.commandFrame, text="Clear", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8,command = self.clearfix)
        self.clear_btn.grid(row=0, column=3, pady=10, padx=10, sticky="w")
        
        
        # >>>>> autocomplete
        self.auto_complete_button = tk.Button(self.commandFrame, text="Auto Complete", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=14,command = self.complete_data)
        self.auto_complete_button.grid(row=1, columnspan=2, pady=10, padx=10, sticky="w")
                                   
        
        
        
        # SET OF RESULT================================================================================================

        self.detailFrame = tk.Frame(self.window,bd = 4, relief = "ridge", background = "#2C3E50")
        self.detailFrame.place(x = 540,y = 80, width = 960,height = 700)

        # >>>>search

        self.search = tk.Label(self.detailFrame, text="Search By ",
                                      font=("consolas", 20, "bold"),
                                      fg="#fefefe"
                                      , background="#2C3E50")
        self.search.grid (row = 0,column=0,pady = 20,padx=10,sticky = "w" )
        self.search_selection = tk.StringVar()

        self.search_by = ttk.Combobox(self.detailFrame, font=("consolas", 16, "bold"), textvariable=self.search_selection)

        self.search_by['values'] = ("Student_Number", "StudentFirstName", "StudentLastName", "StudentEmail", "StudentProgram", "StudentDateofJoin",
                                    "StudentTerm", "StudentGPA")
        self.search_by.grid(row = 0,column=1,pady = 20,padx=10,sticky = "w")

        # >>>>search text
        self.searchText = tk.Entry (self.detailFrame,font=("consolas", 14, "bold"), bd=4,
                                           relief="ridge")
        self.searchText.grid(row = 0,column=2,pady = 20,padx=10,sticky = "w")
        # >>>>search button

        self.searchbtn = tk.Button(self.detailFrame, text="Search", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="raised", width=8, command =self.searchIT)

        self.searchbtn.grid(row = 0,column=3,pady = 20,padx=10,sticky = "w")
        # >>>>search all button

        self.searchAllbtn = tk.Button(self.detailFrame, text="Search All", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="raised", width=10, command = self.search_all)

        self.searchAllbtn.grid(row=0, column=4, pady=20, padx=10, sticky="w")


        # SET OF Database Table ============================================================================================
        self.dataFrame = tk.Frame(self.window,bd = 4,relief = "ridge",bg = "#fefefe")
        self.dataFrame.place(x = 560, y=180, width = 920, height = 580)

        #Student Table from database
        self.scrollx = tk.Scrollbar(self.dataFrame,orient = "horizontal")
        self.scrolly = tk.Scrollbar(self.dataFrame, orient="vertical")

        self.student_table = ttk.Treeview(self.dataFrame,columns = ("Student_Number", "StudentFirstName", "StudentLastName", "StudentEmail", "StudentProgram", "StudentDateofJoin",
                                    "StudentTerm", "StudentGPA"),
                                    xscrollcommand = self.scrollx.set,
                                    yscrollcommand = self.scrolly.set)
        self.scrollx.pack(side = "bottom",fill = "x")
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.config(command =self.student_table.xview)
        self.scrolly.config(command=self.student_table.yview)
        self.student_table.heading("Student_Number",text = "Student_ID")
        self.student_table.heading("StudentFirstName", text="StudentFirstName")
        self.student_table.heading("StudentLastName", text="StudentLastName")
        self.student_table.heading("StudentEmail", text="StudentEmail")
        self.student_table.heading("StudentProgram", text="StudentProgram")
        self.student_table.heading("StudentDateofJoin", text="StudentDateofJoin")
        self.student_table.heading("StudentTerm", text="StudentTerm")
        self.student_table.heading("StudentGPA", text="StudentGPA")
        self.student_table['show'] = 'headings'

        self.student_table.column("Student_Number",width = 120)
        self.student_table.column("StudentFirstName", width=120)
        self.student_table.column("StudentLastName", width=120)
        self.student_table.column("StudentEmail", width=140)
        self.student_table.column("StudentProgram", width=120)
        self.student_table.column("StudentDateofJoin", width=120)
        self.student_table.column("StudentTerm", width=120)
        self.student_table.column("StudentGPA", width=120)


        self.student_table.pack(fill="both",expand = 1)
        #==============================================================================================================

        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.filemenu.add_command(label="Return", command=self.adminStudentAction)
        self.window.config(menu=self.filemenu)
        

        self.window.mainloop()

    def add_item(self):
        flag = self.checker_add_item()
        student_id = self.student_id_entry.get()
        student_name = self.student_firstName_entry.get()
        student_surname = self.student_lastName_entry.get()
        student_email = self.student_email_entry.get()
        student_program = self.student_program_entry.get()
        student_join_date = self.student_dateofJoin_entry.get()
        student_term = self.student_Term_entry.get()
        student_gpa = self.student_GPA_entry.get()

        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            query = """INSERT INTO `mydb`.`Student`(Student_Number, StudentFirstName, StudentLastName, StudentEmail, StudentProgram, StudentDateofJoin, StudentTerm, StudentGPA)
                        VALUES (%s, %s,%s, %s,%s, %s,%s,%s)
            """
            val = (student_id,student_name,student_surname,student_email,student_program,student_join_date,student_term,student_gpa)
            cursor = con.cursor()
            cursor.execute(query,val)
            con.commit()
            con.close()
            messagebox.showinfo("Information","Successfully added")
            self.search_all()

    def checker_add_item(self):
        reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        self.IDlist = reach.get_student_id_list()
        flag = True
        val = self.student_id_entry.get()
        for i in self.IDlist:
            if (i[0] == val):
                flag = False
                messagebox.showerror("Error", "Student ID already in the system")
        student_id = self.student_id_entry.get()
        student_name = self.student_firstName_entry.get()
        student_surname = self.student_lastName_entry.get()
        student_email = self.student_email_entry.get()
        student_program = self.student_program_entry.get()
        student_join_date = self.student_dateofJoin_entry.get()
        student_term = self.student_Term_entry.get()
        student_gpa = self.student_GPA_entry.get()
        if (flag):
            try:
                student_term = float(student_term)
            except:
                messagebox.showerror("Error", "Student term should be float or int")

            try:
                student_gpa = float(student_gpa)
            except:
                messagebox.showerror("Error", "Student gpa should be float or int")

        if (student_id == "" and flag):
            messagebox.showerror("Error", "Student_ID cannot be empty")
            flag = False
        elif (student_name == "" and flag):
            messagebox.showerror("Error", "Student Name cannot be empty")
            flag = False
        elif (student_email == "" and flag):
            messagebox.showerror("Error", "Student Email cannot be empty")
            flag = False
        elif (student_program == "" and flag):
            messagebox.showerror("Error", "Student Program cannot be emty")
            flag = False
        elif (student_join_date == "" and flag):
            messagebox.showerror("Error", "Student Program cannot be emty")
            flag = False
        elif (student_term == "" and flag):
            messagebox.showerror("Error", "Student Term cannot be emty")
            flag = False

        num = 0
        for i in student_join_date:
            try:
                i = int(i)
                num += i
            except:
                pass
        if (flag):
            if (num == 0):
                messagebox.showerror("Error", "Are you sure it is date?")
                flag = False

        if (flag):
            if (student_gpa > 0 and student_term == 1):
                messagebox.showerror("Error", "Student gpa cannot be greater than zero because it is in first term!!")
                flag = False
            if (student_gpa > 4 or student_term > 4):
                messagebox.showerror("Error", "Student gpa or term cannot be greater than four")

        return flag

    def checker_update_item(self):
        reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        self.IDlist = reach.get_student_id_list()
        flag = True
        val = self.student_id_entry.get()
        for i in self.IDlist:
            if (i[0] == val):
                flag = True
        student_id = self.student_id_entry.get()
        student_name = self.student_firstName_entry.get()
        student_surname = self.student_lastName_entry.get()
        student_email = self.student_email_entry.get()
        student_program = self.student_program_entry.get()
        student_join_date = self.student_dateofJoin_entry.get()
        student_term = self.student_Term_entry.get()
        student_gpa = self.student_GPA_entry.get()
        if (flag):
            try:
                student_term = float(student_term)
            except:
                messagebox.showerror("Error", "Student term should be float or int")

            try:
                student_gpa = float(student_gpa)
            except:
                messagebox.showerror("Error", "Student gpa should be float or int")

        if (student_id == "" and flag):
            messagebox.showerror("Error", "Student_ID cannot be empty")
            flag = False
        elif (student_name == "" and flag):
            messagebox.showerror("Error", "Student Name cannot be empty")
            flag = False
        elif (student_email == "" and flag):
            messagebox.showerror("Error", "Student Email cannot be empty")
            flag = False
        elif (student_program == "" and flag):
            messagebox.showerror("Error", "Student Program cannot be emty")
            flag = False
        elif (student_join_date == "" and flag):
            messagebox.showerror("Error", "Student Program cannot be emty")
            flag = False
        elif (student_term == "" and flag):
            messagebox.showerror("Error", "Student Term cannot be emty")
            flag = False

        num = 0
        for i in student_join_date:
            try:
                i = int(i)
                num += i
            except:
                pass
        if (flag):
            if (num == 0):
                messagebox.showerror("Error", "Are you sure it is date?")
                flag = False

        if (flag):
            if (student_gpa > 0 and student_term == 1):
                messagebox.showerror("Error", "Student gpa cannot be greater than zero because it is in first term!!")
                flag = False
            if (student_gpa > 4 or student_term > 4):
                messagebox.showerror("Error", "Student gpa or term cannot be greater than four")

        return flag

    def clearfix(self):
        self.student_id_entry.delete(0,'end')
        self.student_firstName_entry.delete(0,'end')
        self.student_lastName_entry.delete(0,'end')
        self.student_email_entry.delete(0,'end')
        self.student_program_entry.delete(0,'end')
        self.student_dateofJoin_entry.delete(0,'end')
        self.student_GPA_entry.delete(0,'end')
        self.student_Term_entry.delete(0,'end')
        self.student_id_entry.focus_set()

    def update_item(self):
        flag = False

        student_id = self.student_id_entry.get()
        student_name = self.student_firstName_entry.get()
        student_surname = self.student_lastName_entry.get()
        student_email = self.student_email_entry.get()
        student_program = self.student_program_entry.get()
        student_join_date = self.student_dateofJoin_entry.get()
        student_term = self.student_Term_entry.get()
        student_gpa = self.student_GPA_entry.get()

        student_id = self.student_id_entry.get()
        reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        id_list = []
        for id in reach.get_student_id_list():
            id_list.append(id[0])
        self.data_student_id_list = id_list

        if (student_id in self.data_student_id_list):
            flag = True
        else:
            messagebox.showerror("ERROR", "YOU cannot update this id is not in the system")


        if(flag):
            if (int(student_term)==1) and (int(student_gpa) !=0):
                flag = False
                messagebox.showerror("ERROR","You cannot put GPA Score if the student term1")



        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
            UPDATE `mydb`.`Student` SET 
            
            StudentFirstName = %s, 
            StudentLastName = %s, 
            StudentEmail = %s, 
            StudentProgram = %s, 
            StudentDateofJoin = %s, 
            StudentTerm = %s, 
            StudentGPA = %s 
            
            WHERE Student_Number = %s
            """
            val = (student_name,student_surname,student_email,student_program,student_join_date,student_term,student_gpa,student_id)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Update","Informations are updated")
            self.search_all()

    def complete_data(self):
        student_id = self.student_id_entry.get()
        flag = True
        if (student_id == ""):
            messagebox.showerror("ERROR", "Please enter student id for AUTO COMPLETE")
            flag = False
        
        reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        student_data = reach.get_student_id_list()
        
        self.data_student_id_list = []
        for i in student_data:
            self.data_student_id_list.append(i[0])
        
        if (student_id in self.data_student_id_list):
            pass
        else:
            if(flag):
                messagebox.showerror("ERROR","Username is not in system cannot make auto complete")
        for student in student_data:
            
            if (student[0] == student_id):
                self.student_firstName_text.set(student[1])
                self.student_lastName_text.set(student[2])
                self.student_email_text.set(student[3])
                self.student_program_text.set(student[4])
                self.student_dateofJoin_text.set(student[5])
                self.student_Term_text.set(student[6])
                self.student_GPA_text.set(student[7])

    def delete_data(self):
        student_id = self.student_id_entry.get()
        reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        id_list = []
        for id in reach.get_student_id_list():
            id_list.append(id[0])
        self.data_student_id_list = id_list
        flag = False

        if (student_id in self.data_student_id_list):
            self.complete_data()
            flag = True
        else:
            messagebox.showerror("ERROR","This id is not in the system")

        student_id = self.student_id_entry.get()

        databaseConnect = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        result = databaseConnect.grade_table_column_list("Student_Number")


        if (student_id in result and flag):
            flag = False
            messagebox.showerror("Error",
                                 "You cannot delete, it is associated with grade table. This is Foreign Key Restriction")
        else:
            flag = True

        if flag:
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
            DELETE FROM `mydb`.`Student`
            WHERE Student_Number = %s
            """
            val = (self.student_id_entry.get(),)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Deleted","Information is deleted")
            self.search_all()
            self.clearfix()

    def search_all(self):

        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        studentData = dataCon.get_student_id_list()

        self.student_table.delete(*self.student_table.get_children())

        for data in studentData:
            self.student_table.insert('','end',values =(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))

    def searchIT(self):
        self.student_table.delete(*self.student_table.get_children())
        flag = False
        if (self.search_selection.get() != "" and self.searchText.get() == ""):
            messagebox.showerror("ERROR","Search text cannot be empty")
        else:
            flag = True

        if (flag):
            if (self.search_selection.get() == "Student_Number"):

                student_id = self.searchText.get()
                reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
                data = reach.get_student_id_list()

                id_list = []
                for id in data:
                    id_list.append(id[0])


                if (student_id in id_list):
                    for id in data:
                        if(id[0] == student_id):
                            self.student_table.insert('', 'end', values=(
                                id[0],id[1],id[2],id[3],id[4],id[5],id[6],id[7]))
                else:
                    messagebox.showerror("ERROR", "Not Recorded In the System")

            elif (self.search_selection.get() == "StudentFirstName"):

                student_info = self.searchText.get()
                reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
                data = reach.get_student_id_list()

                ex_list = []
                for id in data:
                    ex_list.append(id[1])


                if (student_info in ex_list):
                    for i in data:
                        if(i[1] == student_info):
                            self.student_table.insert('', 'end', values=(
                                i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7]))
                else:
                    messagebox.showerror("ERROR", "Not Recorded In the System")


            elif (self.search_selection.get() == "StudentLastName"):

                student_info = self.searchText.get()
                reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
                data = reach.get_student_id_list()

                ex_list = []
                for id in data:
                    ex_list.append(id[2])

                if (student_info in ex_list):
                    for i in data:
                        if (i[2] == student_info):
                            self.student_table.insert('', 'end', values=(
                                i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                else:
                    messagebox.showerror("ERROR", "Not Recorded In the System")

            elif (self.search_selection.get() == "StudentEmail"):

                student_info = self.searchText.get()
                reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
                data = reach.get_student_id_list()

                ex_list = []
                for id in data:
                    ex_list.append(id[3])

                if (student_info in ex_list):
                    for i in data:
                        if (i[3] == student_info):
                            self.student_table.insert('', 'end', values=(
                                i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                else:
                    messagebox.showerror("ERROR", "Not Recorded In the System")

            elif (self.search_selection.get() == "StudentProgram"):

                student_info = self.searchText.get()
                reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
                data = reach.get_student_id_list()

                ex_list = []
                for id in data:
                    ex_list.append(id[4])

                if (student_info in ex_list):
                    for i in data:
                        if (i[4] == student_info):
                            self.student_table.insert('', 'end', values=(
                                i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                else:
                    messagebox.showerror("ERROR", "Not Recorded In the System")


            elif (self.search_selection.get() == "StudentDateofJoin"):

                student_info = self.searchText.get()
                reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
                data = reach.get_student_id_list()

                ex_list = []
                for id in data:
                    ex_list.append(id[5])

                if (student_info in ex_list):
                    for i in data:
                        if (i[5] == student_info):
                            self.student_table.insert('', 'end', values=(
                                i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                else:
                    messagebox.showerror("ERROR", "Not Recorded In the System")

            elif (self.search_selection.get() == "StudentTerm"):
                try:
                    student_info = int(self.searchText.get())
                except:
                    messagebox.showerror("ERROR","Please enter digit")
                reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
                data = reach.get_student_id_list()

                ex_list = []
                for id in data:
                    ex_list.append(id[6])

                if (student_info in ex_list):
                    for i in data:
                        if (i[6] == student_info):
                            self.student_table.insert('', 'end', values=(
                                i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                else:
                    messagebox.showerror("ERROR", "Not Recorded In the System")

            elif (self.search_selection.get() == "StudentGPA"):
                try:
                    student_info = float(self.searchText.get())
                except:
                    messagebox.showerror("ERROR", "Please enter digit")
                reach = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
                data = reach.get_student_id_list()

                if (student_info < 0 or student_info >4):
                    messagebox.showerror("ERROR", "please enter anythin b/w 0 and 4")
                else:
                    for i in data:
                        if (i[7] >= student_info):
                            self.student_table.insert('', 'end', values=(
                             i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))



    def adminStudentAction(self):
        self.window.destroy()
        go_admin = AdminWindow(self.set_host,self.set_user,self.set_password)

class admin_grade:

    def __init__(self,host,user,password):
        self.set_host = host
        self.set_user = user
        self.set_password = password

        self.window = tk.Tk()
        self.window.title("Admin Student Grade Database")
        self.window.geometry("1530x1080+0+0")
        self.window.resizable(0, 0)

        title = tk.Label(self.window, text="Admin >> Update Student Grade Data", font=("consolas", 35, "bold")
                         , background="#FADF39", fg="#fefefe", relief="groove")
        title.pack(side="top", fill="x")

        # SET OF data============================================================================================
        self.instructionframe = tk.Frame(self.window, bd=4, relief="ridge", background="#FADF39")
        self.instructionframe.place(x=20, y=80, width=500, height=700)

        self.ins_title = tk.Label(self.instructionframe, text="Update Student Grade", font=("consolas", 25, "bold"),
                                  fg="#fefefe"
                                  , background="#FADF39")
        self.ins_title.grid(row=0, columnspan=2, pady=20, padx=20, sticky="w")

        # >>>>Student ID
        self.student_id = tk.Label(self.instructionframe, text="Student ID ", font=("consolas", 14, "bold"),
                                   fg="#fefefe"
                                   , background="#FADF39")
        self.student_id.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.student_id_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4, relief="ridge")
        self.student_id_entry.grid(row=1, column=1, pady=10, padx=20, sticky="w")


        # >>>>course ID

        self.course_ID = tk.Label(self.instructionframe, text="Course ID ",
                                      font=("consolas", 14, "bold"),
                                      fg="#fefefe"
                                      , background="#FADF39")
        self.course_ID.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.course_ID_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                            relief="ridge")
        self.course_ID_entry.grid(row=2, column=1, pady=10, padx=20, sticky="w")
        
        
        # >>>>Professor ID

        self.professor_ID = tk.Label(self.instructionframe, text="Professor ID ",
                                          font=("consolas", 14, "bold"),
                                          fg="#fefefe"
                                          , background="#FADF39")
        self.professor_ID.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        self.professor_ID_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                                relief="ridge")
        self.professor_ID_entry.grid(row=3, column=1, pady=10, padx=20, sticky="w")
        
        

        # >>>>grade

        self.student_grade = tk.Label(self.instructionframe, text="Student Grade ",
                                      font=("consolas", 14, "bold"),
                                      fg="#fefefe"
                                      , background="#FADF39")
        self.student_grade.grid(row=4, column=0, pady=10, padx=20, sticky="w")

        self.student_grade_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                            relief="ridge")
        self.student_grade_entry.grid(row=4, column=1, pady=10, padx=20, sticky="w")

        # SET OF INSTRUCTION============================================================================================
        self.commandFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#FADF39")
        self.commandFrame.place(x=20, y=630, width=500, height=150)

        # >>>>add
        self.add_btn = tk.Button(self.commandFrame, text="Add", font=("consolas", 15, "bold"), fg="#2C3E50",
                                 background="#fefefe",
                                 relief="groove", width=8,command = self.add_item)
        self.add_btn.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # >>>>delete
        self.delete_btn = tk.Button(self.commandFrame, text="Delete", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command = self.delete_data)
        self.delete_btn.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # >>>>update
        self.update_btn = tk.Button(self.commandFrame, text="Update", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command = self.update_item)
        self.update_btn.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        # >>>>clear
        self.clear_btn = tk.Button(self.commandFrame, text="Clear", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="groove", width=8, command = self.clearfix)
        self.clear_btn.grid(row=0, column=3, pady=10, padx=10, sticky="w")
        
       

        # SET OF RESULT================================================================================================

        self.detailFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#FADF39")
        self.detailFrame.place(x=540, y=80, width=960, height=700)

        # >>>>search

        self.search = tk.Label(self.detailFrame, text="Search By ",
                               font=("consolas", 20, "bold"),
                               fg="#fefefe"
                               , background="#FADF39")
        self.search.grid(row=0, column=0, pady=20, padx=10, sticky="w")
        self.searchSelection = tk.StringVar()

        self.search_by = ttk.Combobox(self.detailFrame, font=("consolas", 16, "bold"),
                                      textvariable = self.searchSelection)

        self.search_by['values'] = (
        'Student_Number', 'Course_ID','Professor_Professor_ID', 'grade')
        
        self.search_by.grid(row=0, column=1, pady=20, padx=10, sticky="w")

        # >>>>search text
        self.searchText_set = tk.StringVar()
        self.searchText = tk.Entry(self.detailFrame, font=("consolas", 14, "bold"), bd=4,
                                   relief="ridge",textvariable = self.searchText_set)
        self.searchText.grid(row=0, column=2, pady=20, padx=10, sticky="w")
        # >>>>search button

        self.searchbtn = tk.Button(self.detailFrame, text="Search", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="raised", width=8, command = self.searchIT)

        self.searchbtn.grid(row=0, column=3, pady=20, padx=10, sticky="w")
        # >>>>search all button

        self.searchAllbtn = tk.Button(self.detailFrame, text="Search All", font=("consolas", 15, "bold"), fg="#2C3E50",
                                      background="#fefefe",
                                      relief="raised", width=10, command = self.search_all)

        self.searchAllbtn.grid(row=0, column=4, pady=20, padx=10, sticky="w")

        # SET OF Database Table ============================================================================================
        self.dataFrame = tk.Frame(self.window, bd=4, relief="ridge", bg="#fefefe")
        self.dataFrame.place(x=560, y=180, width=920, height=580)

        # Student Table from database
        self.scrollx = tk.Scrollbar(self.dataFrame, orient="horizontal")
        self.scrolly = tk.Scrollbar(self.dataFrame, orient="vertical")

        self.student_grade_table = ttk.Treeview(self.dataFrame, columns=(
        'Student_Number','Course_ID',"Professor_ID",'grade'),
                                          xscrollcommand=self.scrollx.set,
                                          yscrollcommand=self.scrolly.set)
        self.scrollx.pack(side="bottom", fill="x")
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.config(command=self.student_grade_table.xview)
        self.scrolly.config(command=self.student_grade_table.yview)
        self.student_grade_table.heading("Student_Number", text="Student_ID")
        self.student_grade_table.heading('Course_ID', text='Course_ID')
        self.student_grade_table.heading("Professor_ID", text="Professor_ID")
        self.student_grade_table.heading('grade', text='Student_Grade')

        self.student_grade_table['show'] = 'headings'

        self.student_grade_table.column("Student_Number", width=120)
        self.student_grade_table.column('Course_ID', width=120)
        self.student_grade_table.column("Professor_ID", width=120)
        self.student_grade_table.column('grade', width=120)


        self.student_grade_table.pack(fill="both", expand=1)
        # ==============================================================================================================
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.filemenu.add_command(label="Return", command=self.adminGradeAction)
        self.window.config(menu=self.filemenu)
 
        self.window.mainloop()
    
    def search_all(self):
        
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        gradeData = dataCon.grade_table()

        self.student_grade_table.delete(*self.student_grade_table.get_children())

        for data in gradeData:
            self.student_grade_table.insert('','end',values =(data[0],data[1],data[2],data[3]))

    def searchIT(self):
        
        self.student_grade_table.delete(*self.student_grade_table.get_children())
        
        #==========================================================================
        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        
        student_number_list = data.grade_table_column_list("Student_Number")
        
        course_id_list = data.grade_table_column_list("Professor_ID")
        
        professor_id_list = data.grade_table_column_list("Course_ID")
        
        table = data.grade_table()
        
        value = self.searchText.get()
        #==========================================================================
        selection = self.searchSelection.get()
    
        #==========================================================================
        if (selection == "Student_Number"):
            
            if (value in student_number_list):
                pass
            else:
                messagebox.showerror("ERROR","There is no such a username")
                
            for id in table:
                if (id[0] == value):
                    self.student_grade_table.insert('', 'end', values=(id[0],id[1],id[2],id[3]))
                      
        
        elif (selection =="Course_ID"):
            
            if (value in course_id_list):
                pass
            else:
                messagebox.showerror("ERROR","There is no such a course_id")
                
            for id in table:
                if (id[1] == value):
                    self.student_grade_table.insert('', 'end', values=(id[0],id[1],id[2],id[3]))
            
            
        
        elif (selection =="Professor_Professor_ID"):
            
            if (value in professor_id_list):
                pass
            else:
                messagebox.showerror("ERROR","There is no such a Professor_ID")
                
            for id in table:
                if (id[2] == value):
                    self.student_grade_table.insert('', 'end', values=(id[0],id[1],id[2],id[3]))
                 
        elif (selection =="grade"):
            
            try:
                value = float(value)
            except:
                messagebox.showerror("ERROR","Please enter number:")
            
            for id in table:
                if (id[3] >= float(value)):
                    self.student_grade_table.insert('', 'end', values=(id[0],id[1],id[2],id[3]))

    def add_item(self):
        
        flag = False
        student_id = self.student_id_entry.get()
        course_id = self.course_ID_entry.get()
        professor_id = self.professor_ID_entry.get()
        grade = self.student_grade_entry.get()
        
        try:
            grade = int (grade)
        except:
            messagebox.showerror("error", "Please enter the number")
            self.student_grade_entry.delete(0, 'end')
        
        
            
        if (student_id == "" or course_id =="" or professor_id =="" or grade <0 or grade >100):
            messagebox.showerror("ERROR", "Please enter a valid entry Student_id, course_id and professor_id should not be empty"
                                +"grade should be b/w 0 and 100")
        else:
            flag = True
            
        #=================================================================================
        connect_database_student_table = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        student_id_result = connect_database_student_table.student_table()
        student_id_result_list = []
        
        for id in student_id_result:
            student_id_result_list.append(id[0])
            
        #=================================================================================
        connect_database_course_table = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        course_id_result = connect_database_course_table.course_table()
        course_id_result_list = []
        
        for id in course_id_result:
            course_id_result_list.append(id[0])
        #=================================================================================
        connect_database_professor_table = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        professor_id_result = connect_database_professor_table.professor_table()
        professor_id_result_list = []
        
        for id in professor_id_result:
            professor_id_result_list.append(id[0])
        #=================================================================================
        
        if student_id in student_id_result_list:
            pass
        else:
            flag = False
            messagebox.showerror("ERROR","Student_id does not exist in student_table, Foreign key constraint")
        
        if course_id in course_id_result_list:
            pass
        else:
            flag = False
            messagebox.showerror("ERROR","Course_id does not exist in course_table, Foreign key constraint")
            
        if professor_id in professor_id_result_list:
            pass
        else:
            flag = False
            messagebox.showerror("ERROR","Professor_id does not exist in professor_table, Foreign key constraint")
        
        #=================================================================================
        connect_database_grade_table = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        grade_result = connect_database_grade_table.grade_table()
        grade_result_list = []
        
        for id in grade_result:
            grade_result_list.append(id[0]+id[1])
        
        if ((student_id+course_id) in grade_result_list):
            flag = False
            messagebox.showerror("ERROR","There is a COMPOSITE KEY student_id and course_id should be unique, it exist already in the system")
            
            
        #=================================================================================
        
        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            
            query = """INSERT INTO `mydb`.`grade`(Student_Number, Course_ID, Professor_Professor_ID, grade)
                        VALUES (%s, %s,%s, %s)
            """
            
            val = (student_id, course_id,professor_id,grade)
            cursor = con.cursor()
            cursor.execute(query,val)
            con.commit()
            con.close()
            messagebox.showinfo("Information","Successfully added")
            self.searchText_set.set(student_id)
            self.searchSelection.set("Student_Number")
            self.searchIT()

    def clearfix(self):
        self.student_id_entry.delete(0, 'end')
        self.course_ID_entry.delete(0, 'end')
        self.professor_ID_entry.delete(0,'end')
        self.student_grade_entry.delete(0, 'end')
    
    def delete_data(self):
        
        student_id = self.student_id_entry.get()
        course_id = self.course_ID_entry.get()
        
        flag = False
        
        connect_database_grade_table = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        grade_result = connect_database_grade_table.grade_table()
        grade_result_list = []
        
        for id in grade_result:
            grade_result_list.append(id[0]+id[1])
        
        if ((student_id+course_id) in grade_result_list):
            flag = True
        else:
            messagebox.showerror("ERROR", "Your information is student and course not in the system")
            
            
        if (flag):
            con = mysql.connector.connect(
                    host=self.set_host,
                    user=self.set_user,
                    passwd=self.set_password)
            cursor = con.cursor()
            query = """
                DELETE FROM `mydb`.`grade`
                WHERE (Student_Number,Course_ID) in ((%s,%s))
                """
            val = (self.student_id_entry.get(),self.course_ID_entry.get())
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Deleted","Information is deleted")
            self.search_all()
            self.clearfix()

    def update_item(self):
        flag = False
        
        student_id = self.student_id_entry.get()
        course_id = self.course_ID_entry.get()
        professor_id = self.professor_ID_entry.get()
        grade = self.student_grade_entry.get()
        
        if(student_id !="") and (course_id !="") and (professor_id !="") and (grade !=""):
            flag = True
        else:
            messagebox.showerror("ERROR","Please fill all the blanks without missing")
            flag = False
            
        try:
            grade = int(grade)
        except:
            messagebox.showerror("ERROR","Please enter a number")
            flag = False
        
        if (grade <= 100 and grade>0):
            flag = True
            pass
        else:
            messagebox.showerror("ERROR","Grade should be b/w 0 and 100")
            
        #=====================================================================================================   
        connect_database_grade_table = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        grade_result = connect_database_grade_table.grade_table()
        grade_result_list = []
        
        for id in grade_result:
            grade_result_list.append(id[0]+id[1])
        
        if ((student_id+course_id) in grade_result_list):
            flag = True
        else:
            flag = False
            messagebox.showerror("ERROR", "Your information is wrong no grade for that student and course")   
        #===================================================================================================== 
        connect_database_professor_table = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        professor_id_result = connect_database_professor_table.professor_table()
        professor_id_result_list = []
        
        for id in professor_id_result:
            professor_id_result_list.append(id[0])
        
        if professor_id in professor_id_result_list:
            pass
        else: 
            flag = False
            messagebox.showerror("ERROR", "There is no professor_id in the system like that")
        #=====================================================================================================
        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
            UPDATE `mydb`.`grade` SET 
            
            Professor_Professor_ID = %s,
            grade = %s

            WHERE (Student_Number,Course_ID) in ((%s,%s))
            """
            val = (professor_id,int(grade),student_id,course_id)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Update","Informations are updated")
            self.searchText_set.set(student_id)
            self.searchSelection.set("Student_Number")
            self.searchIT()
        
    def adminGradeAction(self):
        self.window.destroy()
        go_admin = AdminWindow(self.set_host,self.set_user,self.set_password)

class admin_username_password:

    def __init__(self,host,user,password):
        self.set_host = host
        self.set_user = user
        self.set_password = password

        self.window = tk.Tk()
        self.window.title("Admin Username and Password Database")
        self.window.geometry("1530x1080+0+0")
        self.window.resizable(0, 0)

        title = tk.Label(self.window, text="Admin >> Update Username and Password", font=("consolas", 35, "bold")
                             , background="#AAD8BC", fg="#fefefe", relief="groove")
        title.pack(side="top", fill="x")

        # SET OF data============================================================================================
        self.instructionframe = tk.Frame(self.window, bd=4, relief="ridge", background="#AAD8BC")
        self.instructionframe.place(x=20, y=80, width=500, height=700)

        self.ins_title = tk.Label(self.instructionframe, text="Update Username and Password", font=("consolas", 20, "bold"),
                                      fg="#fefefe"
                                      , background="#AAD8BC")
        self.ins_title.grid(row=0, columnspan=2, pady=20, padx=20, sticky="w")

            # >>>>username
        self.username = tk.Label(self.instructionframe, text="Username ", font=("consolas", 14, "bold"),
                                       fg="#fefefe"
                                       , background="#AAD8BC")
        self.username.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.username_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4, relief="ridge")
        self.username_entry.grid(row=1, column=1, pady=10, padx=20, sticky="w")

            # >>>>typeOfUser

        self.typeOfUser = tk.Label(self.instructionframe, text="Type of User",
                                         font=("consolas", 14, "bold"),
                                         fg="#fefefe"
                                         , background="#AAD8BC")
        self.typeOfUser.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.typeOfUser_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                               relief="ridge")
        self.typeOfUser_entry.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # >>>>Password

        self.password = tk.Label(self.instructionframe, text="Password ",
                                 font=("consolas", 14, "bold"),
                                 fg="#fefefe"
                                 , background="#AAD8BC")
        self.password.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        self.password_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                       relief="ridge")
        self.password_entry.grid(row=3, column=1, pady=10, padx=20, sticky="w")

        # SET OF INSTRUCTION============================================================================================
        self.commandFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#AAD8BC")
        self.commandFrame.place(x=20, y=630, width=500, height=150)

        # >>>>add
        self.add_btn = tk.Button(self.commandFrame, text="Add", font=("consolas", 15, "bold"), fg="#2C3E50",
                                 background="#fefefe",
                                 relief="groove", width=8, command=self.add_item)
        self.add_btn.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # >>>>delete
        self.delete_btn = tk.Button(self.commandFrame, text="Delete", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command=self.delete_data)
        self.delete_btn.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # >>>>update
        self.update_btn = tk.Button(self.commandFrame, text="Update", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command=self.update_item)
        self.update_btn.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        # >>>>clear
        self.clear_btn = tk.Button(self.commandFrame, text="Clear", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="groove", width=8, command=self.clearfix)
        self.clear_btn.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        # SET OF RESULT================================================================================================

        self.detailFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#AAD8BC")
        self.detailFrame.place(x=540, y=80, width=960, height=700)

        # >>>>search

        self.search = tk.Label(self.detailFrame, text="Search By ",
                               font=("consolas", 20, "bold"),
                               fg="#fefefe"
                               , background="#AAD8BC")
        self.search.grid(row=0, column=0, pady=20, padx=10, sticky="w")
        self.searchSelection = tk.StringVar()

        self.search_by = ttk.Combobox(self.detailFrame, font=("consolas", 16, "bold"),
                                      textvariable=self.searchSelection)

        self.search_by['values'] = (
            'username', 'typeOfUser')
        self.search_by.grid(row=0, column=1, pady=20, padx=10, sticky="w")

        # >>>>search text
        self.searchText = tk.Entry(self.detailFrame, font=("consolas", 14, "bold"), bd=4,
                                   relief="ridge")
        self.searchText.grid(row=0, column=2, pady=20, padx=10, sticky="w")
        # >>>>search button

        self.searchbtn = tk.Button(self.detailFrame, text="Search", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="raised", width=8, command=self.searchIT)

        self.searchbtn.grid(row=0, column=3, pady=20, padx=10, sticky="w")
        # >>>>search all button

        self.searchAllbtn = tk.Button(self.detailFrame, text="Search All", font=("consolas", 15, "bold"),
                                      fg="#2C3E50",
                                      background="#fefefe",
                                      relief="raised", width=10, command=self.search_all)

        self.searchAllbtn.grid(row=0, column=4, pady=20, padx=10, sticky="w")

        # SET OF Database Table ============================================================================================
        self.dataFrame = tk.Frame(self.window, bd=4, relief="ridge", bg="#fefefe")
        self.dataFrame.place(x=560, y=180, width=920, height=580)

        # Student Table from database
        self.scrollx = tk.Scrollbar(self.dataFrame, orient="horizontal")
        self.scrolly = tk.Scrollbar(self.dataFrame, orient="vertical")

        self.username_and_password_table = ttk.Treeview(self.dataFrame, columns=(
            'username', 'typeOfUser', 'password'),
                                                        xscrollcommand=self.scrollx.set,
                                                        yscrollcommand=self.scrolly.set)
        self.scrollx.pack(side="bottom", fill="x")
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.config(command=self.username_and_password_table.xview)
        self.scrolly.config(command=self.username_and_password_table.yview)
        self.username_and_password_table.heading('username', text="Username")
        self.username_and_password_table.heading('typeOfUser', text='User Type')
        self.username_and_password_table.heading('password', text="Password")
        self.username_and_password_table['show'] = 'headings'

        self.username_and_password_table.column('username', width=120)
        self.username_and_password_table.column('typeOfUser', width=120)
        self.username_and_password_table.column('password', width=120)

        self.username_and_password_table.pack(fill="both", expand=1)
        # ==============================================================================================================
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.filemenu.add_command(label="Return", command=self.adminPaswAction)
        self.window.config(menu=self.filemenu)
        self.window.mainloop()

    #**********************************************************************************************************
    def update_item(self):

        username = self.username_entry.get()
        typeOfUser = self.typeOfUser_entry.get()
        password = self.password_entry.get()
        flag = False

        if (username != "") and (typeOfUser != "") and (password != ""):
            flag = True
        else:
            messagebox.showerror("ERROR", "Please fill all the blanks without missing")
            flag = False

        # >>>>password validation
        sum = 0
        for i in password:
            sum += 1
        if (sum < 6):
            messagebox.showerror("ERROR", "Please enter valid password at least 6 character")
            flag = False
        else:
            flag = True
        #=================================================================================================
        if (username.startswith("C") and typeOfUser != "Student"):
            messagebox.showerror("ERROR","Are you sure, can it be Student?")
            flag = False
        elif (username.startswith("P") and typeOfUser != "Professor"):
            messagebox.showerror("ERROR", "Are you sure, can it be Professor?")
            flag = False
        # =====================================================================================================
        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        usernames = data.username_and_password()
        usernames_list = []
        for id in usernames:
            usernames_list.append(id[0])

        if username in usernames_list:
            flag = True
        else:
            flag = False
            messagebox.showerror("ERROR", "This username does not in the system cannot be updated.")
        #=====================================================================================================
        if (typeOfUser in ["Admin","Student","Professor"]):
            pass
        else:
            messagebox.showerror("ERROR","Please select valid user type Professor, Student or Admin")
            flag = False
        #=====================================================================================================
        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
            UPDATE `mydb`.`UsernameAndPassword` SET 

            typeOfUser = %s,
            password = %s

            WHERE username = %s
            """
            val = (typeOfUser,password,username)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Update", "Informations are updated")
            self.search_all()
    #**********************************************************************************************************
    def delete_data(self):
        username = self.username_entry.get()
        typeOfUser = self.typeOfUser_entry.get()
        password = self.password_entry.get()
        flag = False

        if (self.typeOfUser_entry.get() == "admin"):
            messagebox.showerror("ERROR", "Admin can be only one password and username")

        if(username ==""):
            messagebox.showerror("ERROR","Please enter a user name")
            self.typeOfUser_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
        else:
            flag = True

        if (typeOfUser != "") and (password != ""):
            messagebox.showerror("ERROR", "Please enter only username")
            self.typeOfUser_entry.delete(0, 'end')
            self.password_entry.delete(0,'end')
            flag = False

        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        usernames = data.username_and_password()
        usernames_list = []
        for id in usernames:
            usernames_list.append(id[0])

        if flag:
            if username in usernames_list:
                flag = True
            else:
                flag = False
                messagebox.showerror("ERROR", "Username is not in the system")


        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
                DELETE FROM `mydb`.`UsernameAndPassword`
                WHERE username = %s
                """
            val = (username,)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Deleted", "Information is deleted")
            self.search_all()
            self.clearfix()


    #**********************************************************************************************************
    def add_item(self):
        flag = False
        username = self.username_entry.get()
        typeOfUser = self.typeOfUser_entry.get()
        password = self.password_entry.get()
        # ===========================================================================================================
        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        student_table = data.student_table()
        professor_table = data.professor_table()
        username_list = []

        if (self.typeOfUser_entry.get() == "admin"):
            messagebox.showerror("ERROR", "Admin can be only one password and username")

        for i in student_table:
            username_list.append(i[0])
        for i in professor_table:
            username_list.append(i[0])
        username_list.append("admin")
        # ===========================================================================================================

        if(username =="" or typeOfUser == "" or password == ""):
            messagebox.showerror("ERROR", "Please fill all the section")
            flag = False
        else:
            flag = True

        #>>>>password validation
        if (flag):
            sum = 0
            for i in password:
                sum+=1
            if (sum <6):
                messagebox.showerror("ERROR", "Please enter valid password at least 6 character")
                flag = False
            else:
                flag = True
        #========================
        if (flag):
            if (username in username_list):
                flag = True
            else:
                flag = False
                messagebox.showerror("ERROR","username should be admin, student_id or professor_id which are recorded in the system, OTHERWISE YOU CANNOT ADD")

        #===========================================================================================================
        if (flag):
            if (username.startswith("P") and typeOfUser !="Professor"):
                messagebox.showerror("ERROR", "Are you sure, Can it be professor?")
                flag = False
            elif (username.startswith("C") and typeOfUser != "Student"):
                messagebox.showerror("ERROR", "Are you sure, Can it be student?")
                flag = False


        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)

            query = """INSERT INTO `mydb`.`UsernameAndPassword`(username, typeOfUser, password)
                        VALUES (%s, %s,%s)
            """

            val = (username, typeOfUser,password)
            cursor = con.cursor()
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Information", "Successfully added")
            self.search_all()



    #**************************************************************************************************************************

    def search_all(self):
        
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.username_and_password()

        self.username_and_password_table.delete(*self.username_and_password_table.get_children())

        for data in datas:
            self.username_and_password_table.insert('','end',values =(data[0],data[1],data[2]))

    def searchIT(self):

        self.username_and_password_table.delete(*self.username_and_password_table.get_children())
        # ==========================================================================
        value = self.searchText.get()
        selection = self.searchSelection.get()

        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)

        credential = data.username_and_password()

        self.username_list = []
        self.typeOfUser_list = []


        for i in credential:
            self.username_list.append(i[0])
            self.typeOfUser_list.append(i[1])
        # ==========================================================================

        if (selection == ""):
            messagebox.showerror("ERROR","Please select search type")
        else:
            if (selection == "username"):
                if (value in self.username_list):
                    for id in credential:
                        if id[0] == value:
                            self.username_and_password_table.insert('','end',values=(id[0],id[1],id[2]))
                else:
                    messagebox.showerror("ERROR", "Please enter valid username, does not have any record in the system for the user")

            elif (selection == "typeOfUser"):
                if (value in self.typeOfUser_list):
                    for id in credential:
                        if id[1] == value:
                            self.username_and_password_table.insert('','end',values=(id[0],id[1],id[2]))
                else:
                    messagebox.showerror("ERROR", "There is no such a user type in the system")

    def clearfix(self):
        self.username_entry.delete(0, 'end')
        self.typeOfUser_entry.delete(0, 'end')
        self.password_entry.delete(0,'end')

    
    def adminPaswAction(self):
        self.window.destroy()
        go_admin = AdminWindow(self.set_host,self.set_user,self.set_password)

class admin_professor:
    def __init__(self,host,user,password):
        self.set_host = host
        self.set_user = user
        self.set_password = password

        self.window = tk.Tk()
        self.window.title("Admin Professor Database")
        self.window.geometry("1530x1080+0+0")
        self.window.resizable(0, 0)

        title = tk.Label(self.window, text="Admin >> Update Professor Information", font=("consolas", 35, "bold")
                         , background="#67746A", fg="#fefefe", relief="groove")
        title.pack(side="top", fill="x")

        # SET OF data============================================================================================
        self.instructionframe = tk.Frame(self.window, bd=4, relief="ridge", background="#67746A")
        self.instructionframe.place(x=20, y=80, width=500, height=700)

        self.ins_title = tk.Label(self.instructionframe, text="Update Professor",
                                  font=("consolas", 20, "bold"),
                                  fg="#fefefe"
                                  , background="#67746A")
        self.ins_title.grid(row=0, columnspan=2, pady=20, padx=20, sticky="w")

        # >>>>Professor_ID
        self.professor_ID = tk.Label(self.instructionframe, text="Professor ID ", font=("consolas", 14, "bold"),
                                 fg="#fefefe"
                                 , background="#67746A")
        self.professor_ID.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.professor_ID_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4, relief="ridge")
        self.professor_ID_entry.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        # >>>>Professor First Name

        self.professorFirstName = tk.Label(self.instructionframe, text="Professor First Name",
                                   font=("consolas", 14, "bold"),
                                   fg="#fefefe"
                                   , background="#67746A")
        self.professorFirstName.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.professorFirstName_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                         relief="ridge")
        self.professorFirstName_entry.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # >>>>Professor Last Name

        self.professorLastName = tk.Label(self.instructionframe, text="Professor Last Name",
                                 font=("consolas", 14, "bold"),
                                 fg="#fefefe"
                                 , background="#67746A")
        self.professorLastName.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        self.professorLastName_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                       relief="ridge")
        self.professorLastName_entry.grid(row=3, column=1, pady=10, padx=20, sticky="w")

        # >>>>Professor Email

        self.professor_email = tk.Label(self.instructionframe, text="Professor Email ",
                                 font=("consolas", 14, "bold"),
                                 fg="#fefefe"
                                 , background="#67746A")
        self.professor_email.grid(row=4, column=0, pady=10, padx=20, sticky="w")

        self.professor_email_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                       relief="ridge")
        self.professor_email_entry.grid(row=4, column=1, pady=10, padx=20, sticky="w")



        # SET OF INSTRUCTION============================================================================================
        self.commandFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#67746A")
        self.commandFrame.place(x=20, y=630, width=500, height=150)

        # >>>>add
        self.add_btn = tk.Button(self.commandFrame, text="Add", font=("consolas", 15, "bold"), fg="#2C3E50",
                                 background="#fefefe",
                                 relief="groove", width=8, command = self.add_item)
        self.add_btn.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # >>>>delete
        self.delete_btn = tk.Button(self.commandFrame, text="Delete", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command = self.delete_data)
        self.delete_btn.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # >>>>update
        self.update_btn = tk.Button(self.commandFrame, text="Update", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command = self.update_item)
        self.update_btn.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        # >>>>clear
        self.clear_btn = tk.Button(self.commandFrame, text="Clear", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="groove", width=8, command = self.clearfix)
        self.clear_btn.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        # SET OF RESULT================================================================================================

        self.detailFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#67746A")
        self.detailFrame.place(x=540, y=80, width=960, height=700)

        # >>>>search

        self.search = tk.Label(self.detailFrame, text="Search By ",
                               font=("consolas", 20, "bold"),
                               fg="#fefefe"
                               , background="#67746A")
        self.search.grid(row=0, column=0, pady=20, padx=10, sticky="w")
        self.searchSelection = tk.StringVar()

        self.search_by = ttk.Combobox(self.detailFrame, font=("consolas", 16, "bold"),
                                      textvariable=self.searchSelection)

        self.search_by['values'] = (
            'Professor_ID', 'ProfessorFirstName', 'ProfessorLastName', 'ProfessorEmail')
        self.search_by.grid(row=0, column=1, pady=20, padx=10, sticky="w")

        # >>>>search text
        self.searchText = tk.Entry(self.detailFrame, font=("consolas", 14, "bold"), bd=4,
                                   relief="ridge")
        self.searchText.grid(row=0, column=2, pady=20, padx=10, sticky="w")
        # >>>>search button

        self.searchbtn = tk.Button(self.detailFrame, text="Search", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="raised", width=8, command = self.searchIT)

        self.searchbtn.grid(row=0, column=3, pady=20, padx=10, sticky="w")
        # >>>>search all button

        self.searchAllbtn = tk.Button(self.detailFrame, text="Search All", font=("consolas", 15, "bold"),
                                      fg="#2C3E50",
                                      background="#fefefe",
                                      relief="raised", width=10, command = self.search_all)

        self.searchAllbtn.grid(row=0, column=4, pady=20, padx=10, sticky="w")

        # SET OF Database Table ============================================================================================
        self.dataFrame = tk.Frame(self.window, bd=4, relief="ridge", bg="#fefefe")
        self.dataFrame.place(x=560, y=180, width=920, height=580)

        # Student Table from database
        self.scrollx = tk.Scrollbar(self.dataFrame, orient="horizontal")
        self.scrolly = tk.Scrollbar(self.dataFrame, orient="vertical")

        self.professor_table = ttk.Treeview(self.dataFrame, columns=(
            'Professor_ID', 'ProfessorFirstName', 'ProfessorLastName', 'ProfessorEmail'),
                                                xscrollcommand=self.scrollx.set,
                                                yscrollcommand=self.scrolly.set)
        self.scrollx.pack(side="bottom", fill="x")
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.config(command=self.professor_table.xview)
        self.scrolly.config(command=self.professor_table.yview)
        self.professor_table.heading('Professor_ID', text="Professor_ID")
        self.professor_table.heading('ProfessorFirstName', text='ProfessorFirstName')
        self.professor_table.heading('ProfessorLastName', text='ProfessorLastName')
        self.professor_table.heading('ProfessorEmail', text='ProfessorEmail')
        self.professor_table['show'] = 'headings'

        self.professor_table.column('Professor_ID', width=120)
        self.professor_table.column('ProfessorFirstName', width=120)
        self.professor_table.column('ProfessorLastName', width=120)
        self.professor_table.column('ProfessorEmail', width=120)


        self.professor_table.pack(fill="both", expand=1)
        # ==============================================================================================================
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.filemenu.add_command(label="Return", command=self.adminProAction)
        self.window.config(menu=self.filemenu)
        

        self.window.mainloop()

    #******************************************************************************************************************
    def update_item(self):

        flag = False
        professor_id = self.professor_ID_entry.get()
        professor_first_name = self.professorFirstName_entry.get()
        professor_last_name = self.professorLastName_entry.get()
        professor_email = self.professor_email_entry.get()

        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        professor_id_list = []
        professor_table = data.professor_table()
        for i in professor_table:
            professor_id_list.append(i[0])

        if professor_id in professor_id_list:
            flag = True
        else:
            messagebox.showerror("ERROR","Please enter a valid username")

        if (flag):
            if (professor_id == "") or (professor_first_name == "") or (professor_last_name == "") or (
                    professor_email == ""):
                flag = False
                messagebox.showerror("ERROR", "Please fill all the sections")
            else:
                flag = True


        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
            UPDATE `mydb`.`Professor` SET   

            ProfessorFirstName = %s,
            ProfessorLastName = %s,
            ProfessorEmail = %s
            
            WHERE Professor_ID = %s
            """

            val = (professor_first_name,professor_last_name,professor_email,professor_id)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Update", "Informations are updated")
            self.search_all()

    def delete_data(self):
        flag = False
        professor_id = self.professor_ID_entry.get()
        professor_first_name = self.professorFirstName_entry.get()
        professor_last_name = self.professorLastName_entry.get()
        professor_email = self.professor_email_entry.get()

        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        grade_professor_id_list = data.grade_table_column_list("Professor_ID")

        if (professor_id in grade_professor_id_list):
            messagebox.showerror("ERROR","You cannot delete it is associated with grade table")
            flag = False
        else:
            flag = True

        if (flag):
            if (professor_email !="") or (professor_last_name !="") or (professor_first_name != ""):
                messagebox.showerror("ERROR","Please enter only username")
                self.professorFirstName_entry.delete(0, 'end')
                self.professorLastName_entry.delete(0, 'end')
                self.professor_email_entry.delete(0, 'end')
                flag = False
            else:
                flag = True

        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
                DELETE FROM `mydb`.`Professor`
                WHERE Professor_ID = %s
                """
            val = (professor_id,)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Deleted", "Information is deleted")
            self.search_all()
            self.clearfix()



    def add_item(self):
        flag = False
        professor_id = self.professor_ID_entry.get()
        professor_first_name = self.professorFirstName_entry.get()
        professor_last_name = self.professorLastName_entry.get()
        professor_email = self.professor_email_entry.get()
        # ===========================================================================================================
        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        professor_table = data.professor_table()
        professor_id_list = []

        for i in professor_table:
            professor_id_list.append(i[0])
        #===========================================================================================================
        if professor_id in professor_id_list:
            flag = False
            messagebox.showerror("ERROR","User is already in the system")
        else:
            flag = True
        #===========================================================================================================

        if (professor_id == "") or (professor_first_name =="") or (professor_last_name == "") or (professor_email ==""):
            flag = False
            messagebox.showerror("ERROR", "Please fill all the sections")
        else:
            flag = True

        if (professor_id.startswith("P")):
            pass
        else:
            messagebox.showerror("ERROR", "Professor_ID should start with P")
            flag = False

        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)

            query = """INSERT INTO `mydb`.`Professor`(Professor_ID, ProfessorFirstName, ProfessorLastName, ProfessorEmail)
                        VALUES (%s, %s,%s,%s)
            """

            val = (professor_id, professor_first_name,professor_last_name,professor_email)
            cursor = con.cursor()
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Information", "Successfully added")
            self.search_all()


    def searchIT(self):

        self.professor_table.delete(*self.professor_table.get_children())
        #==========================================================================
        value = self.searchText.get()
        selection = self.searchSelection.get()

        data = database.reach_tables_data(self.set_host,self.set_user,self.set_password)

        credential = data.professor_table()

        professor_id_list = []
        prof_name_list = []
        prof_surname_list =[]
        prof_email_list = []

        for i in credential:
            professor_id_list.append(i[0])
            prof_name_list.append(i[1])
            prof_surname_list.append(i[2])
            prof_email_list.append(i[3])


        if (selection == ""):
            messagebox.showerror("ERROR","Please select search type")
        else:
            if (selection == "Professor_ID"):
                if (value in professor_id_list):
                    for id in credential:
                         if id[0] == value:
                             self.professor_table.insert('','end',values=(id[0],id[1],id[2],id[3]))
                else:
                    messagebox.showerror("ERROR", "Please enter valid ID, does not have any record in the system for this ID")

            elif (selection == "ProfessorFirstName"):
                if (value in prof_name_list):
                    for id in credential:
                        if id[1] == value:
                            self.professor_table.insert('', 'end', values=(id[0], id[1], id[2], id[3]))
                else:
                    messagebox.showerror("ERROR",
                                         "Please enter valid name, does not have any record in the system for this name")

            elif (selection == 'ProfessorLastName'):
                if (value in prof_surname_list):
                    for id in credential:
                        if id[2] == value:
                            self.professor_table.insert('', 'end', values=(id[0], id[1], id[2], id[3]))
                else:
                    messagebox.showerror("ERROR",
                                         "Please enter valid name, does not have any record in the system for this surname")

            elif (selection == 'ProfessorEmail'):
                if (value in prof_email_list):
                    for id in credential:
                        if id[3] == value:
                            self.professor_table.insert('', 'end', values=(id[0], id[1], id[2], id[3]))
                else:
                    messagebox.showerror("ERROR",
                                         "Please enter valid email, does not have any record in the system for this email")

    def search_all(self):
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.professor_table()

        self.professor_table.delete(*self.professor_table.get_children())

        for data in datas:
            self.professor_table.insert('', 'end', values=(data[0], data[1], data[2],data[3]))


    def clearfix(self):
        self.professor_ID_entry.delete(0, 'end')
        self.professorFirstName_entry.delete(0, 'end')
        self.professorLastName_entry.delete(0,'end')
        self.professor_email_entry.delete(0,'end')



    def adminProAction(self):
        self.window.destroy()
        go_admin = AdminWindow(self.set_host,self.set_user,self.set_password)
        self.window.mainloop()

class admin_course:

    def __init__(self,host,user,password):
        self.set_host = host
        self.set_user = user
        self.set_password = password

        self.window = tk.Tk()
        self.window.title("Admin Course Database")
        self.window.geometry("1530x1080+0+0")
        self.window.resizable(0, 0)

        title = tk.Label(self.window, text="Admin >> Update Course Information", font=("consolas", 35, "bold")
                         , background="#626D83", fg="#fefefe", relief="groove")
        title.pack(side="top", fill="x")

        # SET OF data============================================================================================
        self.instructionframe = tk.Frame(self.window, bd=4, relief="ridge", background="#626D83")
        self.instructionframe.place(x=20, y=80, width=500, height=700)

        self.ins_title = tk.Label(self.instructionframe, text="Update Professor",
                                  font=("consolas", 20, "bold"),
                                  fg="#fefefe"
                                  , background="#626D83")
        self.ins_title.grid(row=0, columnspan=2, pady=20, padx=20, sticky="w")

        # >>>>Course_ID
        self.course_ID = tk.Label(self.instructionframe, text="Course ID", font=("consolas", 14, "bold"),
                                     fg="#fefefe"
                                     , background="#626D83")
        self.course_ID.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.course_ID_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4, relief="ridge")
        self.course_ID_entry.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        # >>>>Course Name

        self.course_Name = tk.Label(self.instructionframe, text="Course Name",
                                           font=("consolas", 14, "bold"),
                                           fg="#fefefe"
                                           , background="#626D83")
        self.course_Name.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.course_Name_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                                 relief="ridge")
        self.course_Name_entry.grid(row=2, column=1, pady=10, padx=20, sticky="w")



        # SET OF INSTRUCTION============================================================================================
        self.commandFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#626D83")
        self.commandFrame.place(x=20, y=630, width=500, height=150)

        # >>>>add
        self.add_btn = tk.Button(self.commandFrame, text="Add", font=("consolas", 15, "bold"), fg="#2C3E50",
                                 background="#fefefe",
                                 relief="groove", width=8,command = self.add_item)
        self.add_btn.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # >>>>delete
        self.delete_btn = tk.Button(self.commandFrame, text="Delete", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command = self.delete_data)
        self.delete_btn.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # >>>>update
        self.update_btn = tk.Button(self.commandFrame, text="Update", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command = self.update_item)
        self.update_btn.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        # >>>>clear
        self.clear_btn = tk.Button(self.commandFrame, text="Clear", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="groove", width=8, command = self.clearfix)
        self.clear_btn.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        # SET OF RESULT================================================================================================

        self.detailFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#626D83")
        self.detailFrame.place(x=540, y=80, width=960, height=700)

        # >>>>search all
        self.searchAllbtn = tk.Button(self.detailFrame, text="Search All", font=("consolas", 15, "bold"),
                                      fg="#2C3E50",
                                      background="#fefefe",
                                      relief="raised", width=20, command = self.search_all)

        self.searchAllbtn.grid(row=0, column=2, columnspan=4, pady=20, padx=20, sticky="w")

        # SET OF Database Table ============================================================================================
        self.dataFrame = tk.Frame(self.window, bd=4, relief="ridge", bg="#fefefe")
        self.dataFrame.place(x=560, y=180, width=920, height=580)

        # Student Table from database
        self.scrollx = tk.Scrollbar(self.dataFrame, orient="horizontal")
        self.scrolly = tk.Scrollbar(self.dataFrame, orient="vertical")

        self.course_table = ttk.Treeview(self.dataFrame, columns=(
            'Course_ID', 'CourseName'),
                                            xscrollcommand=self.scrollx.set,
                                            yscrollcommand=self.scrolly.set)
        self.scrollx.pack(side="bottom", fill="x")
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.config(command=self.course_table.xview)
        self.scrolly.config(command=self.course_table.yview)
        self.course_table.heading('Course_ID', text="Course ID")
        self.course_table.heading('CourseName', text='Course Name')

        self.course_table['show'] = 'headings'

        self.course_table.column('Course_ID', width=120)
        self.course_table.column('CourseName', width=120)


        self.course_table.pack(fill="both", expand=1)
        # ==============================================================================================================
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.filemenu.add_command(label="Return", command=self.adminCourseAction)
        self.window.config(menu=self.filemenu)
        self.search_all()
        self.window.mainloop()

    def add_item(self):
        flag = False
        course_id = self.course_ID_entry.get()
        course_name = self.course_Name_entry.get()

        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.course_table()
        course_id_list = []

        for i in datas:
            course_id_list.append(i[0])

        if course_id in course_id_list:
            messagebox.showerror("ERROR", "This course ID is already in the system")
        else:
            flag = True

        if(flag):
            if(course_id.startswith("CSD")):
                pass
            else:
                flag = False
                messagebox.showerror("ERROR","Course ID should start with CSD")
            if (flag):
                sum = 0
                for i in course_id:
                    sum+=1
                if (sum !=7):
                    flag = False
                    messagebox.showerror("ERROR", "It should be seven characters")
                else:
                    flag = True

        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)

            query = """INSERT INTO `mydb`.`Course`(Course_ID, CourseName)
                        VALUES (%s, %s)
            """

            val = (course_id,course_name)
            cursor = con.cursor()
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Information", "Successfully added")
            self.search_all()

    def update_item(self):

        flag = False
        course_id = self.course_ID_entry.get()
        course_name = self.course_Name_entry.get()

        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.course_table()
        course_id_list = []

        for i in datas:
            course_id_list.append(i[0])

        if course_id in course_id_list:
            flag = True
        else:
            messagebox.showerror("ERROR", "This ID is not in the system, please enter valid ID")

        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
            UPDATE `mydb`.`Course` SET   
            CourseName    = %s
            WHERE Course_ID = %s
            """

            val = (course_name,course_id)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Update", "Informations are updated")
            self.search_all()

    def delete_data(self):

        flag = False
        course_id = self.course_ID_entry.get()
        course_name = self.course_Name_entry.get()

        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        grade_course_id_list = dataCon.grade_table_column_list("Course_ID")

        if (course_id in grade_course_id_list):
            messagebox.showerror("ERROR","You cannot delete, It is associated with grade")
        else:
            flag = True

        if (flag):
            if (course_name != ""):
                messagebox.showerror("ERROR","Please write only course_id to delete data")
                self.course_Name_entry.delete(0, 'end')
                flag = False

        if (flag):
            con = mysql.connector.connect(
                host=self.set_host,
                user=self.set_user,
                passwd=self.set_password)
            cursor = con.cursor()
            query = """
                DELETE FROM `mydb`.`Course`
                WHERE Course_ID = %s
                """
            val = (course_id,)
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Deleted", "Information is deleted")
            self.search_all()
            self.clearfix()



    def search_all(self):
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.course_table()

        self.course_table.delete(*self.course_table.get_children())

        for data in datas:
            self.course_table.insert('', 'end', values=(data[0], data[1]))

    def clearfix(self):
        self.course_ID_entry.delete(0, 'end')
        self.course_Name_entry.delete(0, 'end')


    def adminCourseAction(self):
        self.window.destroy()
        go_admin = AdminWindow(self.set_host,self.set_user,self.set_password)

class ProfessorWindow():
    def __init__(self,user,host,set_user,password):
        self.user = user
        self.set_host = host
        self.set_user = set_user
        self.set_password = password


        self.window = tk.Tk()
        self.window.title("Professor Database for {}".format(self.user))
        self.window.geometry("1530x1080+0+0")

        title = tk.Label(self.window, text="Professor >>{} - {}>> Update Student Grade Data".format(self.user,self.prof_name(self.user) +" "+self.prof_surname(self.user)), font=("consolas", 25, "bold")
                         , background="#1C1E20", fg="#fefefe", relief="groove")
        title.pack(side="top", fill="x")

        # SET OF data============================================================================================
        self.instructionframe = tk.Frame(self.window, bd=4, relief="ridge", background="#1C1E20")
        self.instructionframe.place(x=20, y=80, width=500, height=700)

        self.ins_title = tk.Label(self.instructionframe, text="Update Student Grade", font=("consolas", 25, "bold"),
                                  fg="#fefefe"
                                  , background="#1C1E20")
        self.ins_title.grid(row=0, columnspan=2, pady=20, padx=20, sticky="w")

        # >>>>Student ID
        self.student_id = tk.Label(self.instructionframe, text="Student ID ", font=("consolas", 14, "bold"),
                                   fg="#fefefe"
                                   , background="#1C1E20")
        self.student_id.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.student_id_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4, relief="ridge")
        self.student_id_entry.grid(row=1, column=1, pady=10, padx=20, sticky="w")

        # >>>>Professor ID

        self.professor_ID = tk.Label(self.instructionframe, text="Professor ID ",
                                          font=("consolas", 14, "bold"),
                                          fg="#fefefe"
                                          , background="#1C1E20")
        self.professor_ID.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.professor_ID_entry_text = tk.StringVar()
        self.professor_ID_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                                relief="ridge", textvariable = self.professor_ID_entry_text)
        self.professor_ID_entry.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # >>>>course ID

        self.course_ID = tk.Label(self.instructionframe, text="Course ID ",
                                      font=("consolas", 14, "bold"),
                                      fg="#fefefe"
                                      , background="#1C1E20")
        self.course_ID.grid(row=4, column=0, pady=10, padx=20, sticky="w")

        self.course_ID_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                            relief="ridge")
        self.course_ID_entry.grid(row=4, column=1, pady=10, padx=20, sticky="w")


        # >>>>grade

        self.student_grade = tk.Label(self.instructionframe, text="Student Grade ",
                                      font=("consolas", 14, "bold"),
                                      fg="#fefefe"
                                      , background="#1C1E20")
        self.student_grade.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        self.student_grade_entry = tk.Entry(self.instructionframe, font=("consolas", 14, "bold"), bd=4,
                                            relief="ridge")
        self.student_grade_entry.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        # SET OF INSTRUCTION============================================================================================
        self.commandFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#1C1E20")
        self.commandFrame.place(x=20, y=630, width=500, height=150)

        # >>>>Submit
        self.submit_btn = tk.Button(self.commandFrame, text="Submit", font=("consolas", 15, "bold"), fg="#2C3E50",
                                 background="#fefefe",
                                 relief="groove", width=8, command = self.add_item)
        self.submit_btn.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # >>>>Exit
        self.exit_btn = tk.Button(self.commandFrame, text="Exit", font=("consolas", 15, "bold"), fg="#2C3E50",
                                    background="#fefefe",
                                    relief="groove", width=8, command = self.window.destroy)
        self.exit_btn.grid(row=0, column=1, pady=10, padx=10, sticky="w")

      

        # >>>>Reset
        self.reset_btn = tk.Button(self.commandFrame, text="Reset", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="groove", width=8, command = self.clearfix)
        self.reset_btn.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        # SET OF RESULT================================================================================================

        self.detailFrame = tk.Frame(self.window, bd=4, relief="ridge", background="#1C1E20")
        self.detailFrame.place(x=540, y=80, width=960, height=700)

        # >>>>search

        self.search = tk.Label(self.detailFrame, text="Search By ",
                               font=("consolas", 20, "bold"),
                               fg="#fefefe"
                               , background="#1C1E20")
        self.search.grid(row=0, column=0, pady=20, padx=10, sticky="w")
        self.search_selection = tk.StringVar()

        self.search_by = ttk.Combobox(self.detailFrame, font=("consolas", 16, "bold"),
                                      textvariable=self.search_selection)

        self.search_by['values'] = ('Student_Number')
        self.search_by.grid(row=0, column=1, pady=20, padx=10, sticky="w")

        # >>>>search text
        self.searchText = tk.Entry(self.detailFrame, font=("consolas", 14, "bold"), bd=4,
                                   relief="ridge")
        self.searchText.grid(row=0, column=2, pady=20, padx=10, sticky="w")
        # >>>>search button

        self.searchbtn = tk.Button(self.detailFrame, text="Search", font=("consolas", 15, "bold"), fg="#2C3E50",
                                   background="#fefefe",
                                   relief="raised", width=8, command = self.searchIT)

        self.searchbtn.grid(row=0, column=3, pady=20, padx=10, sticky="w")
        # >>>>search all button

        self.searchAllbtn = tk.Button(self.detailFrame, text="Search All", font=("consolas", 15, "bold"), fg="#2C3E50",
                                      background="#fefefe",
                                      relief="raised", width=10, command = self.search_all)

        self.searchAllbtn.grid(row=0, column=4, pady=20, padx=10, sticky="w")

        # SET OF Database Table ============================================================================================
        self.dataFrame = tk.Frame(self.window, bd=4, relief="ridge", bg="#fefefe")
        self.dataFrame.place(x=560, y=180, width=920, height=580)

        # Student Table from database
        self.scrollx = tk.Scrollbar(self.dataFrame, orient="horizontal")
        self.scrolly = tk.Scrollbar(self.dataFrame, orient="vertical")

        self.student_grade_table = ttk.Treeview(self.dataFrame, columns=(
        'Student_Number', 'Student_Name',"Professor_ID","ProfessorName",'Course_ID',"Course_Name",'grade'),
                                          xscrollcommand=self.scrollx.set,
                                          yscrollcommand=self.scrolly.set)
        self.scrollx.pack(side="bottom", fill="x")
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.config(command=self.student_grade_table.xview)
        self.scrolly.config(command=self.student_grade_table.yview)
        self.student_grade_table.heading("Student_Number", text="Student_ID")
        self.student_grade_table.heading('Student_Name', text='Student_Name')
        self.student_grade_table.heading("Professor_ID", text="Professor_ID")
        self.student_grade_table.heading("ProfessorName", text="ProfessorName")
        self.student_grade_table.heading('Course_ID', text='Course_ID')
        self.student_grade_table.heading("Course_Name", text="Course_Name")
        self.student_grade_table.heading('grade', text='Student_Grade')

        self.student_grade_table['show'] = 'headings'

        self.student_grade_table.column("Student_Number", width=120)
        self.student_grade_table.column('Student_Name', width=120)
        self.student_grade_table.column("Professor_ID", width=120)
        self.student_grade_table.column("ProfessorName", width=140)
        self.student_grade_table.column('Course_ID', width=120)
        self.student_grade_table.column("Course_Name", width=120)
        self.student_grade_table.column('grade', width=120)


        self.student_grade_table.pack(fill="both", expand=1)
        # ==============================================================================================================
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.filemenu.add_command(label="Return", command=self.profGradeAction)
        self.window.config(menu=self.filemenu)

        self.professor_ID_entry_text.set(self.user)
        self.window.mainloop()

    #*******************************************************************************************************************
    def clearfix(self):
        self.student_id_entry.delete(0,'end')
        self.course_ID_entry.delete(0,'end')
        self.professor_ID_entry.delete(0,'end')
        self.student_grade_entry.delete(0,'end')


    def search_all(self):
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.grade_table()

        self.student_grade_table.delete(*self.student_grade_table.get_children())

        for data in datas:
            if (data[2] == self.user):
                self.student_grade_table.insert('', 'end', values=(data[0],self.student_name(data[0]),data[2],self.prof_name(data[2]),data[1],self.course_name(data[1]),data[3]))

    def searchIT(self):

        self.student_grade_table.delete(*self.student_grade_table.get_children())

        value = self.searchText.get()
        selection = self.search_selection.get()
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.grade_table()

        if (selection == "Student_Number"):
            for id in datas:
                if id[0] == value:
                    if id[2] == self.user:
                        self.student_grade_table.insert('','end',values=(id[0],self.student_name(id[0]),id[2],self.prof_name(id[2]),id[1],self.course_name(id[1]),id[3]))
        else:
            messagebox.showerror("ERROR","Please select type")

    def add_item(self):
        student_id = self.student_id_entry.get()
        professor_id = self.professor_ID_entry.get()
        course_id = self.course_ID_entry.get()
        grade = self.student_grade_entry.get()

        flag = False

        try:
            grade = int(grade)
        except:
            messagebox.showerror("ERROR", "Please enter number")

        if (grade <100 and grade>0):
            flag = True
        else:
            messagebox.showerror("ERROR","Please enter b/w 0 and 100")

        #===============================================================================================================
        student_id_list = []
        professor_id_list = []
        course_id_list = []
        primary_key_list = []

        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas_student_table = dataCon.student_table()
        datas_prof_table = dataCon.professor_table()
        datas_course_table = dataCon.course_table()
        primary_key_table = dataCon.grade_table()

        for i in datas_student_table:
            student_id_list.append(i[0])

        for i in datas_prof_table:
            professor_id_list.append(i[0])

        for i in datas_course_table:
            course_id_list.append(i[0])

        for i in primary_key_table:
            primary_key_list.append((i[0]+i[1]))
        # ===============================================================================================================
        if (flag):
            if (student_id == "") or () or ():
                messagebox.showerror("ERROR","Please fill all the blanks")
                flag = False
        #===============================================================================================================
        if (flag):
            if (student_id in student_id_list):
                pass
            else:
                messagebox.showerror("ERROR","There is no such a student_id")
                flag = False

        if (flag):
            if (professor_id in professor_id_list):
                pass
            else:
                messagebox.showerror("ERROR", "There is no such a professor_id")
                flag = False

        if (flag):
            if (course_id in course_id_list):
                pass
            else:
                messagebox.showerror("ERROR", "There is no such a course_id")
                flag = False


        #===============================================================================================================
        if (flag):
            if (student_id+course_id) in primary_key_list:
                messagebox.showerror("ERROR","The student_id and course_id are already in the system")
                flag = False
        #===============================================================================================================
        if (self.user == professor_id):
            pass
        else:
            flag = False
            messagebox.showerror("ERROR","You can only update your student information, not for other professors")

        if (flag):
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="")

            query = """INSERT INTO `mydb`.`grade`(Student_Number, Course_ID, Professor_Professor_ID, grade)
                        VALUES (%s, %s,%s, %s)
            """

            val = (student_id, course_id, professor_id, grade)
            cursor = con.cursor()
            cursor.execute(query, val)
            con.commit()
            con.close()
            messagebox.showinfo("Information", "Successfully added")
            self.search_all()

    def prof_surname(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.professor_table()
        for i in datas:
            if i[0] == self.request:
                return i[2]

    def prof_name(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.professor_table()
        for i in datas:
            if i[0] == self.request:
                return i[1]

    def course_name(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.course_table()
        for i in datas:
            if i[0] == self.request:
                return i[1]

    def student_name(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.student_table()
        for i in datas:
            if i[0] == self.request:
                return i[1]

    #******************************************************************************************************************

    def profGradeAction(self):
        self.window.destroy()
        go_main = My_GUI(self.set_host,self.set_user,self.set_password)

class StudentWindow():

    def __init__(self,user,host,set_user,password):
        self.user = user
        self.set_host = host
        self.set_user = set_user
        self.set_password = password


        self.window = tk.Tk()
        self.window.title("Student Grade Database for User: {} - {}".format(self.user, self.student_name(self.user)+" "+self.student_last_name(self.user)))
        self.window.geometry("1530x780+0+0")
        self.window.resizable(0, 0)
        #student action Frame

        self.actionFrame = tk.Frame(self.window,bd =4, relief ="ridge", bg="#ECF0F1")
        self.actionFrame.place(x=20, y=0,width = 1480, height=80)


        #Action Content
        # self.search = tk.Label(self.actionFrame, text="Please enter your name or ID:", font=("consolas", 15, "bold")
        #                          , background="#fefefe", fg="black", relief="groove")
        #
        # self.search.grid(row=0,column=0,pady = 10,padx=20,sticky = "w")
        #**************************************************************************************************************
        self.search_selection = tk.StringVar()

        self.search_by = ttk.Combobox(self.actionFrame, font=("consolas", 16, "bold"),
                                      textvariable=self.search_selection)

        self.search_by['values'] = ('Course_ID')
        self.search_by.grid(row=0, column=0, pady=20, padx=10, sticky="w")

        #**************************************************************************************************************
        self.search_entry = tk.Entry(self.actionFrame, font=("consolas", 15, "bold")
                                 , background="#fefefe", fg="black", relief="groove")

        self.search_entry.grid(row=0,column=1,pady = 10,padx=20,sticky = "w")

        self.searchbtn = tk.Button(self.actionFrame, text="Search", font=("consolas", 15, "bold")
                                 , background="#FCB65E", fg="#fefefe", relief="groove",command = self.searchIT)

        self.searchbtn.grid(row=0,column=2,pady = 10,padx=20,sticky = "w")



        #student Data frame
        self.dataFrame = tk.Frame(self.window, bd=4, relief="ridge", bg="#fefefe")
        self.dataFrame.place(x=20, y=80, width=1480, height=650)

        # Student Table from database
        self.scrollx = tk.Scrollbar(self.dataFrame, orient="horizontal")
        self.scrolly = tk.Scrollbar(self.dataFrame, orient="vertical")

        self.student_grade_table = ttk.Treeview(self.dataFrame, columns=(
            'Student_Number', 'Student_Name', "ProfessorName", 'Course_ID', "Course_Name", 'grade','grade_letter'),
                                                xscrollcommand=self.scrollx.set,
                                                yscrollcommand=self.scrolly.set)
        self.scrollx.pack(side="bottom", fill="x")
        self.scrolly.pack(side="right", fill="y")
        self.scrollx.config(command=self.student_grade_table.xview)
        self.scrolly.config(command=self.student_grade_table.yview)
        self.student_grade_table.heading("Student_Number", text="Student_ID")
        self.student_grade_table.heading('Student_Name', text='Student')
        self.student_grade_table.heading("ProfessorName", text="Professor")
        self.student_grade_table.heading('Course_ID', text='Course_ID')
        self.student_grade_table.heading("Course_Name", text="Course_Name")
        self.student_grade_table.heading('grade', text='Student_Grade')
        self.student_grade_table.heading('grade_letter', text='Grade Letter')

        self.student_grade_table['show'] = 'headings'

        self.student_grade_table.column("Student_Number", width=100)
        self.student_grade_table.column('Student_Name', width=100)
        self.student_grade_table.column("ProfessorName", width=100)
        self.student_grade_table.column('Course_ID', width=100)
        self.student_grade_table.column("Course_Name", width=100)
        self.student_grade_table.column('grade', width=50)
        self.student_grade_table.column('grade_letter', width = 50)
        
        
        self.student_grade_table.pack(fill="both", expand=1)
        # ==============================================================================================================
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.filemenu.add_command(label="Return", command=self.studentAction)
        self.window.config(menu=self.filemenu)
        self.search_all()
        self.window.mainloop()

    def searchIT(self):
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.grade_table()
        input = self.search_entry.get()
        self.student_grade_table.delete(*self.student_grade_table.get_children())
        flag = True
        selection = self.search_selection.get()
        value = self.search_entry.get()

        course_id_list = []
        for data in datas:

            if (data[0] == self.user):
                if(data[1] == input):
                    course_id_list.append(data[1])
                    self.student_grade_table.insert('', 'end', values=(
                                data[0],
                                self.student_name(data[0]) + " " + self.student_last_name(data[0]),
                                self.prof_name(data[2]) + " " + self.prof_surname(data[2]),
                                data[1],
                                self.course_name(data[1]),
                                data[3],
                                self.grade_letter(data[3]))
                                )

        if selection == "":
            messagebox.showerror("ERROR", "Please select search option and enter entry")
            self.search_all()
            flag = False

        if(flag):
            if value in course_id_list:
                pass
            else:
                messagebox.showerror("ERROR","There is no recorded such a Course_Id for your system")
                self.search_selection.set("")
                self.search_all()




    def search_all(self):
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.grade_table()

        self.student_grade_table.delete(*self.student_grade_table.get_children())

        for data in datas:
            if (data[0] == self.user):
                self.student_grade_table.insert('', 'end', values=(
                data[0], self.student_name(data[0]) +" "+self.student_last_name(data[0]),self.prof_name(data[2])+" "+self.prof_surname(data[2]), data[1],
                self.course_name(data[1]), data[3], self.grade_letter(int(data[3]))))

    def prof_name(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.professor_table()
        for i in datas:
            if i[0] == self.request:
                return i[1]

    def prof_surname(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.professor_table()
        for i in datas:
            if i[0] == self.request:
                return i[2]

    def course_name(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.course_table()
        for i in datas:
            if i[0] == self.request:
                return i[1]

    def student_name(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.student_table()
        for i in datas:
            if i[0] == self.request:
                return i[1]

    def student_last_name(self,request):
        self.request = request
        dataCon = database.reach_tables_data(self.set_host,self.set_user,self.set_password)
        datas = dataCon.student_table()
        for i in datas:
            if i[0] == self.request:
                return i[2]

    def grade_letter(self,request):
        
        if (request >= 93):
            return "A+"
        elif (request >=85):
            return "A"
        elif (request >=78):
            return "A-"
        elif (request >=72):
            return "B"
        elif (request >=62):
            return "C"
        elif (request >=50):
            return "D"
        else:
            return "F"
            
    
    def studentAction(self):
            self.window.destroy()
            go = My_GUI(self.set_host,self.set_user,self.set_password)

class database_information:
    def __init__(self):
        self.init_ui()
    
    def init_ui(self):
        self.window = tk.Tk()
        
        # top level frame for explanation
        self.top_frame_label = tk.Frame(self.window)
        self.label = tk.Label(self.top_frame_label, text="SET DATABASE TO CONNECT DATABASE", fg="#FFFFFF", width=50)
        self.label.config(font=("consolas", 20), background="#2C3E50")
        self.label.grid(row=0, column=0)
        self.top_frame_label.grid(row=0, column=0)

        

        # bottom level for password and everything
        self.main_frame = tk.Frame(self.window,bd=4, relief="ridge", background="#2C3E50")
        self.main_frame.place(x=20, y=80, width=710, height=400)


        self.mid_frame = tk.Frame(self.window, bd =4, relief = "ridge", background = "#2C3E50")
        self.mid_frame.place(x=150,y=180, width = "400", height = "250")

        #>>>>Host Information

        self.host_information_label = tk.Label(self.mid_frame,text = "Host",fg ="#FFFFFF")
        self.host_information_label.config(font=("consolas", 16), background="#2C3E50")
        self.host_information_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.host_entry = tk.Entry(self.mid_frame, font=("consolas", 14, "bold"), bd=4, relief="ridge")
        self.host_entry.grid(row=1, column=1, pady=10, padx=20, sticky="w")


        #>>>>> User information

        self.user_information_label = tk.Label(self.mid_frame, text="User", fg="#FFFFFF")
        self.user_information_label.config(font=("consolas", 16), background="#2C3E50")
        self.user_information_label.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.user_entry = tk.Entry(self.mid_frame, font=("consolas", 14, "bold"), bd=4, relief="ridge")
        self.user_entry.grid(row=2, column=1, pady=10, padx=20, sticky="w")

        # >>>> Password Information

        self.password_information_label = tk.Label(self.mid_frame, text="Password", fg="#FFFFFF")
        self.password_information_label.config(font=("consolas", 16), background="#2C3E50")
        self.password_information_label.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        self.password_entry = tk.Entry(self.mid_frame, font=("consolas", 14, "bold"), bd=4, relief="ridge")
        self.password_entry.grid(row=3, column=1, pady=10, padx=20, sticky="w")

        # >>>>Connection Button

        self.connection_button = tk.Button(self.mid_frame, text="CONNECT", fg="#FFFFFF",command = self.action_take)
        self.connection_button.config(font=("consolas", 15), background="#2C3E50")
        self.connection_button.grid(row=4, column=0, padx=(10, 10), pady=(10, 10))

       

        # menu option
        self.menubar = tk.Menu(self.window)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label="Exit", command=self.window.destroy)

        # Main window config and settings
        self.window.config(background="#18BC9C")
        self.window.config(menu=self.filemenu)
        self.window.geometry("750x500+0+0")
        self.window.resizable(0,0)
        self.window.title("Setting Up - Database")
        self.window.mainloop()
        
    def action_take(self):
        try:
            self.host = self.host_entry.get()
            self.user = self.user_entry.get()
            self.passwrd = self.password_entry.get()

            con = mysql.connector.connect(host=self.host,
                            user = self.user,
                            passwd = self.passwrd)
            cursor = con.cursor()

            query = "show schemas"
            cursor.execute(query)
            rows = cursor.fetchall()

            con.commit()
            con.close()
            
            messagebox.showinfo("CONNECTED", "You have connected to the system, successfully, Datas in the System are Random")
            
            self.start_app()
        except:
            messagebox.showerror("ERROR","Connection Informations are wrong please try again")

    
    
    def start_app(self):
        self.window.destroy()
        go = My_GUI(self.host,self.user,self.passwrd)


if __name__ == '__main__':
    go = database_information()

















