from pyfiglet import Figlet
import mysql.connector
mydb=mysql.connector.connect(host='localhost',user='root',passwd='admin',database='library')
cur=mydb.cursor()

    
def login():
    flag=False
    print("""   __             _       
  / /  ___   __ _(_)_ __  
 / /  / _ \ / _` | | '_ \ 
/ /__| (_) | (_| | | | | |
\____/\___/ \__, |_|_| |_|
            |___/         """)

    username=input('Enter username:')
    password=input('Enter password:')
    query=f" select * from login where username=%s"
    cur.execute(query,(username,))
    user_data=cur.fetchall()
    for user in user_data:
        if user[1]==username and user[2]==password:
            print('Successfully logged in')
            uname = username.upper()
            f=Figlet(font="chunky")
            c=Figlet(font="cybersmall")

            print(f.renderText("Welcome"))
            print(c.renderText(uname))
            main_menu(username)
            flag=True
            break
        else:
            flag=False
    if flag==False:
        print('Login failed. Username or Password is Incorrect....redirecting..')
        close_after_1_Sec()
        menu()

def register ():
    print("""  __            _     _             _   _             
  /__\ ___  __ _(_)___| |_ _ __ __ _| |_(_) ___  _ __  
 / \/// _ \/ _` | / __| __| '__/ _` | __| |/ _ \| '_ \ 
/ _  \  __/ (_| | \__ \ |_| | | (_| | |_| | (_) | | | |
\/ \_/\___|\__, |_|___/\__|_|  \__,_|\__|_|\___/|_| |_|
           |___/                                       """)
    try:
        name=input('Enter your name')
        username = input("Enter Username (min. 6 characters): ")
        if len(username) < 6:
            print("Username should be atleast 6 characters")
            menu()
        password=input("Enter Password (min. 6 characters): ")
        if len(password) < 6:
            print("Password should be atleast 6 characters")
            menu()
        email =input("Enter Email:")
        phno = int(input("Enter Phone number (max. 13 numbers): "))
        address = input("Enter Address: ")
        query = f"insert into login(name,username, password,email, phno,address) values (%s,%s,%s,%s,%s,%s)"
        cur.execute(query,(name,username,password,email,phno,address))
        mydb.commit()
        print('Registration complete')
        close_after_1_Sec()
        login()
    except EOFError:
        print('Registration failed. Please Try Again')
        menu()
    
def admin():
    code = int(input("Enter Admin code: "))
    if code == 2022:
        print("Admin code accepted")
        quan=f"select BookQuantity from books"
        cur.execute(quan)
        alert1=cur.fetchall()
        for i in alert1:
            for j in i:
                if j==0:
                    alert=f"select BookName from books where BookQuantity=0"
                    cur.execute(alert)
                    alert2=cur.fetchall()
                    for books in alert2:
                        for book in books:
                            print('\nALERT!')
                            print('There is no stock available for the following books:\n',book)
                            print('Please Restock!')
                    mydb.commit()
                else:
                    break
        mydb.commit()
        print('\nWhat do you wish to do?')
        print('\n1.Add New Books\n2.View Books\n3.Exit')
        adm=int(input('Choose your option:'))
        if adm==1:
            lim=int(input('How many books do you wish to add?'))
            for i in range(lim):
                BookName = input("Enter Book Name: ")
                BookAuthor = input("Enter Book Author: ")
                BookRating = float(input("Enter Book Rating: "))
                BookGenre = input("Enter Book Genre: ")
                BookPrice = float(input("Enter Book Price: "))
                BookQuantity = int(input("Enter Book Quantity: "))
                query = f"insert into books(BookName,BookAuthor,BookRating,BookGenre,BookPrice,BookQuantity) values (%s,%s,%s,%s,%s,%s)"
                cur.execute(query,(BookName,BookAuthor,BookRating,BookGenre,BookPrice,BookQuantity,))
                mydb.commit()
            admin()
                
        elif adm==2:
            admquery=f"select * from books "
            cur.execute(admquery)
            adm_book=cur.fetchall()
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for books in adm_book:
                print(books)
            admin()
        elif adm==3:
            print('Exiting...')
            close_after_1_Sec()
            menu()
    else:
        print("You have entered the wrong admin code")
        menu()
        
