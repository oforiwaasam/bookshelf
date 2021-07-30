from book_apis import *
from booksrun_prices import *

def get_info_by_isbn(isbn, price_api_key):
  title, authors, cover_url = ol_isbn(isbn)
  json = booksrun_api_response(isbn, price_api_key)
  print(json)
  json_booksrun = from_booksrun(json)
  ebook_dict = get_ebook_prices(json_booksrun)
  if ebook_dict is not None or ebook_dict != 'none':
    ebook_price = ebook_dict['perpetual'][0]
    ebook_cart_url = ebook_dict['perpetual'][1]
    return title, authors, cover_url, ebook_price, ebook_cart_url
  else:
    return title, authors, cover_url

def main():
  isbn = "9780132576277"
  price_api_key = "8mhw4i56nn5p1kasxdyu"
  print(get_info_by_isbn(isbn, price_api_key))

if __name__ == '__main__':
  main()
  
  
  
