import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from openpyxl import Workbook
from tkinter import filedialog, messagebox


# ================= Placeholder Entry =================
class PlaceholderEntry(tk.Entry):
    def __init__(self, master, placeholder="", color="grey", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg = self["fg"]

        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)

        self.bind("<FocusIn>", self._clear)
        self.bind("<FocusOut>", self._add)

    def _clear(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self.config(fg=self.default_fg)

    def _add(self, event):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)

# ================= Main Class =================
class std():
    def __init__(self,root):
        self.root = root
        self.root.title("Student Management System")
        self.root.configure(bg='#CFFFE2')

        # Screen => width and height
        self.root.width = self.root.winfo_screenwidth()
        self.root.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.root.width}x{self.root.height}")

        # Heading
        titleLable = tk.Label(self.root, text="--- School Management System ---", font=('Ariel',20,'bold','italic'), relief='groove')
        titleLable.pack(side='top',fill='x')

# ===================== Left Side =====================
        # Left Dashboard / Put image in a Label
        photo = tk.PhotoImage(file="assets/images/school.png")
        rgframe = tk.Frame(self.root,bg="white", relief='ridge')
        rgframe.place(width=self.root.width/4, height=self.root.height/6,y=38)
        img_label = tk.Label(rgframe, image=photo, bg='white')
        img_label.image = photo
        img_label.pack(expand=True)

        # Check Frame
        self.checkFun()
    def checkFun(self):
        self.checkFrame = tk.Frame(self.root, bg='black', relief='ridge')
        self.checkFrame.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)

        regBtn = tk.Button(self.checkFrame, command=self.new_regFun, text="New Register", width=25,font=('Arial', 14, 'bold'))
        regBtn.pack(expand=True)

        techerBtn = tk.Button(self.checkFrame, command=self.teacherFun, text="Teachers", width=25,font=('Arial', 14, 'bold'))
        techerBtn.pack(expand=True)

        studentsBtn = tk.Button(self.checkFrame, command=self.studFun, text="Students", width=25,font=('Arial', 14, 'bold'))
        studentsBtn.pack(expand=True)

        classBtn = tk.Button(self.checkFrame, command=self.classFun, text="Classes", width=25,font=('Arial', 14, 'bold'))
        classBtn.pack(expand=True)

        timeBtn = tk.Button(self.checkFrame, text="Time Tables", width=25,font=('Arial', 14, 'bold'))
        timeBtn.pack(expand=True)

        resultBtn = tk.Button(self.checkFrame, text="Exam Result", width=25,font=('Arial', 14, 'bold'))
        resultBtn.pack(expand=True)

# ===================== Right Side =====================
        # Right Heading
        self.rgFrame = tk.Frame(self.root, bg='white', relief='ridge')
        self.rgFrame.place(width=self.root.width/1.34, height=self.root.height/6, x=self.root.width/4, y=38)

        teachertotal = tk.Frame(self.rgFrame,bg="white",relief='ridge',bd=1)
        teachertotal.place(relx=0, rely=0, relwidth=1/3, relheight=1)
        teachtot= tk.Label(teachertotal, text="Total Teacher :", bg="white", font=('Arial', 14, 'bold'))
        teachtot.grid(row=0,column=0,padx=10,pady=10)
        totalteac = tk.Label(teachertotal, text="0", bg="white", font=('Arial', 18, 'bold'))
        totalteac.grid(row=1,column=0,padx=100,pady=20,columnspan=2,rowspan=2)

        studtotal = tk.Frame(self.rgFrame,bg="white",relief='ridge',bd=1)
        studtotal.place(relx=1/3, rely=0, relwidth=1/3, relheight=1)
        studtot = tk.Label(studtotal, text="Total Students :", bg="white", font=('Arial', 14, 'bold'))
        studtot.grid(row=0,column=0,padx=10,pady=10)
        self.totalstud = tk.Label(studtotal,text="0",bg="white",font=('Arial', 18, 'bold'))
        self.totalstud.grid(row=1, column=0, padx=100, pady=20, columnspan=2, rowspan=2)

        classTotal = tk.Frame(self.rgFrame,bg="white",relief='ridge',bd=1)
        classTotal.place(relx=2/3, rely=0, relwidth=1/3, relheight=1)
        classtot = tk.Label(classTotal, text="Total Classes :", bg="white", font=('Arial', 14, 'bold'))
        classtot.grid(row=0,column=0,padx=10,pady=10)
        totalclass = tk.Label(classTotal, text="0", bg="white", font=('Arial', 18, 'bold'))
        totalclass.grid(row=1,column=0,padx=100,pady=20,columnspan=2,rowspan=2)

