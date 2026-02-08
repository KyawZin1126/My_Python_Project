from tkinter import *
from tkinter import messagebox

root=Tk()
root.title("Login Form")
root.geometry("925x500+300+200")
root.configure(bg="#FFFFFF")
root.resizable(False,False)

def signin():
    username = user.get()
    code= password.get()

    if username == "Admin" and code == "1234":
        screen=Toplevel(root)
        screen.title=("App")
        screen.geometry('925x500+300+200')
        screen.config(bg="White")

        Label(screen, text="Hello Everyone!", bg="#FFF", font=("Segoe UI",20,"bold")).pack(expand=True)

        screen.mainloop()

    elif username !="Admin" or code != "1234":
        messagebox.showerror("Invalid", "Invalid Username and Password")

img = PhotoImage(file="assets/images/login.png")
Label(root, image=img, bg="White").place(x=50,y=50)

frame = Frame(root,width=350, height=350, bg="White")
frame.place(x=480,y=70)

heading = Label(frame, text="Log In", fg="#57a1f8",bg="White",font=("Segoe UI",23,"bold"))
heading.place(x=100,y=5)

# User Entry
def on_enter(e):
    user.delete(0,'end')

def on_leave(e):
    name=user.get()
    if name=="":
        user.insert(0,"Username")

user = Entry(frame, width=25,fg="Black",border=0,bg='White',font=("Segoe UI",11))
user.place(x=30,y=80)
user.insert(0,"Username")
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg="Black").place(x=25,y=107)

# Password Entry
def on_enter(e):
    password.delete(0,'end')

def on_leave(e):
    code=password.get()
    if code=="":
        password.insert(0,"Password")

password = Entry(frame, width=25,fg="Black",border=0,bg='White',font=("Segoe UI",11))
password.place(x=30,y=150)
password.insert(0,"Password")
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg="Black").place(x=25,y=177)

# Button
Button(frame, width=40, pady=8, text="Sign In", bg="#57a1f8", fg="White", border=0,command=signin).place(x=35,y=204)

label=Label(frame, text="Don't have an account?", fg="Black",bg="White",font=("Segoe UI",9))
label.place(x=75,y=270)
sign_up = Button(frame, width=6, text="Sign Up", border=0, bg="White", cursor="hand2", fg="#57a1f8")
sign_up.place(x=217,y=270)

root.mainloop()