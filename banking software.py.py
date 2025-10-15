import tkinter as tk 
from tkinter import messagebox
import mysql.connector as sqltor
from PIL import ImageTk, Image
import numpy as np

conn = sqltor.connect(host="localhost", user="root", passwd="tiger", database="project")

cursor = conn.cursor()
cursor.execute(" create database if not exists project")
cursor.execute(''' create table if not exists customer(accno int primary key,
               name varchar(50),
               contactno varchar(10),
               address varchar(100),
               acc_type varchar(20),
               age int,
               balance int)''')
conn.commit()

#mainscreen
master = tk.Tk()
master.title("banking software")

def qcall():
    qry = "select accno from customer"
    cursor.execute(qry)
    d = cursor.fetchall()
    k = []
    for i in range(0,len(d)):
        k.append(d[i][0])
    return k

def new_customer():
    name = temp_name.get().upper()                      #.get() is to basically fetch data that is stored
    accno = np.random.randint(100000,999999)
    accctype=add_var.get().upper()
    age = temp_age.get()
    phone=temp_phone.get()
    city = temp_city.get().upper()
    bal = temp_bal.get()

    if name == "" or age == "" or phone == 0 or accctype == "" or city == '' or bal == 0 :
        notif.config(fg="red",text="All Fields Required")
        return
    else:
        #query to insert
        insert_query = 'insert into customer values(%s, %s, %s,%s,%s,%s,%s)'
        data = (accno,name,phone,city,accctype,age,bal)
        cursor.execute(insert_query,data)
        conn.commit()
        
        z = "Your account number is: "+str(accno)  
        messagebox.showinfo("confirmation",z)
        na_screen.destroy()
     


def view_bal():
    name = login_temp_name.get().upper()
    accountno = login_temp_accountno.get()
    
    list_accno = qcall()

    if name == "" or accountno == "":
            login_notif.config(fg="red",text="All Fields Required")

    else:
        if int(accountno) in list_accno :
            select_query = 'SELECT * FROM customer WHERE accno = %s'
            data = (accountno,)
            cursor.execute(select_query, data)
            acc_det = cursor.fetchall()
            c = []
            for i in range(0,7):
                c.append(acc_det[0][i])

            pstuff = "ACCOUNT NUMBER : "+str(c[0])+"\nNAME : "+c[1]+"\nCONTACT NUMBER : "+str(c[2])+"\nADDRESS : "+c[3]+"\nACCOUNT TYPE : "+c[4]+"\nAGE : "+str(c[5])+"\nBALANCE : "+str(c[6])
            messagebox.showinfo("Account Details",pstuff)
            cb_screen.destroy()

        else:
            messagebox.showwarning("Check Details", "Account Not Found")


def finishmod():
    old = mod_temp.get()
    new = mod_temp2.get()
    accno = mod_acc.get()
    col = var.get()

    z = qcall()
        
    if mod_temp.get()=="" or new=="" or accno == "":
        mod_notif.config(fg="red",text="All Fields Required")
        
    else:
        if int(accno) in z :
            if var.get() == "Age":
                #qry to change age
                qry = "update customer set age = %s where age=%s and accno = %s"
                data=(int(new),int(old),accno)
                cursor.execute(qry,data)
                conn.commit()
                messagebox.showinfo('Confirmation',"Details updated")
    
            elif var.get() == "Resident City":
                #query
                qry = "update customer set address = %s where address=%s and accno = %s"
                data=(new.upper(),old.upper(),accno)
                cursor.execute(qry,data)
                conn.commit()
                messagebox.showinfo('Confirmation',"Details updated")
                
            elif var.get() == "Name":
                #query            
                qry = "update customer set name = %s where name=%s and accno = %s"
                data=(new.upper(),old.upper(),accno)
                cursor.execute(qry,data)
                conn.commit()
                messagebox.showinfo('Confirmation',"Details updated")

            elif var.get()=="Phone Number":
                #query to change phone number
                qry = "update customer set  contactno= %s where contactno=%s and accno = %s"
                data=(new.upper(),old.upper(),accno)
                cursor.execute(qry,data)
                conn.commit()
                messagebox.showinfo('confirmation',"Details updated")
            
            ma_screen.destroy()

        else:
             messagebox.showwarning('Check Details',"Account Not Found")