# ===================== Functions =====================
    # Data Table Function
    # Student Table
    def stud_tabFun(self):
        studTabFrame = tk.Frame(self.root, bg='black', relief='ridge')
        studTabFrame.place(width=self.root.width/1.34, height = self.root.height/1.45, x=self.root.width/4, y = self.root.height/6+38)

        x_scrol = tk.Scrollbar(studTabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(studTabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(studTabFrame,columns=("Roll No.","Name","Age","Class","Grade","Father Name","Contact Info"),xscrollcommand=x_scrol.set,yscrollcommand=y_scrol.set)
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("Roll No.", text="Roll No.")
        self.table.heading("Name", text="Name")
        self.table.heading("Age", text="Age")
        self.table.heading("Class", text="Class")
        self.table.heading("Grade", text="Grade")
        self.table.heading("Father Name", text="Father Name")
        self.table.heading("Contact Info", text="Contact Info")

        self.table["show"]="headings"

        self.table.column("Roll No.",width=120)
        self.table.column("Name",width=120)
        self.table.column("Age",width=120)
        self.table.column("Class",width=120)
        self.table.column("Grade",width=120)
        self.table.column("Father Name",width=120)
        self.table.column("Contact Info",width=240)

        self.table.pack(fill="both", expand=1)
    
    # Teacher Table Function
    def tec_tabFun(self):
        tecTabFrame = tk.Frame(self.root, bg='black', relief='ridge')
        tecTabFrame.place(width=self.root.width/1.34, height = self.root.height/1.45, x=self.root.width/4, y = self.root.height/6+38)

        x_scrol = tk.Scrollbar(tecTabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tecTabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tecTabFrame,columns=("Name","Age","Class","Experience","Contact Info"),xscrollcommand=x_scrol.set,yscrollcommand=y_scrol.set)
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("Name", text="Name")
        self.table.heading("Age", text="Age")
        self.table.heading("Class", text="Class")
        self.table.heading("Experience", text="Experience")
        self.table.heading("Contact Info", text="Contact Info")

        self.table["show"]="headings"

        self.table.column("Name",width=120)
        self.table.column("Age",width=120)
        self.table.column("Class",width=120)
        self.table.column("Experience",width=120)
        self.table.column("Contact Info",width=240)

        self.table.pack(fill="both", expand=1)

    def score_Frame(self):
        score_Frame = tk.Frame(self.root, bg='black', relief='ridge')
        score_Frame.place(width=self.root.width/1.34, height = self.root.height/1.45, x=self.root.width/4, y = self.root.height/6+38)

        x_scrol = tk.Scrollbar(score_Frame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(score_Frame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(score_Frame,columns=("Roll No.","Myanmar","English","Mathematics","Geology","History","Science"),xscrollcommand=x_scrol.set,yscrollcommand=y_scrol.set)
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("Roll No.", text="Roll No.")
        self.table.heading("Myanmar", text="Myanmar")
        self.table.heading("English", text="English")
        self.table.heading("Mathematics", text="Mathematics")
        self.table.heading("Geology", text="Geology")
        self.table.heading("History", text="History")
        self.table.heading("Science", text="Science")

        self.table["show"]="headings"

        self.table.column("Roll No.",width=120)
        self.table.column("Myanmar",width=120)
        self.table.column("English",width=120)
        self.table.column("Mathematics",width=120)
        self.table.column("Geology",width=120)
        self.table.column("History",width=120)
        self.table.column("Science",width=120)

        self.table.pack(fill="both", expand=1)
    
    def all_score_Frame(self):
        all_score_Frame = tk.Frame(self.root, bg='black', relief='ridge')
        all_score_Frame.place(width=self.root.width/1.34, height = self.root.height/1.45, x=self.root.width/4, y = self.root.height/6+38)

        x_scrol = tk.Scrollbar(all_score_Frame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(all_score_Frame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(all_score_Frame,columns=("Roll No.","Name","Myanmar","English","Mathematics","Geology","History","Science"),xscrollcommand=x_scrol.set,yscrollcommand=y_scrol.set)
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)

        self.table.heading("Roll No.", text="Roll No.")
        self.table.heading("Name", text="Name")
        self.table.heading("Myanmar", text="Myanmar")
        self.table.heading("English", text="English")
        self.table.heading("Mathematics", text="Mathematics")
        self.table.heading("Geology", text="Geology")
        self.table.heading("History", text="History")
        self.table.heading("Science", text="Science")

        self.table["show"]="headings"

        self.table.column("Roll No.",width=120)
        self.table.column("Name",width=120)
        self.table.column("Myanmar",width=120)
        self.table.column("English",width=120)
        self.table.column("Mathematics",width=120)
        self.table.column("Geology",width=120)
        self.table.column("History",width=120)
        self.table.column("Science",width=120)

        self.table.pack(fill="both", expand=1)
# ====================================================================================
    # For new register Button
    def new_regFun(self):
        self.newregFrame = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        self.newregFrame.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)

        studBtn = tk.Button(self.newregFrame, command=self.stud_regFun, text="New Student", width=25,font=('Arial', 14, 'bold'))
        studBtn.pack(expand=True)

        techBtn = tk.Button(self.newregFrame, command=self.tech_regFun, text="New Teacher", width=25,font=('Arial', 14, 'bold'))
        techBtn.pack(expand=True)

        scoreBtn = tk.Button(self.newregFrame, command=self.score_regFun,text="Monthly Score", width=25,font=('Arial', 14, 'bold'))
        scoreBtn.pack(expand=True)

        menuBtn = tk.Button(self.newregFrame, command=self.checkFun, text="Back to Menu", width=25,font=('Arial', 14, 'bold'))
        menuBtn.pack(expand=True)

    def stud_regFun(self):
        form = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        form.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)
        
        self.rolnoin = PlaceholderEntry(form, "Enter Roll No", width=30, font=('Arial', 15))
        self.namein = PlaceholderEntry(form, "Enter Name", width=30, font=('Arial', 15))
        self.agein = PlaceholderEntry(form, "Enter Age", width=30, font=('Arial', 15))
        self.classin = PlaceholderEntry(form, "Enter Class", width=30, font=('Arial', 15))
        self.gradein = PlaceholderEntry(form, "Enter Grade",width=30, font=('Arial', 15))
        self.fnamein = PlaceholderEntry(form, "Enter Father Name", width=30, font=('Arial', 15))
        self.cinfoin = PlaceholderEntry(form, "Enter Contact Info", width=30, font=('Arial', 15))

        entries = [self.rolnoin, self.namein, self.agein, self.classin,self.gradein,self.fnamein, self.cinfoin]

        for i, e in enumerate(entries):
            e.grid(row=i, column=0, padx=15, pady=15)

        stud_regBtn = tk.Button(form, command=self.insertFun, text="Register", width=30,font=('Arial', 14, 'bold'))
        stud_regBtn.grid(row=8, column=0, pady=20)

        menuBtn = tk.Button(form, command=self.checkFun,text="Back to Menu", width=30,font=('Arial', 14, 'bold'))
        menuBtn.grid(row=9, column=0, pady=20)

    def tech_regFun(self):
        tecform = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        tecform.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)
        
        self.tecnamein = PlaceholderEntry(tecform, "Enter Teacher Name", width=30, font=('Arial', 15))
        self.tecagein = PlaceholderEntry(tecform, "Enter Teacher Age", width=30, font=('Arial', 15))
        self.tecclassin = PlaceholderEntry(tecform, "Enter The Class", width=30, font=('Arial', 15))
        self.expin = PlaceholderEntry(tecform, "Enter Experience", width=30, font=('Arial', 15))
        self.teccinfoin = PlaceholderEntry(tecform, "Enter Contact Info", width=30, font=('Arial', 15))

        entries = [self.tecnamein, self.tecagein, self.tecclassin, self.expin, self.teccinfoin]

        for i, e in enumerate(entries):
            e.grid(row=i, column=0, padx=15, pady=15)

        tecregBtn = tk.Button(tecform, command=self.tec_insert_Fun, text="Register", width=30,font=('Arial', 14, 'bold'))
        tecregBtn.grid(row=8, column=0, pady=20)

        menuBtn = tk.Button(tecform, command=self.checkFun,text="Back to Menu", width=30,font=('Arial', 14, 'bold'))
        menuBtn.grid(row=9, column=0, pady=20)

    def score_regFun(self):
        scrform = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        scrform.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)
        
        self.rollin = PlaceholderEntry(scrform, "Enter Roll No.", width=30, font=('Arial', 15))
        self.myain = PlaceholderEntry(scrform, "Myanmar", width=30, font=('Arial', 15))
        self.engin = PlaceholderEntry(scrform, "English", width=30, font=('Arial', 15))
        self.mathin = PlaceholderEntry(scrform, "Mathematics", width=30, font=('Arial', 15))
        self.geoin = PlaceholderEntry(scrform, "Geology", width=30, font=('Arial', 15))
        self.histin = PlaceholderEntry(scrform, "History", width=30, font=('Arial', 15))
        self.sciin = PlaceholderEntry(scrform, "Science", width=30, font=('Arial', 15))

        scoreentries = [self.rollin, self.myain, self.engin, self.mathin, self.geoin, self.histin, self.sciin]

        for i, e in enumerate(scoreentries):
            e.grid(row=i, column=0, padx=15, pady=15)

        scrregBtn = tk.Button(scrform, command=self.scr_insert_Fun, text="Register", width=30,font=('Arial', 14, 'bold'))
        scrregBtn.grid(row=8, column=0, pady=20)

        menuBtn = tk.Button(scrform, command=self.checkFun,text="Back to Menu", width=30,font=('Arial', 14, 'bold'))
        menuBtn.grid(row=9, column=0, pady=20)
# ====================================================================================
    # For Teacher Button
    def teacherFun(self):
        teacherFrame = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        teacherFrame.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)

        self.tecvaluein = PlaceholderEntry(teacherFrame, "Enter value", width=30, font=('Arial', 15))

        tecentries = [self.tecvaluein]

        for i, e in enumerate(tecentries):
            e.grid(row=i, column=0, padx=15, pady=15)

        self.tecoptions = ttk.Combobox(teacherFrame, width=28, font=('Arial', 15), values=("Name","Class","Age","All"))
        self.tecoptions.set("Select one")
        self.tecoptions.grid(row=3, column=0, pady=20)

        searchBtn = tk.Button(teacherFrame, command=self.tec_searchFun, text="Search", width=30,font=('Arial', 14, 'bold'))
        searchBtn.grid(row=5, column=0, pady=20)

        updateBtn = tk.Button(teacherFrame, command=self.tecupdFrame_Fun, text="Update", width=30,font=('Arial', 14, 'bold'))
        updateBtn.grid(row=7, column=0, pady=20)

        delBtn = tk.Button(teacherFrame, command=self.tec_delFun, text="Delete", width=30,font=('Arial', 14, 'bold'))
        delBtn.grid(row=9, column=0, pady=20)

        expoBtn = tk.Button(teacherFrame, command=self.export_teacher_to_excel, text="Export", width=30,font=('Arial', 14, 'bold'))
        expoBtn.grid(row=10, column=0, pady=20)

        menuBtn = tk.Button(teacherFrame, command=self.checkFun, text="Back to Menu", width=30,font=('Arial', 14, 'bold'))
        menuBtn.grid(row=11, column=0, pady=20)
