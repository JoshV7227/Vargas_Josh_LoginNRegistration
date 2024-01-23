from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models import users_model
from icecream import ic
bcrypt = Bcrypt(app)






#------------------------------ CREATE USER

@app.route('/register', methods=['POST'])
def new_user():

    # REGISTRATION VALIDATION
    if not users_model.User.validate_registration(request.form):

        return redirect('/')
    

    #INSERTING INTO DATABASE
    new_guy = users_model.User.save_user(request.form)


    #STORING INFORMATION IN SESSION
    session['id'] = request.form['id']
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']

    #REDIRECTING TO SUCCESS PAGE
    return redirect('/success')






#------------------------------ LOGIN VALIDATION

@app.route('/login', methods=['POST'])
def login():

    #TAKING THE INFORMATION AND CHECKING TO SEE IF IT'S IN OUR DATABASE
    data = { "email" : request.form["email"] }
    our_user = users_model.User.get_by_email(data)


    # IF OUR USER IS NOT IN THE DATABASE, THEY WILL GET REDIRECTED TO THE MAIN PAGE
    if not our_user:
        flash("Invalid Email/Password")
        return redirect("/")
    
    # IF THE PASSWORD DOES NOT MATCH, REDIRECT TO MAIN PAGE
    if not bcrypt.check_password_hash(our_user.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    

    # IF PASSWORDS MATCHED, WE TAKE OUR USER'S INFO AND PUT IT INTO SESSION TO DISPLAY IT NEXT
    session['id'] = our_user.id
    session['first_name'] = our_user.first_name
    session['last_name'] = our_user.last_name

    #IF YOU'VE MADE IT THIS FAR, WE GO TO THE SUCCESS PAGE WHERE YOUR NAME WILL DISPLAY
    return redirect("/success")







#------------------------------ DISPLAY

@app.route('/success')
def display():
    
    if 'id' not in session:
        return redirect('/logout')
    #ONLY RENDERING TEMPLATE HERE
    return render_template('success.html')






#------------------------------ LOG OUT

@app.route('/logout')
def see_ya():

    #CLEARING SESSION TO LOG USER OUT
    session.clear()

    return redirect('/')