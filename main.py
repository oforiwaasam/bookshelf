#Imported files from other external sources
from flask import Flask, render_template,  url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

# Imported Files from our folder
from forms import RegistrationForm, LoginForm
from login_manager import Login_Manager
from encryption import *


app = Flask(__name__)
app.config['SECRET_KEY'] = '182a078b8ed4e78614ce382d20b0ce1e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Class model used to store User information
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.password}')"

#Create login manager object          
log_manage = Login_Manager()      


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # checks if entries are valid
        login_user = User.query.filter_by(username=form.username.data).first()
        
        # Username does not exist
        if login_user is None:
            flash(f'Username {form.username.data} does not exist!', 'danger')
            return render_template('login.html', title='Login', form=form)
        
        #Incorrect Password
        if not check_password_match(login_user.password, form.password.data):
            flash(f'Incorrect password ', 'danger')
            return render_template('login.html', title='Login', form=form)
        
        # Successful Login
        log_manage.login(login_user)
        flash(f'{form.username.data} successfully logged in!', 'success')
        return redirect(url_for('home')) # if so - send to home page

    return render_template('login.html', form=form)

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        # Check database if username is already in use
        exist_user = User.query.filter_by(username=form.username.data).first()
        if exist_user is not None:
            flash(f'Username {exist_user.username} is already taken', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # Check database if email is already in use
        exist_user = User.query.filter_by(email=form.email.data).first()
        if exist_user is not None:
            flash(f'Email {exist_user.email} is already taken', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # User can be registered
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password= encrypt_password(form.password.data))
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}!', 'success')
        
        return redirect(url_for('login'))   # Successfully registered now login
    return render_template('registration.html', form=form)

@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page')

@app.route("/user")
def user():
    theText = "No one logged in"
    if log_manage.is_logged_in():
        theText = 'User: {}, email: {}'.format(
            log_manage.get_username(),log_manage.get_email()) 
                    
    return render_template('user.html', subtitle='User Page',
                           text= theText)

@app.route("/search")
def search():
    return render_template('search.html', subtitle='Search Page')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
