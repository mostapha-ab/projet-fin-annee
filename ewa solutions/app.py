from flask import Flask , render_template , url_for , request , redirect , url_for , session 
from flask_sqlalchemy import SQLAlchemy


from flask_wtf import Form
from wtforms import StringField , PasswordField , SelectField
from wtforms.validators import InputRequired , Email , Length
from sqlalchemy.exc import IntegrityError





app = Flask(__name__)
app.config['SECRET_KEY'] = "hellooooooooo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "hello"


import datetime

#----------------------------------------------

class SignForm(Form):
    username = StringField('Full Name:', validators=[InputRequired() , Length(min=5 , max=20)] )
    userville = SelectField('Ville:',choices = ['Casablanca', 'Fés','Tanger','Marrakech' , 'Salé', 'Meknès','Rabat' , 'Oujda', 'Agadir','Tétouan','	El Jadida', 'Other'])
    userstatus = SelectField('Status' , choices = ['Freelancer', 'Employer','Student','Other'] )
    userfield = SelectField('field' , choices = ['Dev','Web Design'] )
    usergender = SelectField('Gender:', choices = ['Male', 'Female'])
    useremail = StringField('Email', validators=[InputRequired(), Email(message="i dont like you")])
    userpassword = PasswordField('Password',validators=[InputRequired() , Length(min=5,max=10)])





#----------------------------------------------

class EditForm(Form):
    editname = StringField('Full Name:', validators=[InputRequired() , Length(min=5 , max=20)] )
    editville = SelectField('Ville:',choices = ['Casablanca', 'Fés','Tanger','Marrakech' , 'Salé', 'Meknès','Rabat','Other' , 'Oujda', '	Agadir','Tétouan','	El Jadida', 'Other'])
    editstatus = SelectField('Status' , choices = ['Freelancer', 'Employer','Student','Other'] )
    editemail = StringField('Email', validators=[InputRequired()])
    editpassword = PasswordField('Password',validators=[InputRequired() , Length(min=5,max=15)])

#----------------------------------------------





class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(20) , nullable=False )
    ville = db.Column(db.String(20) , nullable=False)
    status = db.Column(db.String(20) , nullable=False)
    field = db.Column(db.String(20) , nullable=False)
    gender = db.Column(db.String(20) , nullable=False)
    email = db.Column(db.String(20) , nullable=False , unique=True)
    password = db.Column(db.String(10) , nullable=False)

    def __init__(self,name,ville,status,field,gender,email,password):
        #self.id = id
        self.name = name
        self.ville = ville
        self.status = status
        self.field = field
        self.gender = gender
        self.email = email
        self.password = password


    def __repr__(self):
        return 'Blog Post' + (self.id) + self.name



#------------------Data base for our messages ----------------------------




