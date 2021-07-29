import requests


# Open Library Books API
# searching by ISBN number for now
def ol_books(isbn):
    
    result = requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:' +
                          isbn + '&jscmd=data&format=json')
    result_json = result.json()
    # print(result_json)
    data = result_json['ISBN:' + isbn]
    print(data['title'])
    for author in data['authors']:
        print(author['name'])
    # print(data)


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


def main():
    isbn = '9780980200447'
    mill_isbn = '9780199670802'
    data_structures = '9780132576277'
    aquarium = '9780793820788'
    petit_pays = '9782246857334'
    buildings = '9781564588852'
    cinderella_murder = '9781476763699'
    blackout = '9781982133276'
    ol_books(blackout)

    author = 'Manan Ahmed Asif'
    ol_authors(author)


if __name__ == "__main__":
    main()
