from flask import Flask, render_template, url_for, request, redirect, flash, session, Blueprint
from forms import RegistrationForm, LoginForm, Home_input
from flask_mysqldb import MySQL
# from flask_socketio import SocketIO, join_room, leave_room, namespace
import MySQLdb
from win10toast import ToastNotifier
from flask_mysqldb import MySQL
import time

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# socketio = SocketIO(app)

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= 'toor'
app.config['MYSQL_DB']= 'easy_homes'
app.config['MYSQL_CURSORCLASS']= 'DictCursor'

#app.secret_key= '#0330#'
#app.config['MYSQL_HOST']= '192.168.137.1'
#app.config['MYSQL_USER']= 'root'
#app.config['MYSQL_PASSWORD']= 'toor'
#app.config['MYSQL_DB']= 'emp'
#app.config['MYSQL_CURSORCLASS']= 'DictCursor'


    # Databases

'''db_admin = MySQLdb.connect("localhost","root","toor","admin" )
admin_cursor = db_admin.cursor() '''

db_owner = MySQLdb.connect("localhost","root","toor","easy_homes" )
owner_cursor = db_owner.cursor()

@app.route('/')
def Home():
    return render_template('home/home.html')



    ##      owner regestration

@app.route('/registration1', methods=['GET', 'POST'])

def signup():    
    form= RegistrationForm()
    if request.method == 'POST':
        uemail= form.email.data
        upass= form.password.data
        uname= form.username.data
        uphone= form.phone_no.data
        email= uemail
        boolean= True
        #cur = mysql.connection.cursor()


        try:
            owner_cursor.execute("""INSERT INTO owner (name, mail, password,phone_no)
                           VALUES (%s,%s,%s,%s)""", (uname, uemail, upass, uphone))
            db_owner.commit()
            db_owner.close()          
            error= 'sucessfull signup'  
            return render_template('signin.html',form= form, error= error)              
                            
        except:      
            error= 'Unsucessfull signup'  
            return render_template('signup.html',form= form, error= error)
    else:
            error= 'Apply Correct Credentials'
            return render_template('signup.html',form= form, error= error)   


##      owner login



@app.route('/login1', methods=['GET', 'POST'])

def signin():
    form= RegistrationForm()
    
    if request.method == 'POST':

        uemail= form.email.data
        upass= form.password.data
        boolean = True

        try:
            db_owner1 = MySQLdb.connect("localhost","root","toor","easy_homes" )
            owner_cursor1 = db_owner1.cursor()
            
            owner_cursor1.execute("select * from owner where mail='"+ uemail +"'  ")

            fetchdata = owner_cursor1.fetchone() 

 

            if fetchdata[5]== upass and fetchdata[3]== uemail:
                message= 'sucessfull login'
                flash(message)
                boolean= False

                session["owner_oid"]= fetchdata[0]   
                session["owner_name"]= fetchdata[1] 
                session["owner_gender"]= fetchdata[2]   
                session["owner_email"]= fetchdata[3]   
                session["owner_phone"]= fetchdata[4]  
                session["owner_pass"]= fetchdata[5]
                


                return render_template('owner_homepage.html', uemail= uemail, upass= upass, form= form)
            return render_template('signin.html', form= form)
        except:
            if boolean == True:
                error= 'incorrect user data'
                return render_template('signin.html', form= form, error= error)                       

    else:
        error= 'Apply Correct Credentials.'
        return render_template('signin.html',form= form, error= error)   




   ##     owner homepage ,  inputting  home details in db


@app.route('/add_house', methods=['GET', 'POST'])

def add_homes():
    form= RegistrationForm()
    if request.method == 'POST':

        bh= form.bhk.data    
        st= form.state.data      
        add= form.address.data   
        cty= form.city.data
        pin= form.pincode.data


        try:
            db_home = MySQLdb.connect("localhost","root","toor","easy_homes" )
            home_cursor = db_home.cursor()

            owner_id= session["owner_oid"]

            home_cursor.execute("""INSERT INTO home (oid, address, pincode, city, state, bhk)
                               VALUES (%s,%s,%s,%s,%s,%s)""", (owner_id, add, pin,cty, st, bh))
            # home_cursor.execute('''insert into  home (address, pincode, state, city) values(add, pin, st, cty); ''')
            db_home.commit()
            db_home.close()          
            alert('New house added..')
            error= 'Sucessfull Inputed Home'  
            return render_template('owner_homepage.html',form= form, error= error)
                            
        except:  
            error= 'Unsucessfull '  
            return render_template('owner_homepage.html',form= form, error= error)
    else:
            error= 'incorrect home details..'
            return render_template('owner_homepage.html',form= form, error= error)   

