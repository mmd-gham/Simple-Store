import tkinter as tk
import sqlite3


class create_database():

    def __init__(self):
        ### create customers table

        sql = '''CREATE TABLE customers
        (ID INTEGER PRIMARY KEY,
        username CHAR(20) NOT NULL,
        password CHAR(20) NOT NULL,
        ncode CHAR(15) NOT NULL,
        score INT (3),
        address CHAR (50) NOT NULL)'''

        cnt.execute(sql)
        cnt.commit()
        print("Table created successfully")

        ### seeding customers table

        sql = ''' INSERT INTO customers (username,password,ncode,score,address)
            VALUES ("admin","a123456789","99999999",0,"rasht") '''

        cnt.execute(sql)
        cnt.commit()
        print("seeding successful")

        ### create products table

        sql = '''CREATE TABLE products
        (ID INTEGER PRIMARY KEY,
        pname CHAR(30) NOT NULL,
        qnt INT (4) NOT NULL,
        image CHAR(30),
        price INT NOT NULL,
        exdate CHAR (20) NOT NULL )'''

        cnt.execute(sql)
        cnt.commit()
        print("Table created successfully")

        ### seeding products table

        sql = ''' INSERT INTO products (pname,qnt,image,price,exdate)
            VALUES ("pen",1000,"",0,"1/1/1") '''
        cnt.execute(sql)
        cnt.commit()
        print("seeding successful")

        ### create shop table

        sql = '''CREATE TABLE shop
        (ID INTEGER PRIMARY KEY,
        uid INT NOT NULL,
        pid INT NOT NULL)'''

        cnt.execute(sql)
        cnt.commit()
        print("Table created successfully")
userid=""


try:
    cnt = sqlite3.connect('simple_store.db')
except:
    print("An error occurred in database connection")
try:
    query = '''SELECT * FROM customers '''
    result = cnt.execute(query,)
except:
    create = create_database()



class MainWindow():

    def __init__(self,master):
        self.master = master
        self.master.geometry('350x200')
        self.master.title('Simple Shop')
        self.master.resizable(False, False)

        self.lbl_msg = tk.Label(self.master, text='Welcome to simple shop')
        self.lbl_msg.pack(pady=10)

        self.login_btn = tk.Button(self.master, text="Login ", command=self.login)
        self.login_btn.pack()

        self.submit_btn = tk.Button(self.master, text="Submit", command=self.submit)
        self.submit_btn.pack()

        self.logout_btn = tk.Button(self.master, text="Logout ", state="disabled", command=self.logout)
        self.logout_btn.pack()

        self.regp_btn = tk.Button(self.master, text="Register ", state="disabled", command=self.regprod)
        self.regp_btn.pack()

        self.shop_btn = tk.Button(self.master, text="Shop ", state="disabled", command=self.shop)
        self.shop_btn.pack()


    def login(self):
        login_window = login(self)
    def submit(self):
        submit_window = submit(self)
    def logout(self):
        logout_window = logout(self)
    def regprod(self):
        regprod_window = regprod()
    def shop(self):
        shop_window = shop()