# ==================================================================================== For Teacher
    # Teacher Insert Function
    def tec_insert_Fun(self):
        tecName = self.tecnamein.get()
        tecAge = self.tecagein.get()
        tecClass = self.tecclassin.get()
        tecExp = self.expin.get()
        tecCinfo = self.teccinfoin.get()

        if tecName and tecAge and tecClass and tecExp and tecCinfo:
            try:
                self.dbfun()
                self.cur.execute("insert into teacher(name,age,class,exp,contact) values(%s,%s,%s,%s,%s)",(tecName,tecAge,tecClass,tecExp,tecCinfo))
                self.conn.commit()
                tk.messagebox.showinfo("Success",f"Teacher : {tecName} is registered successfully.")

                self.tec_tabFun()
                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from teacher where name=%s",(tecName))
                row = self.cur.fetchone()
                self.table.insert('',tk.END,values=row)
                self.conn.close()
                self.tecnamein.delete(0,tk.END)
                self.tecagein.delete(0,tk.END)
                self.tecclassin.delete(0,tk.END)
                self.expin.delete(0,tk.END)
                self.teccinfoin.delete(0,tk.END)
                self.tec_insert_Fun.destroy()
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields.")

    # Teacher Search Function
    def tec_searchFun(self):
        val1 = self.tecoptions.get()
        val2 = self.tecvaluein.get()
        if val1 == "Name":
            try:
                self.dbfun()
                self.cur.execute("select * from teacher where name=%s",val2)
                data = self.cur.fetchall()
                if data:
                    self.tec_tabFun()
                    self.table.delete(*self.table.get_children())
                    for i in data:
                        self.table.insert('',tk.END,values=i)
                    self.conn.close()
                else:
                    tk.messagebox.showerror("Error","No teacher exists with this name.")
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        elif val1 == "Class":
            try:
                self.dbfun()
                self.cur.execute("select * from teacher where class=%s",val2)
                data = self.cur.fetchall()
                if data:
                    self.tec_tabFun()
                    self.table.delete(*self.table.get_children())
                    for j in data:
                        self.table.insert('',tk.END,values=j)
                    self.conn.close()
                else:
                    tk.messagebox.showerror("Error",f"There's no teacher is teaching in {val2}.")
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        elif val1 == "Age":
            val2_int=int(val2)
            try:
                self.dbfun()
                self.cur.execute("select * from teacher where age=%s",val2_int)
                data = self.cur.fetchall()
                if data:
                    self.tec_tabFun()
                    self.table.delete(*self.table.get_children())
                    for k in data:
                        self.table.insert('',tk.END,values=k)
                    self.conn.close()
                else:
                    tk.messagebox.showerror("Error",f"There no teacher with age {val2_int}.")
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        elif val1 == "All":
            try:
                self.dbfun()
                self.cur.execute("select * from teacher")
                data = self.cur.fetchall()
                if data:
                    self.tec_tabFun()
                    self.table.delete(*self.table.get_children())
                    for l in data:
                        self.table.insert('',tk.END,values=l)
                    self.conn.close()
                else:
                    tk.messagebox.showerror("Error","No data exits.")
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")

    # Teacher Update Function
    def tecupdFrame_Fun(self):
        self.tecupdFrame = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        self.tecupdFrame.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)

        self.tecupdvaluein = PlaceholderEntry(self.tecupdFrame, "Enter value", width=30, font=('Arial', 15))

        tecupdentries = [self.tecupdvaluein]

        for i, e in enumerate(tecupdentries):
            e.grid(row=i, column=0, padx=15, pady=15)

        self.tecupdOptions = ttk.Combobox(self.tecupdFrame, width=28, font=('Arial', 15), values=("Name","Age","Class","Experience","Contact Info"))
        self.tecupdOptions.set("Select one")
        self.tecupdOptions.grid(row=3, column=0, pady=20)

        okBtn = tk.Button(self.tecupdFrame, command=self.tecupdFun, text="Ok", width=25,font=('Arial', 14, 'bold'))
        okBtn.grid(row=5, column=0, pady=20)

        menuBtn = tk.Button(self.tecupdFrame, command=self.teacherFun, text="Back", width=25,font=('Arial', 14, 'bold'))
        menuBtn.grid(row=7, column=0, pady=20)
    
    def tecupdFun(self):
        val1 = self.tecoptions.get()
        val2 = self.tecvaluein.get()
        tec_val1 = self.tecupdOptions.get()
        tec_val2 = self.tecupdvaluein.get()
        if val1 == "Name":
            if tec_val1 == "Name":
                try:
                    self.dbfun()
                    self.cur.execute("update teacher set name=%s where name=%s",(tec_val2,val2))
                    self.conn.commit()
                    self.cur.execute("select * from teacher where name=%s",tec_val2)
                    data = self.cur.fetchall()
                    if data:
                        tk.messagebox.showinfo("Success","Teacher's data updated successfully!")
                        self.tec_tabFun()
                        self.table.delete(*self.table.get_children())
                        for i in data:
                            self.table.insert('',tk.END,values=i)
                            self.conn.close()
                            self.tecupdFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No teacher exists with this name.")
                        self.tecupdFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.tecupdFrame.destroy()
            elif tec_val1 == "Class":
                try:
                    self.dbfun()
                    self.cur.execute("update teacher set class=%s where name=%s",(tec_val2,val2))
                    self.conn.commit()
                    self.cur.execute("select * from teacher where name=%s",val2)
                    data = self.cur.fetchall()
                    if data:
                        tk.messagebox.showinfo("Success","Teacher's data updated successfully!")
                        self.tec_tabFun()
                        self.table.delete(*self.table.get_children())
                        for i in data:
                            self.table.insert('',tk.END,values=i)
                            self.conn.close()
                            self.tecupdFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No teacher exists with this name.")
                        self.tecupdFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.tecupdFrame.destroy()
            elif tec_val1 == "Experience":
                try:
                    self.dbfun()
                    self.cur.execute("update teacher set exp=%s where name=%s",(tec_val2,val2))
                    self.conn.commit()
                    self.cur.execute("select * from teacher where name=%s",val2)
                    data = self.cur.fetchall()
                    if data:
                        tk.messagebox.showinfo("Success","Teacher's data updated successfully!")
                        self.tec_tabFun()
                        self.table.delete(*self.table.get_children())
                        for i in data:
                            self.table.insert('',tk.END,values=i)
                            self.conn.close()
                            self.tecupdFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No teacher exists with this name.")
                        self.tecupdFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.tecupdFrame.destroy()
            elif tec_val1 == "Contact Info":
                try:
                    self.dbfun()
                    self.cur.execute("update teacher set contact=%s where name=%s",(tec_val2,val2))
                    self.conn.commit()
                    self.cur.execute("select * from teacher where name=%s",val2)
                    data = self.cur.fetchall()
                    if data:
                        tk.messagebox.showinfo("Success","Teacher's data updated successfully!")
                        self.tec_tabFun()
                        self.table.delete(*self.table.get_children())
                        for i in data:
                            self.table.insert('',tk.END,values=i)
                            self.conn.close()
                            self.tecupdFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No teacher exists with this name.")
                        self.tecupdFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.tecupdFrame.destroy()
            elif tec_val1 == "Age":
                tec_val2_int = int(tec_val2)
                try:
                    self.dbfun()
                    self.cur.execute("update teacher set age=%s where name=%s",(tec_val2_int,val2))
                    self.conn.commit()
                    self.cur.execute("select * from teacher where name=%s",val2)
                    row = self.cur.fetchone()
                    if row:
                        tk.messagebox.showinfo("Success","Teacher's data updated successfully!")
                        self.tec_tabFun()
                        self.table.delete(*self.table.get_children())
                        self.table.insert('',tk.END,values=row)
                        self.conn.close()
                        self.tecupdFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No student exits with this roll number.")
                        self.tecupdFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
        else:
                tk.messagebox.showerror("Error","Select only Name")
                self.updFrame.destroy()
    # Teacher Delete Function
    def tec_delFun(self):
        val1 = self.tecoptions.get()
        val2 = self.tecvaluein.get()
        if val1 == "Name":
            try:
                self.dbfun()
                self.cur.execute("delete from teacher where name=%s",val2)
                self.conn.commit()
                tk.messagebox.showinfo("Success",f"Data of teacher: {val2} is removed.")
                self.conn.close()
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        else:
                tk.messagebox.showerror("Error","Select only Name")
                self.updFrame.destroy()

    # Teacher Export Function
    def export_teacher_to_excel(self):
    # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not file_path:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Teacher"

        # --- Column headings (same as Treeview) ---
        columns = ("Name", "Age", "Class", "Experience", "Contact Info")
        ws.append(columns)

        # --- Insert Treeview data ---
        for row_id in self.table.get_children():
            row = self.table.item(row_id)["values"]
            ws.append(row)

        wb.save(file_path)
        messagebox.showinfo("Success", "Data exported to Excel successfully!")