def user_details(username):
    print("""                           ___     _        _ _     
 /\ /\  ___  ___ _ __     /   \___| |_ __ _(_) |___ 
/ / \ \/ __|/ _ \ '__|   / /\ / _ \ __/ _` | | / __|
\ \_/ /\__ \  __/ |     / /_//  __/ || (_| | | \__ \
 \___/ |___/\___|_|    /___,' \___|\__\__,_|_|_|___/
                                                   """)
    info=f'select name,email, phno,address from login where username="{username}"'
    cur.execute(info)
    rows = cur.fetchall()
    for row in rows:
        print('Your Name:',row[0])
        print('Your Phone number:',row[2])
        print('Your Email:',row[1])
        print('Your Address:',row[3])
    mydb.commit()

def out_of_stock(bookno):
    quan=f"select BookQuantity from books"
    cur.execute(quan)
    alert1=cur.fetchall()
    for i in alert1:
        for j in i:
            if j<=0:
                alert=f"select BookName from books where BookQuantity=0 and BookID={bookno}"
                cur.execute(alert)
                alert2=cur.fetchall()
                for books in alert2:
                    for book in books:
                        print('Sorry!!,The book',book,'is out of stock.')
                        browse(username)
                mydb.commit()
    mydb.commit()
    
    
    

def browse(username):
    print(""" #####                                 #     #                      
#     # ###### #    # #####  ######    ##   ## ###### #    # #    # 
#       #      ##   # #    # #         # # # # #      ##   # #    # 
#  #### #####  # #  # #    # #####     #  #  # #####  # #  # #    # 
#     # #      #  # # #####  #         #     # #      #  # # #    # 
#     # #      #   ## #   #  #         #     # #      #   ## #    # 
 #####  ###### #    # #    # ######    #     # ###### #    #  ####  """)
    print('\n1.Adventure\n2.Autobiography\n3.Young Adult and Teen\n4.Fiction\n5.Classic\n6.Fantasy\n7.Manga\n')
    gen=input('Enter genre number(seperate by comma if you like two or more genres):')
    l=gen.split(',')
    lim=len(l)
    for i in l:
        print('The genre(s) you have selected is/are:')
        if i=='1':
            print('\nAdventure\n')
            cur.execute('select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookGenre="Adventure"')
            adventure=cur.fetchall()
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in adventure:
                print(i)
            mydb.commit()
            
        if i=='2':
            print('\nAutobiography\n')
            cur.execute('select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookGenre="Autobiography"')
            autobiography=cur.fetchall()
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in autobiography:
                print(i)
            mydb.commit()
            
        if i=='3':
            print('\nYoung Adult/Teen\n')
            cur.execute('select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookGenre="Young Adult/Teen"')
            teen=cur.fetchall()
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in teen:
                print(i)
            mydb.commit()
            
        if i=='4':         
            print('\nFiction\n')
            cur.execute('select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookGenre="Fiction"')
            fiction=cur.fetchall()
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in fiction:
                print(i)
            mydb.commit()
            
        if i=='5':
            print('\nClassic\n')
            cur.execute('select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookGenre="Classic"')
            classic=cur.fetchall()
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in classic:
                print(i)
            mydb.commit()
            
        if i=='6':
            print('\nFantasy\n')
            cur.execute('select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookGenre="Fantasy"')
            fantasy=cur.fetchall()
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in fantasy:
                print(i)
            mydb.commit()
            
        if i=='7':
            print('\nManga\n')
            cur.execute('select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookGenre="Manga"')
            manga=cur.fetchall()
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in manga:
                print(i)
            mydb.commit()
    cart(username)