# def alert(item):
#     # One-time initialization
#         toaster = ToastNotifier()

#         # Show notification whenever needed

#         toaster.show_toast(item, "Alert!", threaded=True,
#                         icon_path=None, duration=7)  # 3 seconds
#         while toaster.notification_active():
#             time.sleep(0.1)





                #review houses



@app.route('/review_house', methods=['GET', 'POST'])

def review():
    form= RegistrationForm()

    try:
        review_home = MySQLdb.connect("localhost","root","toor","easy_homes" )
        review_cursor = review_home.cursor()

        owner_id= session["owner_oid"]
        idd= int(owner_id)
        query_string = "SELECT * FROM home WHERE oid = %s"
        review_cursor.execute(query_string, (idd,))
            
        result= review_cursor.fetchall()
        print(result)
        if result != None:   
            alert('Houses found please wait..')            
            return render_template('owner_home_review.html', result= result)
        else:        
            alert('No houses found')
            return render_template('owner_homepage.html',form= form)

    except:  
        alert('try block error')
        return render_template('owner_homepage.html',form= form)

# def alert(item):
#     # One-time initialization
#         toaster = ToastNotifier()

#         # Show notification whenever needed

#         toaster.show_toast( "Easy Homes", item, threaded=True,
#                         icon_path=None, duration=7)  # 3 seconds
#         while toaster.notification_active():
#             time.sleep(0.1)



                # owner profile update below



@app.route('/update_profile', methods=['GET', 'POST'])

def update_owner():

    form= RegistrationForm()  
    owner_id= session["owner_oid"]
    owner_name= session["owner_name"] 
    owner_gender= session["owner_gender"]   
    owner_phone= session["owner_phone"]  
                 
    owner_email = session['owner_email']
    owner_pass = session['owner_pass']

    return render_template('owner_update.html',n= owner_name, i= owner_id,
        g= owner_gender, ph= owner_phone, pa= owner_pass, e= owner_email)    


    if request.method == 'POST':

        owner_email = session['owner_email']
        owner_pass = session['owner_pass']

        db_renter1 = MySQLdb.connect("localhost","root","toor","easy_homes" )
        renter_cursor1 = db_renter1.cursor()
        try:
            
            # renter_cursor1.execute("select * from renter where mail='"+ owner_mail +"'  ")
            # fetchdata = renter_cursor1.fetchone() 

            # print(fetchdata[2])     
            # print(fetchdata[3])  
            print("mail" + owner_email)
            print("pass" + owner_pass)
            return render_template('owner_update.html', p= owner_pass, m= owner_email)    

        except:  
            error= 'Updatre not shown '  
            return render_template('owner_homepage.html', form= form, error= error)    


    else:
        error= 'provide details'
        return render_template('owner_homepage.html',form= form, error= error)   





#   ----------------- RENTER Registration -----------------------------------------



@app.route('/renter_registration', methods=['GET', 'POST'])

def renter_signup():    
    form= RegistrationForm()
    if request.method == 'POST':
        remail= form.email.data
        upass= form.password.data
        uname= form.username.data
        uphone= form.phone_no.data
        boolean= True
        
        db_renter = MySQLdb.connect("localhost","root","toor","easy_homes" )
        renter_cursor = db_renter.cursor()

        try:
            renter_cursor.execute("""INSERT INTO renter (name, mail, passwor,phone_no)
                           VALUES (%s,%s,%s,%s)""", (uname, remail, upass, uphone))
            db_renter.commit()
            db_renter.close()          
            error= 'sucessfull signup'  
            return render_template('renter_home/r_signin.html',form= form, error= error)             
                            
        except:  
            error= 'Error Signing up'  
            return render_template('renter_home/r_signup.html',form= form, error= error)
    else:
            error= 'Apply Correct Credentials'
            return render_template('renter_home/r_signup.html',form= form, error= error)   