class Msg(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    author = db.Column(db.String(20) , nullable=False )
    content = db.Column(db.String(20) , nullable=False , unique=True)

    def __init__(self,author,content):
        #self.id = id
        self.author = author
        self.content = content


    def __repr__(self):
        return 'Blog Post' + self.author 




#-----------------------------------

@app.route("/"  , methods = ["GET","POST"])
@app.route("/home"  , methods = ["GET","POST"])
def home():
    return render_template("index.html")





#-----------------------------------------


# to display this form we should pass it to template

@app.route("/sign" , methods = ["GET","POST"])
def sign():
    form = SignForm()
    if form.validate_on_submit() and request.method == "POST":
        username = request.form["username"] 
        userville = request.form["userville"] 
        userstatus = request.form["userstatus"] 
        userfield = request.form["userfield"] 
        usergender = request.form["usergender"] 
        useremail = request.form["useremail"]
        userpassword = request.form["userpassword"]

        foundUser = Student.query.all()

        for user in foundUser:
            if (user.name == username) and (user.email == useremail):
                return redirect(url_for("sign"))

        user = Student(name = username , ville = userville,status = userstatus,field = userfield,gender=usergender ,email=useremail ,password = userpassword)
        db.session.add(user)
        db.session.commit()


        return redirect(url_for("login"))


    return render_template("signin.html" , form = form)





#-----------------------------------

@app.route("/login" , methods = ["GET","POST"] )
def login():
    if request.method == "POST":
        name_email = request.form["name"]
        password = request.form["password"]

        if (name_email == "ewa") and (password == "@Agadir"):
            session["name_admine"] = name_email 
            return redirect(url_for("admin"))


        foundUser = Student.query.all()

        for user in foundUser:
            if ((name_email == user.name) or (name_email == user.email)) and (password == user.password):
                session["id"] = user.id
                session["name"] = user.name
                session["ville"] = user.ville
                session["status"] = user.status
                session["gender"] = user.gender
                session["email"] = user.email
                session["password"] = user.password

                # we should render to Dashboard page
                return redirect(url_for("dashboard"))

    return render_template("login.html")







#---------------- Dashboard -------------------




@app.route("/Dashboard" , methods = ["GET","POST"])
def dashboard():
    if 'name' in session:
        form = EditForm(editname=session.get("name") ,editville = session.get("ville")  ,editstatus = session.get("status") , editemail = session.get("email"))
        
        name = session.get("name")
        user = Student.query.filter_by(name=name).first()
        all_user = Student.query.all()
        # check if this person hav a message in message to change his name
        all_msg = Msg.query.all()

        if user and form.validate_on_submit() and  request.method == "POST":
            # now we should aceess the input
            name = request.form["editname"]
            ville = request.form["editville"]
            status = request.form["editstatus"]
            email = request.form["editemail"]
            password = request.form["editpassword"]

            for student in all_user:
                if (student.name == name) and (student.email == email):
                    return redirect(url_for("dashboard"))

            

            
                


            user.name = name
            user.ville = ville
            user.status = status
            user.email = email
            user.password = password  


            for msg in all_msg:
                if msg.author == session.get("name"):
                    msg.author = name


            session["name"] = name
            session["ville"] = ville
            session["status"] = status
            session["email"] = email
            session["password"] = password
            # now let's change the value of our session
            db.session.commit()   


            return redirect(url_for("dashboard"))


        return render_template("dashboard.html" ,form = form)
    
    # if a user just acess this page without login
    else:
        return redirect(url_for("login"))    


#--------------Messages---------------------------------

@app.route("/message" , methods=["POST","GET"])
def msg():
    if  ("name" in session):
        if request.method == "POST":
            content = request.form["message"]
            
            msg = Msg(author=session.get("name") , content = content)
            try:
                db.session.add(msg)
                db.session.commit()
                return redirect("/message")
            except IntegrityError:
                db.session.rollback()

            return redirect("/message")
            
        else:
            all_posts = Msg.query.all()
            all_users = Student.query.all()
            return render_template("message.html" , posts= all_posts , users = all_users)

    else:
        return redirect("login")
        




#--------------Log out Section---------------------------------

@app.route("/logout" , methods=["POST","GET"])
def logout():
    if ('name' in session) or ('name_admine' in session):
        if request.method == "POST":
            session.clear()
            return redirect(url_for("login"))
            
        else:
            return render_template("logout.html")    

    else:
        return redirect(url_for("login"))




@app.route("/hey")
def hey():
    name = session.get("name")
    return "hello " + name



#----------------------------------------------




@app.route("/admin")
def admin():
    if "name_admine" in session:


        #---------------------------------------Clcule Statistic-------------------------------------------------------
        all_users = Student.query.all()

        all_dev = Student.query.filter_by(field='Dev').all()

        len_dev = 0

        #-------------Now we get the number of all web develpers and designer

        for dev in all_dev :
            len_dev += 1

        session["numbersDev"] = len_dev    

        #---------------------------------------------------------------------

        #-----------------len of Males and female in Web Developpements and Percantages-------------------

        males_dev = 0
        females_dev = 0

        employers_dev = 0
        freelance_dev = 0

        #----------------Number of developper (employers and freelancers)---------------------
        for dev in all_dev:
            if dev.gender == "Male":
                males_dev += 1



            elif dev.gender == "Female":
                females_dev =+ 1



        #---------------------------------
        for free in all_dev:
            if dev.status == "Freelancer":
                freelance_dev =+ 1


        for emplo in all_dev:
            if emplo.status == "Employer":
                employers_dev =+ 1        

        #-------------------------------------


        session["employersDev"] = employers_dev 
        session["FreelanceDev"] = freelance_dev 

        #-------------------------------------

        perc_dev_male = 0
        perc_dev_female = 0

        if len_dev == 0:
            perc_dev_female = 0
            perc_dev_male = 0

        else:    
            perc_dev_male =  int( (males_dev * 100) / len_dev)
            perc_dev_female = int( (females_dev * 100) / len_dev)

        session["percDevMale"] = perc_dev_male 
        session["percDevFemale"] = perc_dev_female 

        #------------

        

        all_des = Student.query.filter_by(field='Web Design').all()

        len_des = 0

        #-------------Now we get the number of all web develpers and designer

        for des in all_des :
            len_des += 1

        session["numbersDes"] = len_des    

        #---------------------------------------------------------------------

        #-----------------len of Males and female in Web Developpements and Percantages-------------------

        males_des = 0
        females_des = 0

        employers_des = 0
        freelance_des = 0

        #----------------Number of developper (employers and freelancers)---------------------
        for des in all_des:
            if des.gender == "Male":
                males_des += 1



            elif des.gender == "Female":
                females_des =+ 1


        #---------------------------------
        for free in all_des:
            if des.status == "Freelancer":
                freelance_des =+ 1


        for emplo in all_des:
            if emplo.status == "Employer":
                employers_des =+ 1        

        #-------------------------------------


        session["employersDes"] = employers_des 
        session["FreelanceDes"] = freelance_des 

        #-------------------------------------

        perc_des_male = 0
        perc_des_female = 0

        if len_des == 0:
            perc_des_female = 0
            perc_des_male = 0

        else:    
            perc_des_male =  int( (males_des * 100) / len_des)
            perc_des_female = int( (females_des * 100) / len_des)

        session["percDesMale"] = perc_des_male 
        session["percDesFemale"] = perc_des_female 

        #----------------------------------------------------------------------------------------------

        #return "hey" + str(session.get("FreelanceDev"))
        return render_template("admin.html" , users = all_users)
    
    else:
        return redirect(url_for("login"))




@app.route("/admin/<int:id>")
def removeUser(id):
    user_found = Student.query.get(id)
    db.session.delete(user_found)
    db.session.commit()
    return redirect("/admin")







#---------------- This section edit it -------------------
# def calcule(employers_dev):
#     j = 0
#     for student in employers_dev:
#         j += 1
#     return j    


# @app.route("/info")
# def hey():
#     employers_dev = Student.query.filter_by(status='employer')

#     emplyers = calcule(employers_dev)
#     return "the numberof employers is " + str(emplyers)



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)