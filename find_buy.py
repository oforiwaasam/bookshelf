from book_apis import *
from booksrun_prices import *


def get_info_by_isbn(isbn, price_api_key):
  title, authors, cover_url = ol_isbn(isbn)
  json = booksrun_api_response(isbn, price_api_key)

  json_booksrun = from_booksrun(json)
  ebook_dict = get_ebook_prices(json_booksrun)
  if ebook_dict is not None or ebook_dict != 'none':
    ebook_price = ebook_dict['perpetual'][0]
    ebook_cart_url = ebook_dict['perpetual'][1]
    return title, authors, cover_url, ebook_price, ebook_cart_url
  else:
    return title, authors, cover_url

  
def lowest_used_book_price(booksrun_prices, others_prices, json_isbndb):
  used_booksrun = used_lowest_price(booksrun_prices, others_prices)
  used_isbndb = i_lowest_used_price(json_isbndb)
  used_isbndb_tuple = used_isbndb.items()
#   if used_booksrun is not None and used_isbndb is not None:
#     if used_booksrun['BooksRun.com'] < used_isbndb:
#       return used_booksrun
#   else:
    return used_isbndb

  
def lowest_new_book_price(booksrun_prices, others_prices, json_isbndb):
  new_booksrun =  new_lowest_price(booksrun_prices, others_prices)
  new_isbndb = i_lowest_new_price(json_isbndb)
  if new_booksrun < new_isbndb:
    return new_booksrun
  else:
    return new_isbndb

def lowest_ebook_price
  
  
def main():
  isbn = "9780132576277"
  price_api_key = "8mhw4i56nn5p1kasxdyu"
  print(get_info_by_isbn(isbn, price_api_key))

if __name__ == '__main__':
  main()
  
  
  
