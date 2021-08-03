#Imported files from other external sources
from flask import Flask, render_template,  url_for, flash, redirect,request
from flask_sqlalchemy import SQLAlchemy
# Imported Files from our folder
from forms import RegistrationForm, LoginForm
from login_manager import Login_Manager
from encryption import *
from book_apis import *
from bestsellers import *
from isbndb_prices import get_data
from databases import *
from sending_emails import *


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

class Book:
    def __init__(self):
        self.key = ''
        self.other_books = {}
        self.home_search = ''
        
book = Book()
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    top_books, book.other_books = homepage_bestsellers()
#     book.other_books = top_books
    if request.method=='POST':
        book.key = request.form.get("q")
        book.other_books = ol_book_names(book.key)
        return render_template('search.html',button="Books", books=book.other_books, top_books=top_books)
    return render_template('home.html',top_books=top_books)


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
        
        # creating a user instance in user_data table
        new_user(user.id, user.username, user.email)
        
        receiver = user.email
        body = "Thank you for registering with Bookshelf!"
        subject = "Successful Registration!"
        html = '<a href="https://bookshelfaacdl.herokuapp.com/"><br />Bookshelf</a>'
        
        # sending an email to a user who registers
        sending_email(user.email, subject, body, html)
        
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
                           text= theText, 
                           username=log_manage.get_username())

# helper fun for book_page
def lookforbook(other_books,name):
    if(isinstance(other_books, dict)):
        for key,value in other_books.items():
            if(name in key ):
                return key, value
    else:
        for elem in other_books:
#             print(elem)
            for key,value in other_books.items():
                if(name in key ):
                    return key, value
    return None, [None,None,None,None] #in case it does not work for now -> make exception later on
            

@app.route("/book_page/<path:key>", methods=['GET'])
def book_page(key):
    cover, book_data = lookforbook(book.other_books,key)
#     print(book_data[1], book_data[3])
#     author = ''.join(book_data[1])
    # [listed_price,lowest_ebook,lowest_used,lowest_new,lowest_rental]  
    prices = get_data(book_data[3])
    if prices==None:
        return render_template('book_page.html', book_title=book_data[0], author=book_data[1], web=book_data[2], cover=cover, recs = book.other_books)

    return render_template('book_page.html', book_title=book_data[0], author=book_data[1], web=book_data[2], cover=cover, recs = book.other_books, prices=prices)


@app.route("/search_best_seller/<string:category>", methods=['GET', 'POST'])
def search_best_seller(category):
#     print(category)
    book.other_books = select_category(category)
#     if request.method=='POST':
#         book.key = request.form.get("q")
#         book.other_books = ol_book_names(book.key)
# #         book.name = "Book1"
# #         book.other_books = {"Book1":["book_title", "authors_list", "cover_url", "url"], "Book2":["book_title", "authors_list", "cover_url", "url"], "Book3":["book_title", "authors_list", "cover_url", "url"],"Book32":["book_title", "authors_list", "cover_url", "url"]}
#         return render_template('search.html',button="Book", books=book.other_books)
        
    return render_template('search.html',button="Books", books=book.other_books)


@app.route("/search", methods=['GET', 'POST'])
def search():
    book.other_books = select_category("Hardcover Fiction")
    if request.method=='POST':
        book.key = request.form.get("q")
        if log_manage.is_logged_in():
            username = log_manage.get_username()
            update_search_history(username, 'Book', book.key)

        book.other_books = ol_book_names(book.key)
#         book.name = "Book1"
#         book.other_books = {"Book1":["book_title", "authors_list", "cover_url", "url"], "Book2":["book_title", "authors_list", "cover_url", "url"], "Book3":["book_title", "authors_list", "cover_url", "url"],"Book32":["book_title", "authors_list", "cover_url", "url"]}
        return render_template('search.html',button="Book", books=book.other_books)
        
    return render_template('search.html',button="Book", books=book.other_books)

@app.route("/search_author", methods=['GET', 'POST'])
def search_author():
    if request.method=='POST':
        book.key = request.form.get("q")
        
        if log_manage.is_logged_in():
            username = log_manage.get_username()
            update_search_history(username, 'Author', book.key)
        
        search = ol_authors(book.key)
        if(search[0]==0):
            book.other_books = search[1]
#             print(book.other_books)
            return render_template('search.html',button="Author", books=book.other_books)
        else:
            return render_template('search.html',button="Author", subtitle=f'Did you mean.. {search[1]}', books={})
        
    return render_template('search.html',button="Author", books={})

@app.route("/search_ISBN", methods=['GET', 'POST'])
def search_ISBN():
    print("search_ISBN")
    if request.method=='POST':
        book.key = request.form.get("q")
        
        if log_manage.is_logged_in():
            username = log_manage.get_username()
            update_search_history(username, 'ISBN', book.key)
        
        book.other_books = ol_isbn(book.key)
        return render_template('search.html',button="ISBN", books=book.other_books)
    return render_template('search.html',button="ISBN", books={})

@app.route("/search_topics", methods=['GET', 'POST'])
def search_topics():
    print("search_topics")
    if request.method=='POST':
        book.key = request.form.get("q")
        
        if log_manage.is_logged_in():
            username = log_manage.get_username()
            update_search_history(username, 'Topic', book.key)
        
        book.other_books = ol_subjects(book.key)
        return render_template('search.html',button="Topics", books=book.other_books)
    return render_template('search.html',button="Topics", books={})

@app.route("/search_open_ID", methods=['GET', 'POST'])
def search_open_ID():
    print("search_open_ID")
    if request.method=='POST':
        book.key = request.form.get("q")
        book.other_books = ol_work_id(book.key)
        return render_template('search.html',button="ID", books=book.other_books)
        
    return render_template('search.html',button="ID", books={})
  
@app.route("/bestsellers", methods=['GET', 'POST'])
def bestsellers():
    print("search_open_ID")
    if request.method=='POST':
        book.key = request.form.get("q")
        book.other_books = ol_work_id(book.key)
        return render_template('bestsellers.html', books=book.other_books)
        
    return render_template('bestsellers.html', books={})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
