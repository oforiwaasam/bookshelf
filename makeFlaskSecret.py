# makeFlaskSecret
# 
# File contains function that creates and prints a secret that can be copy
# and pasted for our app.config['SECRET_KEY'] variale in the mainfile. This 
# is so that the main.py is less cluttered
# 
# If this file is run it will print the secret key on terminal
#

import secrets

#function prints secret token
def print_secret():
    # gives secret key to copy+paste for our app.config['SECRET_KEY'] var
    print(secrets.token_hex(16))


if __name__ == '__main__':
    print_secret()