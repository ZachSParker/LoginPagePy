from flask_app import app
from flask import render_template, redirect, request, session,flash,url_for,flash
from flask_app.models.user import User # import your model files
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route('/')
def index():
    return redirect('/login')
@app.route('/register/process',methods = ['POST'])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/login')
    data = {"email":request.form['email']}
    user_in_db = User.check_credentials(data)
    if user_in_db:
        flash('Email already exists!')
        return redirect('/login') 
    if request.form['confirm_pw'] != request.form['password']:
        flash('passwords do not match')
        return redirect('/login')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
    }
    
    user_in_db = User.register_user(data)
    session['user_in_db'] = user_in_db
    
    return redirect('/login')

@app.route('/login')
def login_page():
    return render_template('Login.html')

@app.route('/login/process',methods = ['POST'])
def login_post():
    data = {"email":request.form['login_email']}
    user_in_db = User.check_credentials(data)
    print(user_in_db)
    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['login_pw']):
        flash('incorrect email/password')
        return redirect('/login')
    session['user_id'] = user_in_db.id
    flash('you have been registered, you may now login')
    return redirect('/dashboard')

@app.route('/dashboard')
def home_page():
    if 'user_id' not in session:
        return redirect('/login')
    user_id = User.get_one_by_id(session)
    return render_template('Home.html',user_id = user_id)