def finish_wmoney():
    accno = wm_temp_accno.get()
    name = wm_temp_name.get().upper()
    amt = wm_temp_amt.get()

    z = qcall()

    q = "select balance from customer where accno = %s"
    data =(accno,)
    cursor.execute(q,data)
    c = cursor.fetchone()
    #query to acces bank balance bb, check if bb>amt or bb<amt

    if name == "" or accno == "" or amt == "":
        wm_notif.config(fg="red",text="All Fields Required")
    
    elif int(accno) in z:
        if float(amt)<=c[0]:
            #conditional staments for bb and amt
            qry = "update customer set balance = %s where accno = %s"
            data = (c[0]-float(amt),int((accno)))
            cursor.execute(qry,data)
            conn.commit()

            messagebox.showinfo("information","Transaction complete \nRemaining Balance:"+str(data[0]))

        elif float(amt)>=c[0]:
            messagebox.showerror("Error","Insufficient Funds")

        wm_screen.destroy()

    else:
        messagebox.showwarning("Check Details","Account Not Found")
        

    
def finish_dmoney():
    accno = dm_temp_accno.get()
    name =dm_temp_name.get().upper()
    amt = dm_temp_amt.get()

    k = qcall()  
    
    #query to acces bank balance bb, check if bb>amt or bb<amt
    qry = "select balance from customer where accno = %s"
    data =(accno,)
    cursor.execute(qry,data)
    c = cursor.fetchone()

    if name == "" or accno == "" or amt == "":
        dm_notif.config(fg="red",text="All Fields Required")
    
    elif int(accno) in k:
        if float(amt)<1000 or float(amt)>200000000:
            messagebox.showwarning("Transaction Limits","Amount Out of Transaction Limit (1000 - 200000000)")
            
        else:
            qry = "update customer set balance = %s where accno = %s"
            data = (c[0]+float(amt),accno)
            cursor.execute(qry,data)
            conn.commit()
            messagebox.showinfo("Information","Transaction Complete \nCurrent Balance : "+str(data[0]))
            dm_screen.destroy()
    else:
        messagebox.showwarning("Check Details","Account Not Found")
        


def finish_delacc():
    accno = del_temp_accno.get()
    name =del_temp_name.get().upper()

    k = qcall() 

    #query to check if record exists and to delete
    if name == "" or accno == "":
        del_notif.config(fg="red",text="All Fields Required")

    elif int(accno) in k:
            qry = "delete from customer where accno = %s"
            data = (accno,)
            cursor.execute(qry,data)
            conn.commit()
            messagebox.showinfo("Action Complete","Account Deleted")
            del_screen.destroy()


    else:
        messagebox.showwarning("Check Details","Account Not Found")
        



def new_accout():
    
    global temp_bal,temp_age,temp_city,temp_name,temp_phone,notif,add_var,na_screen
    
    temp_name= tk.StringVar()
    temp_phone=tk.IntVar()
    temp_age = tk.StringVar()
    temp_city=tk.StringVar()
    temp_bal = tk.IntVar()
    na_screen = tk.Toplevel(master)
    na_screen.title('New Account')
    #na_screen.geometry("500x500")
    
    #label
    tk.Label(na_screen, text = "ENTER DETAILS", font=('Calibri',12)).grid(row=0,sticky='N',pady=10,padx =10)
    tk.Label(na_screen, text = "Name", font=('Calibri',12)).grid(row=1,sticky='w',pady=10,padx =10)
    tk.Label(na_screen, text = "Phone no.", font=('Calibri',12)).grid(row=2,sticky='w',pady=10,padx =10)
    tk.Label(na_screen, text = "Age", font=('Calibri',12)).grid(row=3,sticky='w',pady=10,padx =10)
    tk.Label(na_screen, text = "Residing City", font=('Calibri',12)).grid(row=4,sticky='w',pady=10,padx =10)
    tk.Label(na_screen, text ='Choose Account type \n(Checking or Saving)', font=('Calibri',12)).grid(row=5,sticky='w',pady=10,padx =10)
    tk.Label(na_screen, text = "Deposit Balance", font=('Calibri',12)).grid(row=6,sticky='w',pady=10,padx =10)
    notif = tk.Label(na_screen, font=('Calibri',12))
    notif.grid(row=8,column=1,sticky='n',pady=10)

    #enteries
    tk.Entry(na_screen,textvariable=temp_name).grid(row=1,column=1)
    tk.Entry(na_screen,textvariable=temp_phone).grid(row=2,column=1)
    tk.Entry(na_screen,textvariable=temp_age).grid(row=3,column=1)
    tk.Entry(na_screen,textvariable=temp_city).grid(row=4,column=1)
    acctypes = ['Checkings',"Savings"]
    add_var = tk.StringVar()
    add_spinbox = tk.Spinbox(na_screen,values =acctypes,textvariable=add_var, width = 13,font=("calibri",12)).grid(row =5,column=1,sticky='n',padx=10,pady=10)
    add_var.set("Savings")
    tk.Entry(na_screen,textvariable=temp_bal).grid(row=6,column=1)

    #button
    tk.Button(na_screen,text="Add New Customer",font=('Calibri',12),command=new_customer).grid(row=7,column = 1,sticky='n',pady=10,padx=10)
    

