from flask import Flask, render_template

import secrets


# gives secret key to copy+paste for our app.config['SECRET_KEY'] var
# print(secrets.token_hex(16))

app = Flask(__name__)
app.config['SECRET_KEY'] = '980d348741e7e672e87f483676c3e912'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page')


@app.route("/login")
def login():
    return render_template('login.html', subtitle='Login Page')

@app.route("/registration")
def registration():
    return render_template('registration.html', subtitle='Registration Page')

@app.route("/about")
def about():
    return render_template('about.html', subtitle='About Page')

@app.route("/user")
def user():
    return render_template('user.html', subtitle='User Page')

@app.route("/search")
def search():
    return render_template('search.html', subtitle='Search Page')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")