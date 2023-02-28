from datetime import date,datetime
from tkinter import * #type:ignore
from tkinter import ttk,messagebox
from PIL import ImageTk,Image
from tkcalendar import DateEntry
import sqlite3 as sq
import os
#my custom colors
dracula = '#171717'
red = '#D72343'
green = '#85FCCB'
drk_green = '#67C29D'
ent_bg = '#1F272C'
bg_img = 'Background\\opv.png'


#create directory
path = 'c:/OP Manager'
try:
    os.mkdir(path)
    print('Folder Created')
except FileExistsError:
    print ('Folder Already Exist In  ' +  path)

#DATABASE
try:
    connection = sq.connect('C:/OP Manager/OP Manager.db')
    print('Successfully Connected ✔ '+'\n')
except:
    print('Error in database')
try:

    connection.execute(''' CREATE TABLE USERS 
               (ID INTEGER PRIMARY KEY,
                USERNAME TEXT NOT NULL,
                REFERRAL TEXT NOT NULL,
                EMAIL TEXT NOT NULL,
                PHONE TEXT NOT NULL,
                DATE TEXT NOT NULL
                );''')
    print('Table Created Successfully ✔ ')
except:
    print('Table ✔ '+'\n')

def main_page():

    global img

    img = (Image.open(bg_img))
    img = img.resize((500,500),)
    img = ImageTk.PhotoImage(img)
    
    canvas = Canvas(width=500,bd=0,bg=dracula,highlightthickness=0)
    canvas.pack(side='left',fill='both')

    canvas.create_image(0,0, image=img, anchor='nw')
    
    Label(ws,text='',font=('segoe print',12,'bold'),bg=dracula).pack()
    
    btn_add = Button(ws,text='',command=destroy_to_add,bd=0,image=img_add_user,bg=dracula,activebackground=dracula)
    btn_add.pack(pady=25)

    btn_mng = Button(ws,command=destroy_to_search,bd=0,bg=dracula,activebackground=dracula,image=img_manage_user)
    btn_mng.pack(pady=25)

    btn_exit = Button(ws,command=ws.destroy,bd=0,bg=dracula,activebackground=dracula,image=img_exit)
    btn_exit.pack(pady=25)

def add_page():

    def add_to_db():

        u = username.get()
        r = referral.get()
        e = Email.get()
        p = phone.get()
        d = Date.get()
        
        if u == '':
            status.configure(text='Please Enter The Username')
            ws.after(5000,lambda: status.configure(text=''))
            return
        if r == '':
            status.configure(text='Please Enter The Referral')
            ws.after(5000,lambda: status.configure(text=''))
            return
        if d == '':
            status.configure(text='Please Enter The Date')
            ws.after(5000,lambda: status.configure(text=''))
            return
        if e == '':
            status.configure(text='Please Enter The Email')
            ws.after(5000,lambda: status.configure(text=''))
            return
        if p == '':
            status.configure(text='Please Enter The Phone')
            ws.after(5000,lambda: status.configure(text=''))
            return

        try:

            check = connection.execute("SELECT USERNAME FROM USERS WHERE USERNAME=? ",(u,))
            check = check.fetchone()

            if check==None:
                connection.execute('''INSERT INTO USERS (USERNAME,REFERRAL,EMAIL,PHONE,DATE)
                VALUES (?,?,?,?,?)''',(u,r,e,p,d))
                connection.commit()
                status.configure(text='User Successfully Added')
                ws.after(2500,lambda: status.configure(text=''))
            else:

                status.configure(text='User Already Exist!')
                ws.after(2500,lambda: status.configure(text=''))
        except:
            print('Problem in add to db 2')

    def dater():

        det = StringVar()
        det.set('')
        Date.configure(textvariable=det)

        getdate = StringVar()
        getdate.set(datetime.now().strftime('%d/%m/%Y'))
        Date.configure(textvariable=getdate)
    def timer():
        global clock
        clock = datetime.now().strftime('%a %I:%M:%S %p')
        cl.configure(text=clock)
        cl.after(1000,timer)
        
    my_frame = Frame(ws,bg=green)
    my_frame.pack(fill='both',expand=True,anchor='nw')

    my_canvas = Canvas(my_frame,bg=dracula,bd=0,highlightthickness=0)
    my_canvas.pack(expand=True,fill="both",anchor='nw')
    my_canvas.create_image(450,250,image=img_add_ui)
    username = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,highlightbackground=dracula,selectbackground=red)
    username.place(x=120,y=46,width=140)

    referral = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,highlightbackground=dracula,selectbackground=red)
    referral.place(x=408,y=46,width=140)

    Date = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,highlightbackground=dracula,selectbackground=red,state='normal',readonlybackground=dracula)
    Date.place(x=677,y=46,width=140)

    date_btn = Button(my_canvas,image=img_date,bg=dracula,bd=0,activebackground=dracula,command=dater,relief='flat')
    date_btn.place(x=840,y=40)

    Email = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,highlightbackground=dracula,selectbackground=red)
    Email.place(x=85,y=170,width=318)

    phone = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,validate='key',validatecommand=(ws.register(lambda P: P.isdigit() or P ==''), '%P'),bg=dracula,highlightbackground=dracula,selectbackground=red)
    phone.place(x=552,y=170,width=150)
    
    back = Button(my_canvas,image=img_back,bg=dracula,bd=0,activebackground=dracula,command=destroy_to_main)
    back.pack(side='left',anchor='sw')

    add = Button(my_canvas,image=img_add,bg=dracula,bd=0,activebackground=dracula,command=add_to_db,relief='flat')
    add.pack(side='right',anchor='se')
    
    cl = Label(my_canvas,bg=dracula,fg=red,justify='center',text='',font=('Arial',40,'bold'))
    cl.pack(side='bottom',anchor='n')

    status = Label(my_canvas,bg=dracula,fg=green,justify='center',text='',font=('Arial',13,'bold'))
    status.pack(side='bottom',anchor='n')

    timer()
    
