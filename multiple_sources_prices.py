from book_apis import *
from booksrun_prices import *
from isbndb_prices import *

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
  if used_booksrun is not None and used_isbndb is not None:
      for key, value in used_booksrun.items():
        booksrun_price = value[0]
      for key, value in used_isbndb.items():
        isbndb_price = value[0]
      if float(booksrun_price) < float(isbndb_price):
          return used_booksrun
      else:
          return used_isbndb
  
  elif used_booksrun is None and used_isbndb is not None:
    return used_isbndb
  elif used_isbndb is None and used_booksrun is not None:
    return used_booksrun
  else:
    return None

  
def lowest_new_book_price(booksrun_prices, others_prices, json_isbndb):
  new_booksrun = new_lowest_price(booksrun_prices, others_prices)
  new_isbndb = i_lowest_new_price(json_isbndb)
  if new_booksrun is not None and new_isbndb is not None:
      for key, value in new_booksrun.items():
        booksrun_price = value[0]
      for key, value in new_isbndb.items():
        isbndb_price = value[0]
      if float(booksrun_price) < float(isbndb_price):
          return new_booksrun
      else:
          return new_isbndb
  
  elif new_booksrun is None and new_isbndb is not None:
    return new_isbndb
  elif new_isbndb is None and new_booksrun is not None:
    return new_booksrun
  else:
    return None
  

def lowest_ebook_price(ebook_prices, json_isbndb):
  ebook_booksrun = ebook_or_rental_lowest(ebook_prices)
  ebook_isbndb = i_lowest_ebook_price(json_isbndb)
  if ebook_booksrun is not None and ebook_isbndb is not None:
      for key, value in ebook_booksrun.items():
        booksrun_price = value[0]
      for key, value in ebook_isbndb.items():
        isbndb_price = value[0]
      if float(booksrun_price) < float(isbndb_price):
          return ebook_booksrun
      else:
          return ebook_isbndb
  
  elif ebook_booksrun is None and ebook_isbndb is not None:
    return ebook_isbndb
  elif ebook_isbndb is None and ebook_booksrun is not None:
    return ebook_booksrun
  else:
    return None


def lowest_rental_price(rental_prices, json_isbndb):
  rental_booksrun = ebook_or_rental_lowest(rental_prices)
  rental_isbndb = i_lowest_rental_price(json_isbndb)
  if rental_booksrun is not None and rental_isbndb is not None:
      for key, value in rental_booksrun.items():
        booksrun_price = value[0]
      for key, value in rental_isbndb.items():
        isbndb_price = value[0]
      if float(booksrun_price) < float(isbndb_price):
          return rental_booksrun
      else:
          return rental_isbndb
  
  elif rental_booksrun is None and rental_isbndb is not None:
    return rental_isbndb
  elif rental_isbndb is None and rental_booksrun is not None:
    return rental_booksrun
  else:
    return None


def setprices(prices):
    data = []
    names = ["Lowest Ebook","Lowest Used","Lowest New","Lowest Rental"]
    for elem in prices:
        count = elem[0]
        dic = elem[1]
        for key,value in dic.items():
            data.append((key,value[0],value[1],names[count]))
    return data

def get_data(ISBN):
    if ISBN is not None:
        data = []
        booksrun_api_key = "8mhw4i56nn5p1kasxdyu"
        isbn_api_key = "46445_4b9207100f7b3236200445a31f95a377"
        #isbn = input_isbn()
        json1 = booksrun_api_response(ISBN, booksrun_api_key)
        json2 = i_api_response(isbn_api_key, ISBN)

        json_booksrun = from_booksrun(json1)
        json_others = from_others(json1)

        paperbook_prices1 = get_booksrun_paperbook_prices(json_booksrun)
        paperbook_prices2 = get_others_paperbook_prices(json_others)
        ebook_prices = get_ebook_prices(json_booksrun)
        rental_prices = get_rentals_prices(json_booksrun)

        lowest_used = lowest_used_book_price(paperbook_prices1, paperbook_prices2, json2)
        lowest_new = lowest_new_book_price(paperbook_prices1, paperbook_prices2, json2)
        lowest_ebook = lowest_ebook_price(ebook_prices, json2)
        lowest_rental = lowest_rental_price(rental_prices, json2)
        temp = [lowest_ebook,lowest_used,lowest_new,lowest_rental]
        count = 0
        for elem in temp:
            if elem != None:
                data.append((count,elem))
            count+=1

        return setprices(data)


    
  
# def main():
# #   isbn = "9780132576277"
# #   booksrun_api_key = "8mhw4i56nn5p1kasxdyu"
# #   isbn_api_key = "46445_4b9207100f7b3236200445a31f95a377"
    
# #   js_mill_isbn = '9780199670802'
# #   data_structures = '9780132576277'
# #   aquarium = '9780793820788'
# #   petit_pays = '9782246857334'
# #   buildings = '9781564588852'
# #   cinderella_murder = '9781476763699'
# #   wrong_isbn = '1892sharabia'

# #   #isbn = input_isbn()
# #   json1 = booksrun_api_response(data_structures, booksrun_api_key)
# #   json2 = i_api_response(isbn_api_key, data_structures)
  
# #   json_booksrun = from_booksrun(json1)
# #   json_others = from_others(json1)

# #   paperbook_prices1 = get_booksrun_paperbook_prices(json_booksrun)
# #   paperbook_prices2 = get_others_paperbook_prices(json_others)
# #   ebook_prices = get_ebook_prices(json_booksrun)
# #   rental_prices = get_rentals_prices(json_booksrun)

# #   print(lowest_used_book_price(paperbook_prices1, paperbook_prices2, json2))
# #   print(lowest_new_book_price(paperbook_prices1, paperbook_prices2, json2))
# #   print(lowest_ebook_price(ebook_prices, json2))
# #   print(lowest_rental_price(rental_prices, json2))
#     data_structures = '9780132576277'
#     get_data(data_structures)
    
      

# if __name__ == '__main__':
#   main()
  
  
  