class submit(MainWindow):
    def __init__(self, main_window):
        self.main_window = main_window

        self.submit_win = tk.Toplevel()
        self.submit_win.title("Submit")
        self.submit_win.geometry("350x300")

        self.lbl_user2 = tk.Label(self.submit_win, text='Username:')
        self.lbl_user2.pack()
        self.usernamew = tk.Entry(self.submit_win, width=15)
        self.usernamew.pack()

        self.lbl_pass2 = tk.Label(self.submit_win, text='Password:')
        self.lbl_pass2.pack()
        self.passw = tk.Entry(self.submit_win, width=15)
        self.passw.pack()
        self.lbl_pass3 = tk.Label(self.submit_win, text='Confirm password:')
        self.lbl_pass3.pack()
        self.cpassw = tk.Entry(self.submit_win, width=15)
        self.cpassw.pack()

        self.lbl_ncode = tk.Label(self.submit_win, text='National code:')
        self.lbl_ncode.pack()
        self.ncodew = tk.Entry(self.submit_win, width=15)
        self.ncodew.pack()

        self.lbl_addrw = tk.Label(self.submit_win, text='Address:')
        self.lbl_addrw.pack()
        self.addrw = tk.Entry(self.submit_win, width=35)
        self.addrw.pack()

        self.submit_btn2 = tk.Button(self.submit_win, text="Submit", command=self.submit2)
        self.submit_btn2.pack(pady=5)
        self.lbl_msg2 = tk.Label(self.submit_win, text='')
        self.lbl_msg2.pack()

    def submit2(self):
        self.user2 = self.usernamew.get()
        self.pass2 = self.passw.get()
        self.cpass2 = self.cpassw.get()
        self.ncode = self.ncodew.get()
        self.score = 0
        self.addr = self.addrw.get()


        ######### checking info
        if (self.user2 == "" or self.pass2=="" or self.ncode=="" or self.addr==""):
            self.lbl_msg2.configure(text="Fill the boxes to submit")
            return
        elif (len(self.pass2)<=8):
            self.passw.delete(0, 'end')
            self.lbl_msg2.configure(text="Password should have more than 8 characters")
            return
        elif (self.pass2 != self.cpass2):
            self.cpassw.delete(0, 'end')
            self.lbl_msg2.configure(text="Confirm your password")
            return
        try:
            int(self.ncode)
        except:
            self.ncodew.delete(0, 'end')
            self.lbl_msg2.configure(text="National code should be a number")
            return

        ######### checking username
        query = '''SELECT * FROM customers WHERE username=?'''
        result = cnt.execute(query, (self.user2,))
        if (result.fetchone()):
            self.lbl_msg2.configure(text="Username already exist")
            return

        ######## insert data into customers table
        query = '''INSERT INTO customers (username,password,ncode,score,address) 
                        VALUES(?,?,?,?,?)'''
        cnt.execute(query, (self.user2, self.pass2, self.ncode, self.score, self.addr))
        cnt.commit()
        ########## success message
        self.usernamew.delete(0, 'end')
        self.passw.delete(0, 'end')
        self.cpassw.delete(0, 'end')
        self.ncodew.delete(0, 'end')
        self.addrw.delete(0, 'end')
        self.lbl_msg2.configure(text="Submit Done!")
        self.main_window.lbl_msg.configure(text="Please, Login Now")


class regprod:
    def __init__(self):
        self.reg_win = tk.Toplevel()
        self.reg_win.title("Register products")
        self.reg_win.geometry("350x300")

        self.lbl_msg2 = tk.Label(self.reg_win, text='')
        self.lbl_msg2.pack()

        self.lbl_pname = tk.Label(self.reg_win, text='Product name: ')
        self.lbl_pname.pack()
        self.pname = tk.Entry(self.reg_win, width=15)
        self.pname.pack()

        self.lbl_qnt = tk.Label(self.reg_win, text='Quantity: ')
        self.lbl_qnt.pack()
        self.qnt = tk.Entry(self.reg_win, width=15)
        self.qnt.pack()

        self.lbl_price = tk.Label(self.reg_win, text='Price: ')
        self.lbl_price.pack()
        self.price = tk.Entry(self.reg_win, width=15)
        self.price.pack()

        self.lbl_exdate = tk.Label(self.reg_win, text='Expire date: ')
        self.lbl_exdate.pack()
        self.exdate = tk.Entry(self.reg_win, width=15)
        self.exdate.pack()

        self.reg_btn = tk.Button(self.reg_win, text="Register", command=self.preg2)
        self.reg_btn.pack(pady=20)

        self.reg_win.resizable(False, False)
        self.reg_win.mainloop()

    def preg2(self):
        self.prpname = self.pname.get()

        self.prqnt = self.qnt.get()
        self.prprice = self.price.get()
        self.prexdate = self.exdate.get()

        ######## checking info
        if (self.prpname=="" or self.prqnt=="" or self.prprice=="" or self.prexdate==""):
            self.lbl_msg2.configure(text="Fill the boxes to register a product")
            return
        try:
            int(self.prqnt)
        except:
            self.qnt.delete(0, 'end')
            self.lbl_msg2.configure(text="Quantity should be a number")
            return
        try:
            int(self.prprice)
        except:
            self.price.delete(0, 'end')
            self.lbl_msg2.configure(text="Price should be a number")
            return
        try:
            int(self.prexdate)
        except:
            self.exdate.delete(0, 'end')
            self.lbl_msg2.configure(text="Expire date should be a year")
            return


        ######## insert data into customers table
        query = ''' INSERT INTO products (pname,qnt,price,exdate)
              VALUES (?,?,?,?) '''
        cnt.execute(query, (self.prpname, self.prqnt, self.prprice, self.prexdate))
        cnt.commit()

        ######## success message
        self.pname.delete(0, 'end')
        self.qnt.delete(0, 'end')
        self.price.delete(0, 'end')
        self.exdate.delete(0, 'end')
        self.lbl_msg2.configure(text="register Done!")


