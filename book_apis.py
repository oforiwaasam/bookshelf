import requests


# Open Library Books API
# searching by ISBN number for now
def ol_books(isbn):
    result = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:' +
                          isbn + '&jscmd=data&format=json')
    result_json = result.json()
    # print(result_json)
    data = result_json['ISBN:' + isbn]
    print('Book title: ' + data['title'])
    authors_str = ''
    key = 'authors'
    if key in data:
        for author in data['authors']:
            authors_str += author['name'] + ', '
        size = len(authors_str)
        authors = authors_str[:size - 2]
        print('Author(s): ' + authors)
    else:
        print('Information on author(s) not available!')
    # print(data)


def ol_book_names(book):
    result = requests.get('http://openlibrary.org/search.json?q=' + book)
    result_json = result.json()
    print('First 20 results')
    print('----------------')
    num_books = 0
    for book in result_json['docs']:
        print(book)
        num_books += 1
        key = 'isbn'
        if key in book:
            if len(book['isbn']) > 1:
                book_isbn = book['isbn'][1]
            else:
                book_isbn = book['isbn'][0]

            # get book info using its isbn
            print('ISBN Number: ' + book_isbn)
            ol_books(book_isbn)
        else:
            print('Information about book not available!')
        if num_books == 20:
            break
    # print(result_json)


def ol_authors(author):
    result = requests.get('https://openlibrary.org/search/authors.json?q=' +
                          author)
    result_json = result.json()
    num_found = result_json['numFound']
    if num_found == 1:
        ol_id = result_json['docs'][0]['key']
        books = requests.get('https://openlibrary.org/authors/' + ol_id +
                             '/works.json')
        books_json = books.json()
        list_of_books = []
        for book in books_json['entries']:
            list_of_books.append(book['title'])
        print('Below are the books written by ' + author + ': ')

        # later transform this so that the brackets don't appear
        print(list_of_books)
    else:

        # figure out how to make sure that authors for whose names could be
        # written differently do not fall in this else statement

        print("Please enter the exact name of the author! Options below!!!")
        authors = []
        for author in result_json['docs']:
            authors.append(author['text'][1])
        print(authors)
        # print(result_json)


# figure out how this one works
def ol_work_id():
    result = requests.get('https://openlibrary.org/works/OL16563824W.json')
    result_json = result.json()
    print(result_json)


# figure out how I can get data from the work ID (refer to ol_work_id)
def ol_subjects():
    result = requests.get('https://openlibrary.org/subjects/bujumbura.json')
    result_json = result.json()
    print(result_json)


def main():
    # everything in main was used to test if functions work well
    isbn = '9780980200447'
    mill_isbn = '9780199670802'
    data_structures = '9780132576277'
    aquarium = '9780793820788'
    petit_pays = '9782246857334'
    buildings = '9781564588852'
    cinderella_murder = '9781476763699'
    
    blackout = '9781982133276'
    weird = '9780563533603'  # no info on author
    # ol_books(blackout)

    author = 'Ahmed Manan'
    # ol_authors(author)

    manan_book = 'Where the wild frontiers are'
    data_structures_book = 'Data Structures and Algorithm Analysis in Java'
    faye = 'Petit Pays'
    # ol_book_names(manan_book)

    # look into how to make the following functions work efficiently
        # ol_subjects()
        # ol_work_id()


if __name__ == "__main__":
    main()