def check_balance():
    global login_temp_accountno,login_temp_name,login_notif,cb_screen
   
    login_temp_accountno = tk.StringVar()
    login_temp_name = tk.StringVar()

    cb_screen = tk.Toplevel(master)
    cb_screen.title("Check Balance")
    #cb_screen.geometry("300x300")
    
    tk.Label(cb_screen,text="ENTER DETAILS",font=('Calibri',12)).grid(row = 0,sticky ='N',pady=10,padx =10)
    tk.Label(cb_screen, text = "Name", font=('Calibri',12)).grid(row=1,sticky='w',pady=10,padx =10)
    tk.Label(cb_screen, text = "Account Number", font=('Calibri',12)).grid(row=2,sticky='w',pady=10,padx =10)
    login_notif=tk.Label(cb_screen, font=('Calibri',12))
    login_notif.grid(row = 4,column=1, sticky = 'n')

    tk.Entry(cb_screen,textvariable = login_temp_name).grid(row=1,column =1,padx =10)
    tk.Entry(cb_screen,textvariable = login_temp_accountno).grid(row=2,column =1,padx=10)

    tk.Button(cb_screen,text ="View Balance",font=('Calibri',12),command=view_bal).grid(row=3,column=1,sticky='n',pady=10,padx=10)

def modifyacc():
    #vars
    global mod_temp,var,mod_notif,mod_temp2,mod_acc,ma_screen
    
    mod_temp=tk.StringVar()
    mod_temp2=tk.StringVar()
    mod_acc=tk.StringVar()
    ma_screen = tk.Toplevel(master)
    ma_screen.title("Choose Field")

    #labels
    tk.Label(ma_screen,text="ENTER DETAILS", font=('Calibri',12)).grid(row=0,sticky=tk.EW,pady=10,padx =30)
    tk.Label(ma_screen,text="Enter Account Number", font=('Calibri',12)).grid(row=1,sticky='w',pady=10,padx =10)
    tk.Label(ma_screen,text="Enter Old", font=('Calibri',12)).grid(row=2,sticky='w',pady=10,padx =10)
    tk.Label(ma_screen,text="Choose Field To Be Modified", font=('Calibri',12)).grid(row=3,sticky='w',pady=10,padx =10)
    tk.Label(ma_screen,text="Enter New", font=('Calibri',12)).grid(row=4,sticky='w',pady=10,padx =10)

    #entry
    tk.Entry(ma_screen,textvariable = mod_acc).grid(row=1,column =1)
    tk.Entry(ma_screen,textvariable = mod_temp).grid(row=2,column =1)            # mod temp is the old value of selcetd field
    tk.Entry(ma_screen,textvariable = mod_temp2).grid(row=4,column =1)            # mod_temp2 is the new value
    data = ["Account Number","Age","Resident City","Name","Phone Number"]
    var = tk.StringVar()
    myspinbox=tk.Spinbox(ma_screen,values =data,textvariable=var, width = 14,font=("calibri",12)).grid(row =3,column=1,padx=10,pady=10)
    var.set("Phone Number")

    #BUTTONS 
    tk.Button(ma_screen,text ="Modify Records",font=('Calibri',12),command=finishmod).grid(row=5,column=1,sticky='EW',pady=10,padx=50)
    #notif
    mod_notif = tk.Label(ma_screen, font=('Calibri',12))
    mod_notif.grid(row =6,column=1,sticky ='N')


def wmoney():
    
    global wm_temp_name,wm_temp_accno,wm_temp_amt,wm_notif,wm_screen
    
    wm_temp_name =tk.StringVar()
    wm_temp_accno =tk.StringVar()
    wm_temp_amt=tk.StringVar()

    wm_screen = tk.Toplevel(master)
    wm_screen.title("Withdrawal")
    
    tk.Label(wm_screen,text="ENTER DETAILS",font=('Calibri',12)).grid(row = 0,sticky ='N',pady=10,padx =10)
    tk.Label(wm_screen, text = "Name", font=('Calibri',12)).grid(row=1,sticky='w',pady=10,padx =10)
    tk.Label(wm_screen, text = "Account Number", font=('Calibri',12)).grid(row=2,sticky='w',pady=10,padx =10)
    tk.Label(wm_screen, text = "Amount To Be Withdrawn", font=('Calibri',12)).grid(row=3,sticky='w',pady=10,padx =10)

    tk.Entry(wm_screen,textvariable = wm_temp_name).grid(row=1,column =1,padx=10)
    tk.Entry(wm_screen,textvariable = wm_temp_accno).grid(row=2,column =1,padx=10)
    tk.Entry(wm_screen,textvariable = wm_temp_amt).grid(row=3,column =1,padx=10)

    tk.Button(wm_screen,text ="Withdraw Money",font=('Calibri',12),command=finish_wmoney).grid(row=4,column=1,pady=10,padx=10)
       
    wm_notif = tk.Label(wm_screen, font=('Calibri',12))
    wm_notif.grid(row = 5,column=1,pady =10)