#   ----------------- RENTER Login -----------------------------------------


@app.route('/renter_login', methods=['GET', 'POST'])

def renter_signin():
    form= RegistrationForm()
    if request.method == 'POST':

        uemail= form.email.data
        upass= form.password.data
        boolean = True

        db_renter1 = MySQLdb.connect("localhost","root","toor","easy_homes" )
        renter_cursor1 = db_renter1.cursor()
        try:
        
            renter_cursor1.execute("select * from renter where mail='"+ uemail +"'  ")
            fetchdata = renter_cursor1.fetchone() 
               
            if fetchdata[5]== upass and fetchdata[3]== uemail:
                message= 'sucessfull login'
                flash(message)
                boolean= False

                session["renter_rid"]= fetchdata[0]   
                session["renter_name"]= fetchdata[1] 
                session["renter_gender"]= fetchdata[2]   
                session["renter_email"]= fetchdata[3]   
                session["renter_phone"]= fetchdata[4]  
                session["renter_pass"]= fetchdata[5]
         
                return render_template('renter_home/renter_homepage.html', uemail= uemail, upass= upass, form= form)
            return render_template('renter_home/r_signin.html', form= form)
        except:
            if boolean == True:
                error= 'incorrect user data'
                return render_template('renter_home/r_signin.html', form= form, error= error)                       

    else:
        error= 'Apply Correct Credentials.'
        return render_template('renter_home/r_signin.html',form= form, error= error)   




   ##     renter homepage ,  fetching  home details


@app.route('/find_house', methods=['GET', 'POST'])

def find_homes():
    form= RegistrationForm()
    if request.method == 'POST':

        house_found= False
        pin= form.pincode.data
        cty= form.city.data
        fetch_home = MySQLdb.connect("localhost","root","toor","easy_homes" )
        fetch_cursor = fetch_home.cursor()       
        print(cty, pin)

           ## search by city
        try:
            query_string_1 = "SELECT * FROM home WHERE city = %s "
            fetch_cursor.execute(query_string_1, (cty, ))

            results= fetch_cursor.fetchall()
            print(results)

            if results[0] != None:
                house_found= True
                alert('Be patience while we search for houses..')                
                return render_template('renter_home/view_houses.html', results= results)
            else:
                alert('No houses found')
                return render_template('renter_home/renter_homepage.html', form= form)
                 
        except:  
            error= 'Enter valid  details'  
            alert('BE patience while we search for houses..')                
            return render_template('renter_home/renter_homepage.html',form= form, error= error)

          ## search by pincode
           
        finally:
            if house_found == False:
                query_string_1 = "SELECT * FROM home WHERE pincode = %s "
                fetch_cursor.execute(query_string_1, (pin, ))
                results= fetch_cursor.fetchall()
                return render_template('renter_home/view_houses.html', results= results)
                 
    else:
            error= '  Enter correct details..'
            return render_template('renter_home/renter_homepage.html',form= form, error= error)   

def alert(item):
    # One-time initialization
        toaster = ToastNotifier()

        # Show notification whenever needed

        toaster.show_toast(item, "Easy Homes!", threaded=True,
                        icon_path=None, duration=7)  # 3 seconds
        while toaster.notification_active():
            time.sleep(0.1)




@app.route('/renter_user_profile/<int:id>')
def user_profile_fun(id):
    id= str(id)    
    print(id)
    try:
        user_profile= MySQLdb.connect("localhost","root","toor","easy_homes" )
        user_profile_cursor= user_profile.cursor()

        query_string_2= "select * from owner where oid= %s "
        user_profile_cursor.execute(query_string_2, (id, ))
        profile= user_profile_cursor.fetchall()
        print(profile)
        return render_template('renter_home/profile.html', profile= profile)
    except:
        return render_template('renter_home/renter_homepage.html')

    # id= str(id)
    # cur= mysql.connection.cursor()
    # cur.execute("delete from empdata where id=" +id+" ")
    # mysql.connection.commit()
    # return redirect(url_for('Home') )
   

                # renter profile update below

@app.route('/update_profile_1', methods=['GET', 'POST'])