def search(username):
    print('How do you wish to search?')
    print('\n1.Search by author\n2.Search by title\n3.Search by genre')
    by=int(input('Enter the option:'))
    if by==1:
        ser1=input('Enter what you wish to search...')
        cur.execute("select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookAuthor like '%{}%'".format(ser1))
        res=cur.fetchall()
        if len(res)==0:
            print('Sorry,No books found for your search')
            print('Returning to search menu...\n')
            close_after_1_Sec()
            search(username)
        else:
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in res:
                print(i)
            cart(username)
    if by==2:
        ser2=input('Enter what you wish to search...')
        cur.execute("select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookName like '%{}%'".format(ser2))
        res=cur.fetchall()
        if len(res)==0:
            print('Sorry,No books found for your search')
            print('Returning to search menu...\n')
            close_after_1_Sec()
            search(username)
        else:
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in res:
                print(i)
            cart(username)            
    if by==3:
        ser3=input('Enter what you wish to search...')
        cur.execute("select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookGenre like '%{}%'".format(ser3))
        res=cur.fetchall()
        if len(res)==0:
            print('Sorry,No books found for your search')
            print('Returning to search menu...\n')
            close_after_1_Sec()
            search(username)
        else:
            column_names = [i[0] for i in cur.description]
            print(column_names)
            print('\n')
            for i in res:
                print(i)
            cart(username)
    
def date():
        import datetime
        return datetime.date.today()
    
def  buy2(username,bkno):
    qty=int(input('Enter quantity of the book you have chosen'))
    current_date=date()
    buy2=f'insert into buy(BookID,BookName,Qty,TotalPrice,username,Date)values((select distinct BookID from cart where BookID={bkno}),(select distinct BookName from cart where BookID={bkno}),{qty},(select distinct BookPrice from cart where BookID={bkno})*{qty},"{username}","{current_date}")'
    cur.execute(buy2)
    mydb.commit()
    print('Your Order is Processing...')
    close_after_1_Sec()
    cur.execute(f'update books set  BookQuantity= BookQuantity-{qty}')
    cur.execute(f'delete from cart where BookID={bkno} and username="{username}"')
    mydb.commit()
    print('The Order is Successful, You will recieve your item in three working days.')
    order=f'select OrderID from buy where username="{username}"and Date="{current_date}" and BookID={bkno}'
    cur.execute(order)
    ordrno=cur.fetchall()
    for orderno in ordrno:
        for i in orderno:
            print('\nYour order number is',i)
    mydb.commit()
    print('\nredirecting you back to menu.....')
    close_after_1_Sec()
    main_menu(username)

def buy(username):
    buy=input('Are you ready to buy?(y/n)')
    if buy.lower()=='y':
        print('\n---- Your Cart ----')
        check=f'select distinct BookID,BookName,BookPrice,Date from cart where username="{username}"'     
        cur.execute(check)
        cart1=cur.fetchall()
        if len(cart1)==0:
            print('   Your Cart is Empty!   ')
            print('Redirecting to menu...')
            close_after_1_Sec()
            main_menu(username)
        if len(cart1)==1:
            column_names = [i[0] for i in cur.description]
            print(column_names)
            for book in cart1:
                print(book)
            bkn=f'select BookID from cart where username="{username}"'
            cur.execute(bkn)
            bkn1=cur.fetchall()
            for i in bkn1:
                for bkno1 in i:
                    user_details(username)
                    buy2(username,bkno1)
        else:
            column_names = [i[0] for i in cur.description]
            print(column_names)
            for book in cart1:
                print(book)
            bkno2=int(input('Enter Book ID of the book you wish to choose'))
            query2=f'select distinct BookID,BookName,BookPrice,Date from cart where username="{username}" and BookID=%s'
            cur.execute(query2,(bkno2,))
            select_book=cur.fetchone()
            print('\nThe book you have selected is\n')
            for chosen in select_book:
                print(chosen,end=' ')
            mydb.commit()
            user_details(username)
            buy2(username,bkno2)

    if buy.lower()=='n':
        main_menu(username)
    else:
        print('Wrong Option......redirecting to menu')
        close_after_1_Sec()
        main_menu(username)