def dmoney():
    global dm_temp_name,dm_temp_accno,dm_temp_amt,dm_notif,dm_screen
    
    dm_temp_name =tk.StringVar()
    dm_temp_accno =tk.StringVar()
    dm_temp_amt=tk.StringVar()

    dm_screen = tk.Toplevel(master)
    dm_screen.title("Deposit")
    
    tk.Label(dm_screen,text="ENTER DETAILS",font=('Calibri',12)).grid(row = 0,sticky ='N',pady=10,padx =10)
    tk.Label(dm_screen, text = "Name", font=('Calibri',12)).grid(row=1,sticky='w',pady=10,padx =10)
    tk.Label(dm_screen, text = "Account Number", font=('Calibri',12)).grid(row=2,sticky='w',pady=10,padx =10)
    tk.Label(dm_screen, text = "Amount To Be Deposited", font=('Calibri',12)).grid(row=3,sticky='w',pady=10,padx =10)

    tk.Entry(dm_screen,textvariable = dm_temp_name).grid(row=1,column =1,padx=10)
    tk.Entry(dm_screen,textvariable = dm_temp_accno).grid(row=2,column =1,padx=10)
    tk.Entry(dm_screen,textvariable = dm_temp_amt).grid(row=3,column =1,padx=10)
    tk.Button(dm_screen,text ="Deposit Money",font=('Calibri',12),command=finish_dmoney).grid(row=4,column=1,pady=10,padx=10)
       
    dm_notif = tk.Label(dm_screen, font=('Calibri',12))
    dm_notif.grid(row = 5,column=1,sticky = 'n')
    

def delacc():
    global del_temp_name,del_temp_accno,del_notif,del_screen
    
    del_temp_name =tk.StringVar()
    del_temp_accno =tk.StringVar()

    del_screen = tk.Toplevel(master)
    del_screen.title("Delete")

    tk.Label(del_screen,text="ENTER DETAILS",font=('Calibri',12)).grid(row = 0,sticky ='N',pady=10,padx =10)
    tk.Label(del_screen, text = "Name", font=('Calibri',12)).grid(row=1,sticky='w',pady=10,padx =10)
    tk.Label(del_screen, text = "Account Number", font=('Calibri',12)).grid(row=2,sticky='w',pady=10,padx =10)

    tk.Entry(del_screen,textvariable = del_temp_name).grid(row=1,column =1,padx=10)
    tk.Entry(del_screen,textvariable = del_temp_accno).grid(row=2,column =1,padx=10)
    
    tk.Button(del_screen,text ="Delete Records",font=('Calibri',12),command=finish_delacc).grid(row=3,column=1,pady=10,padx=10)

    del_notif = tk.Label(del_screen, font=('Calibri',12))
    del_notif.grid(row = 4,column=1,sticky = 'n')

def exit():
    z = messagebox.askquestion('Exit',"Are you Sure you want to exit the application ?")
    if z =="yes":
        master.destroy()
    elif z == "no":
        pass

#image
img = Image.open('secure.png')
img = img.resize((150,150))
img = ImageTk.PhotoImage(img)

#labels 
tk.Label(master, text = "Custom Banking", font=('Calibri',20,'bold')).grid(row=0,sticky='N',pady=10)
tk.Label(master, text = "The most secure bank you've probably used", font=('Calibri',12)).grid(row=1,sticky='N')
tk.Label(master, image=img).grid(row=2,sticky='N',pady=10)

#buttons
tk.Button(master, text="New Account", font=('Calibri',14),width=20,command=new_accout).grid(row=3,sticky='N',pady =10)
tk.Button(master, text="Check Balance", font=('Calibri',14),width=20,command=check_balance).grid(row=4,sticky='N',pady=10)
tk.Button(master,text="Modify Account",font=('Calibri',14),width=20,command=modifyacc).grid(row=5,sticky='N',pady=10)
tk.Button(master,text="Withdraw Money",font=('Calibri',14),width=20,command=wmoney).grid(row=6,sticky='N',pady=10)
tk.Button(master,text="Deposit Money",font=('Calibri',14),width=20,command=dmoney).grid(row=7,sticky='N',pady=10)
tk.Button(master,text="Delete Account",font=('Calibri',14),width=20,command=delacc).grid(row=8,sticky='N',pady=10)
tk.Button(master,text='Exit',font=("calibri",10,"bold"),width=15,command=exit).grid(row=9,pady= 10)

master.mainloop()