def update_renter():

    form= RegistrationForm()  
    renter_id= session["renter_rid"]
    renter_name= session["renter_name"] 
    renter_gender= session["renter_gender"]   
    renter_phone= session["renter_phone"]  
                 
    renter_email = session['renter_email']
    renter_pass = session['renter_pass']

    return render_template('renter_home/renter_update.html',na= renter_name, id= renter_id,
        ge= renter_gender, pho= renter_phone, pas= renter_pass, em= renter_email)    

                        # admin login

@app.route('/adminLogin', methods=['GET', 'POST'])

def adminLog():
    form= RegistrationForm()
    if request.method == 'POST':
        aname= form.username.data
        apass= form.password.data        
        try:
            if aname == "admin001" and apass == "root001":
                message= 'sucessfull login'
                flash(message)
                return render_template('admin/adminHome.html',  form= form)
            return render_template('admin/adminLogin.html', form= form)
        except:
                error= 'incorrect user data'
                return render_template('admin/adminLogin.html', form= form, error= error)                       

    else:
        error= 'Apply Correct Credentials.'
        return render_template('admin/adminLogin.html',form= form, error= error)   


                # admin renter table..

@app.route('/RenterTable', methods=['GET', 'POST'])
def RenterTable():
    
    form= RegistrationForm()
    try:
        RenterTable= MySQLdb.connect("localhost","root","toor","easy_homes" )
        RenterTable_cursor= RenterTable.cursor()

        RenterTable_cursor.execute("select * from renter")
        renter_table= RenterTable_cursor.fetchall()
        return render_template('admin/adminHome.html', results= renter_table)
    except:
        return render_template('admin/adminHome.html')

                # admin OwnerTable

@app.route('/OwnerTable', methods=['GET', 'POST'])
def OwnerTable():
    
    form= RegistrationForm()
    try:
        OwnerTable= MySQLdb.connect("localhost","root","toor","easy_homes" )
        OwnerTable_cursor= OwnerTable.cursor()

        OwnerTable_cursor.execute("select * from owner")
        owner_table= OwnerTable_cursor.fetchall()
        return render_template('admin/adminHome.html', results= owner_table)
    except:
        return render_template('admin/adminHome.html')

                # admin house Table


@app.route('/HomeTable', methods=['GET', 'POST'])
def HomeTable():
    
    form= RegistrationForm()
    try:
        HomeTable= MySQLdb.connect("localhost","root","toor","easy_homes" )
        HomeTable_cursor= HomeTable.cursor()

        HomeTable_cursor.execute("select * from home")
        house_table= HomeTable_cursor.fetchall()
        return render_template('admin/adminHome.html', results= house_table)
    except:
        return render_template('admin/adminHome.html')

        # delete data

@app.route('/delete/<int:id>')
def delete(id):
    del_id= int(id)
    print(del_id)
    try:
        delete_table= MySQLdb.connect("localhost","root","toor","easy_homes" )
        delete_table_cursor= delete_table.cursor()
        # cur= mysql.connection.cursor()
        # cur.execute("delete from renter where phone_no=" +del_id+" ")
        # mysql.connection.commit()

        # query_string_3 = "delete from renter where phone_no='+ del_id +' "
        # delete_table_cursor.execute(query_string_3)        

        delete_table_cursor.execute("delete from home where pincode = '+ del_id +' ")

        # query_string_3 = "delete from renter where rid= %s"
        # delete_table_cursor.execute(query_string_3, (del_id,))

        print('try')
        return redirect(url_for('HomeTable') )
    except:
        return redirect(url_for('HomeTable') )
        #pass

    # try:
    #     delete_table_1= MySQLdb.connect("localhost","root","toor","easy_homes" )
    #     delete_table_1_cursor= delete_table_1.cursor()

    #     delete_table_1_cursor.execute("delete * from home where oid='"+ del_id +"' ")
    #     print('ex')
    #     return redirect(url_for('HomeTable') )
    # except:
    #     print('owner')
    #     return redirect(url_for('RenterTable') )






                # socket -0------------------------------

# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received my event: ' + str(json))
#     room= json["room"]
#     socketio.emit('my response', json,
#                              room= room, callable=all(room) )

# def all(data):
#     print('data: '+ data)

# @socketio.on('all')
# def handle_my_custom_event():
#     print('received my event: ')    

mysql= MySQL(app)

if __name__=='__main__':
    app.run(debug= True)