def cart(username):

    print('\n')
    bookno=int(input('Enter Book ID of the Book you wish to choose'))
    out_of_stock(bookno)
    query1=f"select BookID,BookName,BookAuthor,BookRating,BookGenre,BookPrice from books where BookID={bookno}"
    cur.execute(query1)
    selected_book=cur.fetchall()
    column_names = [i[0] for i in cur.description]
    print('\n')
    for chosen in selected_book:
        print('\nThe book you have selected is\n',column_names,'\n',chosen)   
    mydb.commit()
    book = "select BookName, BookPrice from books where BookID = %s"
    cur.execute(book, (bookno, ))
    result = cur.fetchone()
    cur_date = date()
    cart  = f"insert into cart(BookID, BookName, BookPrice, username, Date) values({bookno}, '{result[0]}',  {result[1]}, '{username}', '{cur_date}')"
    cur.execute(cart)
    mydb.commit()
    cont=input('Do you wish to continue browsing books?(yes/no)')
    if cont.lower()=='yes':
        main_menu(username)
    elif cont.lower()=='no':
        buy(username)
    else:
        print('Wrong Option!...Redirecting to menu......\n')
        close_after_1_Sec()
        main_menu(username)
        
        
def order_search(username):
    order_id=int(input('Enter your Order ID:'))
    user_order=f'select BookID,BookName,Qty,TotalPrice,Date from buy where OrderID={order_id}'
    cur.execute(user_order)
    userorder=cur.fetchall()
    column_names = [i[0] for i in cur.description]
    for i in userorder:
        print('Your order is:\n')
        print(column_names)
        print(i)
        
def cover():
    print('\nWelcome to our software\n|||||\n',
        """        ░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░░▒▓███████▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
        ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░ ░▒▓█▓▒▒▓█▓▒░░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░  ░▒▓██████▓▒░  
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░ 
        ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▓█▓▒░ ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░ 
        ░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░  ░▒▓██▓▒░  ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░    ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░ """,'\n|||||')
        
                                                                                                                                                             
                                                                                                                                                                    
    close_after_1_Sec()

    print('\nYour book adventure starts now....')
    close_after_1_Sec()
    

def close_after_1_Sec():
    import time
    time.sleep(0.5)

    
def menu():
    print("""       __          
|\ /| |   | | |  | 
| < | |<< |\| |  | 
|   | |__ | | '<<'""","\n\n")
    print('1.Register\n2.Login\n3.Admin\n4.Exit\n')
    op=int(input('Enter the choice you would like to choose: '))
    if op==1:
        print('\n')
        register()
        print('\n')
    elif op==2:
        login()
        print('\n')
    elif op ==3:
        admin()
        print('\n')
    elif op ==4 :
        import sys
        exit
    else:
        print("!!!! Wrong choice !!!!")
        print('Returning to menu...')
        close_after_1_Sec()
        menu()

def main_menu(username):
    print('\nDo you wish to\n1.Browse Books\n2.Search Books\n3.Cart and Checkout\n4.View Order Details\n5.Log Out\n')
    op=int(input('Choose your option:'))
    if op==1:
        print('\n')
        browse(username)
        print('\n')
    elif op==2:
        search(username)
        print('\n')
    elif op==3:
        buy(username)
        print('\n')
    elif op==4:
        order_search(username)
        print('Returning to menu...')
        close_after_1_Sec()
        main_menu(username)
    elif op==5:
        print('\n')
        print('Thank you for choosing us')
        print('Logging out...')
        close_after_1_Sec()
        menu()
    else:
        print('Wrong option!, Redirecting to menu....')
        close_after_1_Sec()
        menu()
cover()
menu()