# ====================================================================================
    # For Student Button
    def studFun(self):
        studFrame = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        studFrame.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)

        self.valuein = PlaceholderEntry(studFrame, "Enter value", width=30, font=('Arial', 15))

        entries = [self.valuein]

        for i, e in enumerate(entries):
            e.grid(row=i, column=0, padx=15, pady=15)

        self.options = ttk.Combobox(studFrame, width=28, font=('Arial', 15), values=("Roll No.","Name","Class","All"))
        self.options.set("Select one")
        self.options.grid(row=3, column=0, pady=20)

        searchBtn = tk.Button(studFrame, command=self.searchFun, text="Search", width=30,font=('Arial', 14, 'bold'))
        searchBtn.grid(row=5, column=0, pady=20)

        updateBtn = tk.Button(studFrame, command=self.updFrame_Fun, text="Update", width=30,font=('Arial', 14, 'bold'))
        updateBtn.grid(row=7, column=0, pady=20)

        delBtn = tk.Button(studFrame, command=self.delFun, text="Delete", width=30,font=('Arial', 14, 'bold'))
        delBtn.grid(row=9, column=0, pady=20)

        expoBtn = tk.Button(studFrame,command=lambda: self.export_students_to_excel(), text="Export", width=30,font=('Arial', 14, 'bold'))
        expoBtn.grid(row=10, column=0, pady=20)

        menuBtn = tk.Button(studFrame, command=self.checkFun, text="Back to Menu", width=30,font=('Arial', 14, 'bold'))
        menuBtn.grid(row=11, column=0, pady=20)