def manage_users_page():

    def enable_edit_mode():
        for entry, button in [(username, btn_update), (referral, btn_update), (Date, btn_update), (Email, btn_update), (phone, btn_update)]:
            entry.configure(state=NORMAL)
            button.configure(state=NORMAL)

    def update_user():
        
        confirmation = messagebox.showwarning(title='Confirmation',message='Are you Sure?',type=messagebox.YESNO,default=messagebox.NO)
        if confirmation ==  'yes' :
            
            selected = my_tree.focus()
            values = my_tree.item(selected,'values')
            oid = values[0]
            my_tree.item(selected,values=(oid,username.get(),referral.get(),Email.get(),phone.get(),Date.get()))

            upd= connection.execute("UPDATE USERS  SET USERNAME = ?,REFERRAL = ?,EMAIL = ?,PHONE = ?,DATE = ? WHERE ID=? ",(username.get(),referral.get(),Email.get(),phone.get(),Date.get(),oid,))
            connection.commit()

            username.delete(0,END)
            Date.delete(0,END)
            Email.delete(0,END)
            referral.delete(0,END)
            phone.delete(0,END)
            for entry, button in [(username, btn_update), (referral, btn_update), (Date, btn_update), (Email, btn_update), (phone, btn_update)]:
                entry.configure(state='readonly')
                button.configure(state=DISABLED)
        else:
            pass

    def delete_user():

        confirmation = messagebox.showwarning(title='Confirmation',message='Are you Sure?',type=messagebox.YESNO,default=messagebox.NO)
        if confirmation ==  'yes' :
            
            u = username.get()

            selected = my_tree.focus()
            values = my_tree.item(selected,'values')
            oid = values[0]

            check = connection.execute("SELECT * FROM USERS WHERE ID=?",(oid,))
            check = check.fetchone()
            
            de = connection.execute("DELETE FROM USERS  WHERE ID=? ",(oid,))
            connection.commit()
            d = my_tree.selection()
            my_tree.delete(d)
            username.delete(0,END)
            Date.delete(0,END)
            Email.delete(0,END)
            referral.delete(0,END)
            phone.delete(0,END)
        else:
            pass

    style = ttk.Style()
    style.theme_use('default')
    style.configure('Treeview', background=dracula, foreground=dracula, rowheight=20, fieldbackground=dracula)
    style.map('Treeview', background=[('selected', '#904848')])

    tree_frame = Frame(ws, bg=dracula)
    tree_frame.pack(fill='x',anchor='nw',expand=False)

    options_frame = Frame(ws, bg=red)
    options_frame.pack(fill='both',expand=True)

    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side='right', fill='y')

    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='extended')
    my_tree.pack(fill=X)

    tree_scroll.config(command=my_tree.yview)

    my_tree['columns'] = ( 'ID','Username', 'Referral','Email', 'Phone', 'Date')

    my_tree.column('#0', width=0, stretch=NO)
    my_tree.column('ID', anchor='center', width=5)
    my_tree.column('Username', anchor='center', width=140)
    my_tree.column('Referral', anchor='center', width=140)
    my_tree.column('Email', anchor='center', width=140)
    my_tree.column('Phone', anchor='center', width=140)
    my_tree.column('Date', anchor='center', width=140)

    my_tree.heading('#0', text='', anchor='center')
    my_tree.heading('ID', text='ID', anchor='center')
    my_tree.heading('Username', text='Username', anchor='center')
    my_tree.heading('Referral', text='Referral', anchor='center')
    my_tree.heading('Email', text='Email', anchor='center')
    my_tree.heading('Phone', text='Phone', anchor='center')
    my_tree.heading('Date', text='Date', anchor='center')

    data = connection.execute("SELECT ID,USERNAME,REFERRAL,EMAIL,PHONE,DATE FROM USERS")
    data = data.fetchall()

    for i , row in enumerate(data):
        tags = ('evenrows',) if i % 2 == 0 else ('oddrows',)
        my_tree.insert(parent='', index='end', text='', values=row, tags=tags, iid=i) #type:ignore

    my_tree.tag_configure('evenrows', background='white')
    my_tree.tag_configure('oddrows', background='#bababa')

    my_canvas = Canvas(options_frame,bg=dracula,bd=0,highlightthickness=0,width=900,height=281)
    my_canvas.pack(fill='both',anchor='nw')
    my_canvas.create_image(450,140,image=img_search_ui)

    username = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,highlightbackground=dracula,selectbackground=red,readonlybackground=dracula,state='readonly')
    username.place(x=110,y=19,width=130)

    Date = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,highlightbackground=dracula,selectbackground=red,readonlybackground=dracula,state='readonly')
    Date.place(x=364,y=19,width=130)

    Email = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,highlightbackground=dracula,selectbackground=red,readonlybackground=dracula,state='readonly')
    Email.place(x=597,y=19,width=280)

    referral = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,highlightbackground=dracula,selectbackground=red,readonlybackground=dracula,state='readonly')
    referral.place(x=110,y=97,width=130)

    phone = Entry(my_canvas,font=('Arial',13,'bold'),justify='center',bd=0,fg=red,bg=dracula,validate='key',validatecommand=(ws.register(lambda P: P.isdigit() or P ==''), '%P'),highlightbackground=dracula,selectbackground=red,readonlybackground=dracula,state='readonly')
    phone.place(x=364,y=97,width=130)

    btn_back = Button(options_frame,image=img_sback,command=destroy_to_main,bg=dracula,activebackground=dracula,bd=0)
    btn_back.place(x=216,y=235)

    btn_delete = Button(options_frame,image=img_delete,command=delete_user,bg=red,activebackground=red,bd=0)
    btn_delete.place(x=316,y=235)

    btn_update = Button(options_frame,image=img_update,command=update_user,bg=red,activebackground=red,bd=0,state=DISABLED)
    btn_update.place(x=410,y=235)

    btn_edit = Button(options_frame,image=img_edit,command=enable_edit_mode,bg=red,activebackground=red,bd=0)
    btn_edit.place(x=516,y=235)

    def select_records(e):
        
        try:    
            
            delete = StringVar()
            delete.set('')
            username.configure(textvariable=delete)
            referral.configure(textvariable=delete)
            Date.configure(textvariable=delete)
            Email.configure(textvariable=delete)
            phone.configure(textvariable=delete)

            selected = my_tree.focus()

            values = my_tree.item(selected,'values')
            
            username.insert(0,values[1])
            Date.insert(0,values[5])
            Email.insert(0,values[3])
            referral.insert(0,values[2])
            phone.insert(0,values[4])

            insert1 = StringVar()
            insert1.set(values[1])
            insert2 = StringVar()
            insert2.set(values[2])
            insert3 = StringVar()
            insert3.set(values[3])
            insert4 = StringVar()
            insert4.set(values[4])
            insert5 = StringVar()
            insert5.set(values[5])

            username.configure(textvariable=insert1)
            Date.configure(textvariable=insert5)
            Email.configure(textvariable=insert3)
            referral.configure(textvariable=insert2)
            phone.configure(textvariable=insert4)
        except IndexError:
            pass
        
    my_tree.bind('<ButtonRelease-1>',select_records)