class shop:
    def __init__(self):
        self.shop_win = tk.Toplevel()
        self.shop_win.title("Shop")
        self.shop_win.geometry("350x450")
        self.lbl_shop_msg = tk.Label(self.shop_win, text='')
        self.lbl_shop_msg.pack(pady=5)
        self.lstbx = tk.Listbox(self.shop_win, height=20, width=40)
        self.lstbx.pack()

        self.lbl_shop = tk.Label(self.shop_win, text='product ID: ')
        self.lbl_shop.pack()
        self.pid = tk.Entry(self.shop_win, width=15)
        self.pid.pack()

        self.shop_btn2 = tk.Button(self.shop_win, text="Shop Now", command=self.shopnow)
        self.shop_btn2.pack(pady=10)

        ################################### inserting information of items
        query = ''' SELECT * FROM products'''
        result = cnt.execute(query)
        rows = result.fetchall()
        self.ID_lst=[]
        for row in rows:
            self.lstbx.insert("end", "ID: " + str(row[0]) + "   " + "name: " + row[1] + " QNT: " + str(row[2]))
            self.ID_lst.append(str(row[0]))
        ###################################

        self.shop_win.resizable(False, False)
        self.shop_win.mainloop()


    def shopnow(self):
        global userid

        self.proid=self.pid.get()
        if (self.proid in self.ID_lst):
            query='''INSERT INTO shop (uid,pid)
                     VALUES(?,?)'''
            cnt.execute(query,(userid,self.proid))
            cnt.commit()
            self.lbl_shop_msg.configure(text="Shop approved")
            self.pid.delete(0,"end")
            ###########################################
            query=''' select qnt from products where id=? '''
            result = cnt.execute(query,(self.proid,))
            row = result.fetchone()
            qnt1=row[0]
            new_qnt=qnt1-1
            query=''' UPDATE products SET qnt=? WHERE id=? '''
            cnt.execute(query,(new_qnt,self.proid))
            cnt.commit()
            ########################################## update listbox
            self.lstbx.delete(0,"end")
            query = ''' SELECT * FROM products'''
            result = cnt.execute(query)
            rows = result.fetchall()
            for row in rows:
                self.lstbx.insert("end","ID: "+str(row[0])+"   "+"name: "+row[1]+" QNT: "+str(row[2]))
        else:
            self.lbl_shop_msg.configure(text="Enter a ID number first")
            self.pid.delete(0, "end")


class login(MainWindow):
    def __init__(self, main_window):
        self.main_window = main_window
        ...

        self.login_win = tk.Toplevel()
        self.login_win.title("Login")
        self.login_win.geometry("350x200")

        self.lbl_temp = tk.Label(self.login_win, text='')
        self.lbl_temp.pack()

        self.lbl_user = tk.Label(self.login_win, text='Username:')
        self.lbl_user.pack()

        self.userw = tk.Entry(self.login_win, width=15)
        self.userw.pack()

        self.lbl_pass = tk.Label(self.login_win, text='Password')
        self.lbl_pass.pack()

        self.passwordw = tk.Entry(self.login_win, width=15)
        self.passwordw.pack()

        self.login_btn2 = tk.Button(self.login_win, text="Login", command=self.login2)
        self.login_btn2.pack(pady=20)

        self.login_win.resizable(False, False)
        self.login_win.mainloop()


    def login2(self):
        global userid

        self.user = self.userw.get()
        self.password = self.passwordw.get()

        query = '''SELECT * FROM customers WHERE username=? AND PASSWORD=?'''
        result = cnt.execute(query, (self.user, self.password))
        row = result.fetchall()

        if (row):
            userid = row[0][0]
            self.login_win.destroy()
            self.main_window.lbl_msg.configure(text="welcome " + self.user)
            self.main_window.login_btn.configure(state="disabled")
            self.main_window.logout_btn.configure(state="active")
            if self.user == "admin":
                self.main_window.regp_btn.configure(state="active")
            if (self.user):
                self.main_window.shop_btn.configure(state="active")

        else:
            self.userw.delete(0, 'end')
            self.passwordw.delete(0, 'end')
            self.lbl_temp.configure(text="Wrong username or password")


class logout(MainWindow):

    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.lbl_msg.configure(text="Confirm logout by clicking the button again !!!")
        self.main_window.logout_btn.configure(command=self.logout2)

    def logout2(self):
        self.main_window.login_btn.configure(state="active")
        self.main_window.logout_btn.configure(state="disabled")
        self.main_window.regp_btn.configure(state="disabled")
        self.main_window.shop_btn.configure(state="disabled")
        self.main_window.lbl_msg.configure(text="You are logged out now !!!")


root= tk.Tk()
window= MainWindow(root)
root.mainloop()