# ==================================================================================== For Students
    # Insert Function
    def insertFun(self):
        rolno = int(self.rolnoin.get())
        name = self.namein.get()
        age = int(self.agein.get())
        clas = self.classin.get()
        grade = self.gradein.get()
        fname = self.fnamein.get()
        cinfo = self.cinfoin.get()

        if rolno and name and age and clas and grade and fname and cinfo:
            try:
                self.dbfun()
                self.cur.execute("insert into student(rollno,name,age,class,grade,fathername,contact) values(%s,%s,%s,%s,%s,%s,%s)",(rolno,name,age,clas,grade,fname,cinfo))
                self.conn.commit()
                tk.messagebox.showinfo("Success",f"Student : {name} is registered successfully.")

                self.stud_tabFun()
                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from student where rollno=%s",(rolno))
                row = self.cur.fetchone()
                self.table.insert('',tk.END,values=row)
                self.conn.close()
                self.rolnoin.delete(0,tk.END)
                self.namein.delete(0,tk.END)
                self.agein.delete(0,tk.END)
                self.classin.delete(0,tk.END)
                self.gradein.delete(0,tk.END)
                self.fnamein.delete(0,tk.END)
                self.cinfoin.delete(0,tk.END)
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields.")

    # Search Function
    def searchFun(self):
        val1 = self.options.get()
        val2 = self.valuein.get()
        if val1 == "Roll No.":
            val2_int = int(val2)
            try:
                self.dbfun()
                self.cur.execute("select * from student where rollno=%s order by rollno",val2_int)
                row = self.cur.fetchone()
                if row:
                    self.stud_tabFun()
                    self.table.delete(*self.table.get_children())
                    self.table.insert('',tk.END,values=row)
                    self.conn.close()
                else:
                    tk.messagebox.showerror("Error","No student exits with this roll number.")
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        elif val1 == "Name":
            try:
                self.dbfun()
                self.cur.execute("select * from student where name=%s order by rollno",val2)
                data = self.cur.fetchall()
                if data:
                    self.stud_tabFun()
                    self.table.delete(*self.table.get_children())
                    for i in data:
                        self.table.insert('',tk.END,values=i)
                    self.conn.close()
                else:
                    tk.messagebox.showerror("Error","No student exists with this name.")
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        elif val1 == "Class":
            try:
                self.dbfun()
                self.cur.execute("select * from student where class=%s order by rollno",val2)
                data = self.cur.fetchall()
                if data:
                    self.stud_tabFun()
                    self.table.delete(*self.table.get_children())
                    for j in data:
                        self.table.insert('',tk.END,values=j)
                    self.conn.close()
                else:
                    tk.messagebox.showerror("Error",f"No student attanded in {val2}.")
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        elif val1 == "All":
            try:
                self.dbfun()
                self.cur.execute("select * from student")
                data = self.cur.fetchall()
                if data:
                    self.stud_tabFun()
                    self.table.delete(*self.table.get_children())
                    for j in data:
                        self.table.insert('',tk.END,values=j)
                    self.conn.close()
                else:
                    tk.messagebox.showerror("Error","No data exits.")
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")

    # Update Function
    def updFrame_Fun(self):
        self.updFrame = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        self.updFrame.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)

        self.updvaluein = PlaceholderEntry(self.updFrame, "Enter value", width=30, font=('Arial', 15))

        updentries = [self.updvaluein]

        for i, e in enumerate(updentries):
            e.grid(row=i, column=0, padx=15, pady=15)

        self.updOptions = ttk.Combobox(self.updFrame, width=28, font=('Arial', 15), values=("Roll No.","Name","Class","Grade","Father Name","Contact Info"))
        self.updOptions.set("Select one")
        self.updOptions.grid(row=3, column=0, pady=20)

        okBtn = tk.Button(self.updFrame, command=self.updFun, text="Ok", width=25,font=('Arial', 14, 'bold'))
        okBtn.grid(row=5, column=0, pady=20)

        menuBtn = tk.Button(self.updFrame, command=self.studFun, text="Back", width=25,font=('Arial', 14, 'bold'))
        menuBtn.grid(row=7, column=0, pady=20)

    def updFun(self):
        val1 = self.options.get()
        val2 = self.valuein.get()
        new_val1 = self.updOptions.get()
        new_val2 = self.updvaluein.get()
        if val1 == "Roll No.":
            val2_int = int(val2)
            if new_val1 == "Roll No.":
                new_val2_int = int(new_val2)
                try:
                    self.dbfun()
                    self.cur.execute("update student set rollno=%s where rollno=%s",(new_val2_int,val2_int))
                    self.conn.commit()
                    self.cur.execute("select * from student where rollno=%s",new_val2_int)
                    row = self.cur.fetchone()
                    if row:
                        tk.messagebox.showinfo("Success","Student updated successfully!")
                        self.stud_tabFun()
                        self.table.delete(*self.table.get_children())
                        self.table.insert('',tk.END,values=row)
                        self.conn.close()
                        self.updFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No student exits with this roll number.")
                        self.updFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
            elif new_val1 == "Name":
                try:
                    self.dbfun()
                    self.cur.execute("update student set name=%s where rollno=%s",(new_val2,val2_int))
                    self.conn.commit()
                    self.cur.execute("select * from student where name=%s",new_val2)
                    data = self.cur.fetchall()
                    if data:
                        self.stud_tabFun()
                        self.table.delete(*self.table.get_children())
                        for i in data:
                            self.table.insert('',tk.END,values=i)
                        self.conn.close()
                        self.updFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No student exists with this name.")
                        self.updFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.updFrame.destroy()
            elif new_val1 == "Class":
                try:
                    self.dbfun()
                    self.cur.execute("update student set class=%s where rollno=%s",(new_val2,val2_int))
                    self.conn.commit()
                    self.cur.execute("select * from student where class=%s",new_val2)
                    data = self.cur.fetchall()
                    if data:
                        self.stud_tabFun()
                        self.table.delete(*self.table.get_children())
                        for j in data:
                            self.table.insert('',tk.END,values=j)
                        self.conn.close()
                        self.updFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No student exists with this name.")
                        self.updFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.updFrame.destroy()
            elif new_val1 == "Grade":
                try:
                    self.dbfun()
                    self.cur.execute("update student set grade=%s where rollno=%s",(new_val2,val2_int))
                    self.conn.commit()
                    self.cur.execute("select * from student where grade=%s",new_val2)
                    data = self.cur.fetchall()
                    if data:
                        self.stud_tabFun()
                        self.table.delete(*self.table.get_children())
                        for k in data:
                            self.table.insert('',tk.END,values=k)
                        self.conn.close()
                        self.updFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No student exists with this name.")
                        self.updFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.updFrame.destroy()
            elif new_val1 == "Father Name":
                try:
                    self.dbfun()
                    self.cur.execute("update student set fathername=%s where rollno=%s",(new_val2,val2_int))
                    self.conn.commit()
                    self.cur.execute("select * from student where fathername=%s",new_val2)
                    data = self.cur.fetchall()
                    if data:
                        self.stud_tabFun()
                        self.table.delete(*self.table.get_children())
                        for j in data:
                            self.table.insert('',tk.END,values=j)
                        self.conn.close()
                        self.updFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No student exists with this name.")
                        self.updFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.updFrame.destroy()
            elif new_val1 == "Contact Info":
                try:
                    self.dbfun()
                    self.cur.execute("update student set contact=%s where rollno=%s",(new_val2,val2_int))
                    self.conn.commit()
                    self.cur.execute("select * from student where contact=%s",new_val2)
                    data = self.cur.fetchall()
                    if data:
                        self.stud_tabFun()
                        self.table.delete(*self.table.get_children())
                        for j in data:
                            self.table.insert('',tk.END,values=j)
                        self.conn.close()
                        self.updFrame.destroy()
                    else:
                        tk.messagebox.showerror("Error","No student exists with this name.")
                        self.updFrame.destroy()
                except Exception as e:
                    tk.messagebox.showerror("Error",f"Error : {e}")
                    self.updFrame.destroy()
            else:
                tk.messagebox.showerror("Error",f"Please Enter valid Value.")
                self.updFrame.destroy()
        else:
                tk.messagebox.showerror("Error","Select only Roll No.")
                self.updFrame.destroy()

    # Delete Function
    def delFun(self):
        val1 = self.options.get()
        val2 = self.valuein.get()
        if val1 == "Roll No.":
            val2_int = int(val2)
            try:
                self.dbfun()
                self.cur.execute("delete from student where rollno=%s",val2_int)
                self.conn.commit()
                tk.messagebox.showinfo("Success",f"Data of student: {val2_int} is removed.")
                self.conn.close()
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        elif val1 == "Name":
            try:
                self.dbfun()
                self.cur.execute("delete from student where name=%s",val2)
                self.conn.commit()
                tk.messagebox.showinfo("Success",f"Data of student: {val2} is removed.")
                self.conn.close()
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")

    # Export Function
    def export_students_to_excel(self):
    # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not file_path:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Students"

        # --- Column headings (same as Treeview) ---
        columns = ("Roll No.", "Name", "Age", "Class", "Grade", "Father Name", "Contact Info")
        ws.append(columns)

        # --- Insert Treeview data ---
        for row_id in self.table.get_children():
            row = self.table.item(row_id)["values"]
            ws.append(row)

        wb.save(file_path)
        messagebox.showinfo("Success", "Data exported to Excel successfully!")
