import config
import requests
import json

def bestsellers_category():
  url = 'https://api.nytimes.com/svc/books/v3/lists/names.json?&api-key=' + config.api_key
  response = requests.get(url)
  results = response.json()['results']
  for name_dict in results:
    print(name_dict['list_name'] + ': ' + name_dict['list_name_encoded'])
  

def select_category():
  #user_input = input('Enter a book category: ')
  url = 'https://api.nytimes.com/svc/books/v3/lists/current/' + user_input + '.json?&api-key=' + config.api_key

  output = requests.get(url)
  data = output.json()
  print(data['results']['books'])

  for book in data['results']['books']:
    rank = book['rank']
    isbn10 = book['primary_isbn10']
    isbn13 = book['primary_isbn13']
    publisher = book['publisher']
    title = book['title']
    author = book['author']
    book_image = book['book_image']
    buy_links = book['buy_links']

    print(rank, isbn10, isbn13, publisher, title, author, book_image, buy_links)
    
    
def homepage_bestsellers():
  homepage_url = 'https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?&api-key=' + config.api_key
  response = requests.get(homepage_url)
  book_list = response.json()
  book_dic = {}
  for book in book_list['results']['books']:
    rank = book['rank']
    isbn10 = book['primary_isbn10']
    isbn13 = book['primary_isbn13']
    publisher = book['publisher']
    title = book['title']
    author = book['author']
    book_image = book['book_image']
    buy_links = book['buy_links']
  
    book_dic[book_image] = [title, author, buy_links]
  #print(book_list['results']['books'])
  #print(book_dic)
  return book_dic


def main():
  #homepage_bestsellers()
  #bestsellers_category()
  select_category()

  
if __name__ == "__main__":
  main()
