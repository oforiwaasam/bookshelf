#Imported files from other external sources
from flask import Flask, render_template,  url_for, flash, redirect,request
from flask_sqlalchemy import SQLAlchemy
# Imported Files from our folder
from forms import RegistrationForm, LoginForm
from login_manager import Login_Manager
from encryption import *
from book_apis import *
from bestsellers import *
#from isbndb_prices import get_data
from databases import *
from sending_emails import *
from multiple_sources_prices import *




app = Flask(__name__)
app.config['SECRET_KEY'] = '182a078b8ed4e78614ce382d20b0ce1e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

icons = [(0,"https://lh3.googleusercontent.com/proxy/KhROWQZH_lpON6zZA_R7l5YSGm1FHDd0qd1OpnVkbr2eD-ePoiOsc_aF_U6w2zPVnhHOHR317-j7xTiGu-QrnO8W"),
    (1,"data:image/jpeg;base64,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"),
        (2,"https://www.vippng.com/png/detail/45-453141_clip-art-library-download-desktop-icons-purple-icon.png"),
        (3,"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5x7kCFXefkoWvMYGyUWTkIjADdVFeqXkakw&usqp=CAU")]

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
        self.book_stack = {"Recent":{},"Selected":{},"Favorite":{}}
        self.image = icons[0][1]

book = Book()
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    top_books, book.other_books = homepage_bestsellers()
    book.book_stack["Recent"] = book.other_books
#     book.other_books = top_books
    if request.method=='POST':
        book.key = request.form.get("q")
        book.other_books = ol_book_names(book.key)
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
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
            return render_template('registration.html', title='Register', form=form)
        
        # Check database if email is already in use
        exist_user = User.query.filter_by(email=form.email.data).first()
        if exist_user is not None:
            flash(f'Email {exist_user.email} is already taken', 'danger')
            return render_template('registration.html', title='Register', form=form)
        
        # User can be registered
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password= encrypt_password(form.password.data))
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}!', 'success')
        
        # creating a user instance in user_data table
        #new_user(user.id, user.username, user.email)
        
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

#helpers for user page
def make_shelves(shelves): #{"Recent":{book_data},"Selected":{book_data}}
    cmplt = []
    for name,bookshelf in shelves.items():
        print("JBCOWDNCXKWMXPWKMXKLNSJBCDHSBCDHEREE")
        slide = make_slide_show(bookshelf)
        cmplt.append((name,slide))
#         for key,value in bookshelf.items()
#             cmplt.append((key,value))
    return cmplt

def make_slide_show(bookshelve):
    count = 0
    total_count =0
    lst = []
    temp = []
    length = len(bookshelve.keys())
    for key,value in bookshelve.items():
        temp.append((key,value))
        count+=1  
        total_count+=1
        print("length", total_count, length)
        if(count==3):
            lst.append(temp)
            temp=[]
            count=0
        elif(total_count==length):
            lst.append(temp)
            temp=[]
            count=0
                  
        
        
    return lst
        
@app.route("/user", methods=['GET', 'POST'])
def user(): #uncomment when finished
#     form = LoginForm()
#     if log_manage.is_logged_in():
        bookstack=make_shelves(book.book_stack)
        theText = 'User: {}, email: {}'.format(
            log_manage.get_username(),log_manage.get_email())
        if(request.method=='POST'):
            image = request.form.get("q")
        return render_template('user.html', subtitle='User Page',
                           text= theText, 
                           username=log_manage.get_username(),bookstack=bookstack, image=book.image, image_lst=icons)
@app.route("/set_profile/<string:count>", methods=['GET','POST'])
def set_profile(count):
    print(count)
    book.image = icons[int(count)]
    bookstack=make_shelves(book.book_stack)
    theText = 'User: {}, email: {}'.format(
        log_manage.get_username(),log_manage.get_email())
    image = request.form.get("q")
    return render_template('user.html', subtitle='User Page',
                           text= theText, 
                           username=log_manage.get_username(),bookstack=bookstack, image=book.image, image_lst=icons)
            

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
            

@app.route("/book_page/<path:key>", methods=['GET','POST'])
def book_page(key):
    cover, book_data = lookforbook(book.other_books,key)
    # [listed_price,lowest_ebook,lowest_used,lowest_new,lowest_rental]  
    prices = get_data(book_data[3])
    if(cover!=None and (cover not in book.book_stack["Selected"].keys())):
        print("COVERCOVERCOVER", cover)
        book.book_stack["Selected"].update({cover:book_data})
    if(request.method=='POST'):
        if(cover!=None and (cover not in book.book_stack["Favorite"].keys())):
            book.book_stack["Favorite"].update({cover:book_data})
    if prices==None:
        return render_template('book_page.html', book_title=book_data[0], author=book_data[1], web=book_data[2], cover=cover, recs = book.other_books)

    return render_template('book_page.html', book_title=book_data[0], author=book_data[1], web=book_data[2], cover=cover, recs = book.other_books, prices=prices)


@app.route("/search_best_seller/<string:category>", methods=['GET', 'POST'])
def search_best_seller(category):
#     print(category)
    book.other_books = select_category(category)
    book.book_stack["Recent"] = book.other_books
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
    if(len(book.other_books.keys())==0):
        flash("Sorry No Books",'error')
    book.book_stack["Recent"] = book.other_books
    if request.method=='POST':
        book.key = request.form.get("q")
        if log_manage.is_logged_in():
            username = log_manage.get_username()
            update_search_history(username, 'Book', book.key)

        book.other_books = ol_book_names(book.key)
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
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
            print("IN HERE")
            book.other_books = search[1]
            if(len(book.other_books.keys())==0):
                flash("Sorry No Books",'error')
            book.book_stack["Recent"] = book.other_books
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
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
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
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
        return render_template('search.html',button="Topics", books=book.other_books)
    return render_template('search.html',button="Topics", books={})

@app.route("/search_open_ID", methods=['GET', 'POST'])
def search_open_ID():
    print("search_open_ID")
    if request.method=='POST':
        book.key = request.form.get("q")
        book.other_books = ol_work_id(book.key)
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
        return render_template('search.html',button="ID", books=book.other_books)
        
    return render_template('search.html',button="ID", books={})
  
@app.route("/bestsellers", methods=['GET', 'POST'])
def bestsellers():
    print("search_open_ID")
    if request.method=='POST':
        book.key = request.form.get("q")
        book.other_books = ol_work_id(book.key)
        if(len(book.other_books.keys())==0):
            flash("Sorry No Books",'error')
        book.book_stack["Recent"] = book.other_books
        return render_template('bestsellers.html', books=book.other_books)
        
    return render_template('bestsellers.html', books={})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
