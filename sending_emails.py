import yagmail


receiver = "ikiguma%73628@gmail.com"
body = "Thank you for registering with Bookshelf!"
subject = "Successful Registration!"
html = '<a href="https://bookshelfaacdl.herokuapp.com/"><br />Bookshelf</a>'

def sending_email(receiver, subj, body, html):

    yag = yagmail.SMTP("bookshelfaacdl", "&UD0$r?zirEHS'")
    yag.send(
        to=receiver,
        subject=subj,
        contents=[body, html]
    )

#sending_email(receiver, subject, body, html)