def destroy_to_main():
    try:
        for i in ws.winfo_children():
            i.forget()
        main_page()
    except:
        pass

def destroy_to_add():
    try:
        for i in ws.winfo_children():
            i.forget()
        add_page()
    except:
        pass

def destroy_to_search():
    try:
        for i in ws.winfo_children():
            i.forget()
        manage_users_page()
    except:
        pass


def root():
    global ws,img_add_user,img_manage_user,img_exit,img_back,img_add
    global img_add_ui,img_sback,img_update,img_delete,img_edit,img_search_ui,img_date
    ws = Tk()
    ws.title('OP Manager')
    ws.geometry('900x500')
    ws.config(bg=dracula)
    ws.iconbitmap('Icon\\icons8-openvpn-48.ico')
    ws.resizable(False,False)
    img_add_ui = PhotoImage(file='Background\\add_pageUI.png')
    img_search_ui = PhotoImage(file='Background\\Search_pageUI_new1.png')
    img_add_user = PhotoImage(file='Buttons\\Add user.png')
    img_manage_user = PhotoImage(file='Buttons\\Manage Users.png')
    img_exit = PhotoImage(file='Buttons\\Exit.png')
    img_back = PhotoImage(file='Buttons\\Back.png')
    img_sback = PhotoImage(file='Buttons\\sBack.png')
    img_add = PhotoImage(file='Buttons\\Add.png')
    img_update = PhotoImage(file='Buttons\\Update.png')
    img_delete = PhotoImage(file='Buttons\\delete.png')
    img_edit = PhotoImage(file='Buttons\\edit.png')
    img_date = PhotoImage(file='Icon\\icons8-calendar.png')

    main_page()
    ws.mainloop()

root()