# ====================================================================================
    # For Class Button
    def classFun(self):
        classFrame = tk.Frame(self.root, bg='black', bd=4, relief='ridge')
        classFrame.place(width=self.root.width/4 , height = self.root.height/1.45, y =185)

        classABtn = tk.Button(classFrame, command=self.classA_button, text="Class A", width=25,font=('Arial', 14, 'bold'))
        classABtn.pack(expand=True)

        classBBtn = tk.Button(classFrame, command=self.classB_button, text="Class B", width=25,font=('Arial', 14, 'bold'))
        classBBtn.pack(expand=True)

        classCBtn = tk.Button(classFrame, command=self.classC_button,text="Class C", width=25,font=('Arial', 14, 'bold'))
        classCBtn.pack(expand=True)

        scrBtn = tk.Button(classFrame, command=self.scr_button, text="Scoreboard", width=25,font=('Arial', 14, 'bold'))
        scrBtn.pack(expand=True)

        menuBtn = tk.Button(classFrame, command=self.checkFun, text="Back to Main Menu", width=25,font=('Arial', 14, 'bold'))
        menuBtn.pack(expand=True)
# ==================================================================================== For Class Button
    def scr_insert_Fun(self):
        rollno = int(self.rollin.get())
        mya = int(self.myain.get())
        eng = int(self.engin.get())
        maths = int(self.mathin.get())
        geo = int(self.geoin.get())
        hist = int(self.histin.get())
        sci = int(self.sciin.get())

        if rollno and mya and eng and maths and geo and hist and sci:
            try:
                self.dbfun()
                self.cur.execute("insert into score(rollno,mya,eng,math,geo,hist,sci) values(%s,%s,%s,%s,%s,%s,%s)",(rollno,mya,eng,maths,geo,hist,sci))
                self.conn.commit()
                tk.messagebox.showinfo("Success",f"Roll No. {rollno} score is registered successfully.")

                self.score_Frame()
                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from score where rollno=%s",(rollno))
                row = self.cur.fetchone()
                self.table.insert('',tk.END,values=row)
                self.conn.close()
                self.rollin.delete(0,tk.END)
                self.myain.delete(0,tk.END)
                self.engin.delete(0,tk.END)
                self.mathin.delete(0,tk.END)
                self.geoin.delete(0,tk.END)
                self.histin.delete(0,tk.END)
                self.sciin.delete(0,tk.END)
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error : {e}")
        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields.")
    # ClassA Button
    def classA_button(self):
        val1 = "Class A"
        try:
            self.dbfun()
            self.cur.execute("select * from student where class=%s",val1)
            data = self.cur.fetchall()
            if data:
                self.stud_tabFun()
                self.table.delete(*self.table.get_children())
                for j in data:
                    self.table.insert('',tk.END,values=j)
                self.conn.close()
            else:
                tk.messagebox.showerror("Error","No data exits.")
        except Exception as e:
            tk.messagebox.showerror("Error",f"Error : {e}")
    # ClassB Button
    def classB_button(self):
        val1 = "Class B"
        try:
            self.dbfun()
            self.cur.execute("select * from student where class=%s",val1)
            data = self.cur.fetchall()
            if data:
                self.stud_tabFun()
                self.table.delete(*self.table.get_children())
                for j in data:
                    self.table.insert('',tk.END,values=j)
                self.conn.close()
            else:
                tk.messagebox.showerror("Error","No data exits.")
        except Exception as e:
            tk.messagebox.showerror("Error",f"Error : {e}")

    # ClassC Button
    def classC_button(self):
        val1 = "Class C"
        try:
            self.dbfun()
            self.cur.execute("select * from student where class=%s",val1)
            data = self.cur.fetchall()
            if data:
                self.stud_tabFun()
                self.table.delete(*self.table.get_children())
                for j in data:
                    self.table.insert('',tk.END,values=j)
                self.conn.close()
            else:
                tk.messagebox.showerror("Error","No data exits.")
        except Exception as e:
            tk.messagebox.showerror("Error",f"Error : {e}")

    # ScoreBoard Button
    def scr_button(self):
        try:
            self.dbfun()
            self.cur.execute("select student.rollno,student.name,score.mya,score.eng,score.math,score.geo,score.hist,score.sci from student inner join score on student.rollno = score.rollno")
            data = self.cur.fetchall()
            if data:
                self.all_score_Frame()
                self.table.delete(*self.table.get_children())
                for j in data:
                    self.table.insert('',tk.END,values=j)
            else:
                tk.messagebox.showerror("Error","No data exits.")
        finally:
            self.conn.close()


# ====================================================================================
    def dbfun(self):
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="ijdzlnc6",
                database="school"
                )
            self.cur = self.conn.cursor()
# ===================== Run Code =====================
root = tk.Tk()
obj = std(root)
root.mainloop()