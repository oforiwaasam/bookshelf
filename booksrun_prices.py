import requests


# The user inputs the ISBN of the book
def input_isbn():
    return input("Enter book ISBN: ")


# Getting the response from the API of Booksrun.com
def booksrun_api_response(isbn, api_key):
    url = "https://booksrun.com/api/v3/price/buy/" + isbn + "?key=" + api_key
    resp = requests.get(url)
    if resp.status_code == 200:
      json = resp.json()
      return json['result']['offers']
    else:
      return None



# prices given by Booksrun (usually no shipping fee)
def from_booksrun(json):
  if 'booksrun' in json:
    return json['booksrun']
  else:
    return None


# prices from third party sellers selling on Booksrun (there is usually a
# shipping fee)
def from_others(json):

  if 'marketplace' in json:
    return json['marketplace']
  else:
    return None



# prices of hard copy books sold by Booksrun
# return: prices and cart urls of used, new, and rented books
def get_booksrun_paperbook_prices(json_booksrun):
    buy_used = None

    if json_booksrun != None:
      buy_used = {}
      if json_booksrun['used'] != 'none':
          buy_used['BooksRun.com'] = json_booksrun['used']['price'], json_booksrun['used']['cart_url']

    buy_new = None
    if json_booksrun != None:
      buy_new = {}
      if json_booksrun['new'] != 'none':
          buy_new['BooksRun.com'] = json_booksrun['new']['price'], json_booksrun['new']['cart_url']


    return buy_used, buy_new


# prices of hard copy books sold by third party sellers on Booksrun
# return: prices and cart urls of used, new, and rented books
def get_others_paperbook_prices(json_marketplace):


    if json_marketplace != 'none' and json_marketplace != None:

        buy_used = []
        for element in json_marketplace:
            item = {}
            if element['used'] != 'none' and element['used'] != None:
                element['used']['price'] += element['shipping']
                key = 'condition'
                if key in element['used']:
                  del element['used']['condition']
                price_and_url = {}
                price_and_url['BooksRun.com'] = element['used']['price'], element['used']['cart_url']
                buy_used.append(price_and_url)

        buy_new = []
        for element in json_marketplace:
            item = {}
            if element['new'] != 'none' and element['new'] != None:
                element['new']['price'] += element['shipping']
                key = 'condition'
                if key in element['new']:
                  del element['new']['condition']
                price_and_url = {}
                price_and_url['BooksRun.com'] = element['new']['price'], element['new']['cart_url']
                buy_used.append(price_and_url)

        return buy_used, buy_new
    else:
        return None


# prices of ebooks sold by Booksrun
# return: prices, length of rent and cart urls of the ebooks
def get_ebook_prices(json_booksrun):
    ebook = None
    if json_booksrun != None:
      if json_booksrun['ebook'] != 'none' and json_booksrun['ebook'] != None:
          ebook = []
          for length, info in json_booksrun['ebook'].items():
              to_append = {}
              to_append['BooksRun.com'] = json_booksrun['ebook'][length]['price'], json_booksrun['ebook'][length]['cart_url']
              ebook.append(to_append)

      return ebook
    else:
      return None

# returns rental prices
def get_rentals_prices(json_booksrun):
    rent = None
    if json_booksrun != None:
      if json_booksrun['rent'] != 'none':
          rent = []
          for days, info in json_booksrun['rent'].items():
            to_append = {}
            to_append['BooksRun.com'] = json_booksrun['rent'][days]['price'], json_booksrun['rent'][days]['cart_url']
            rent.append(to_append)
            
      return rent
    else:
      return None


# compares all the prices of used books offered by Booksrun and returns the lowest
def used_lowest_price(bookrun_paper_prices, third_party_prices):
    lowest_price = []
    if bookrun_paper_prices[0] != None and bookrun_paper_prices != 'none':
        lowest_price.append(bookrun_paper_prices[0])
  
    if third_party_prices != None and third_party_prices != 'none':
      if third_party_prices[0] != None and third_party_prices != 'none':
          for pair in third_party_prices[0]:
            lowest_price.append(pair)
    
    if lowest_price != [{}] and lowest_price != []:
        sorted(lowest_price, key = lambda item: item['BooksRun.com'][0])
        return lowest_price[0]
    else:
      return None
    
    
# compares all the prices of new books offered by Booksrun and returns the lowest
def new_lowest_price(bookrun_paper_prices, third_party_prices):
    lowest_price = []
    if bookrun_paper_prices[1] != None and bookrun_paper_prices != 'none':
        lowest_price.append(bookrun_paper_prices[1])
    
    if third_party_prices != None and third_party_prices != 'none':
      if third_party_prices[1] != None:
          for pair in third_party_prices[1]:
            lowest_price.append(pair)
    
    if lowest_price != [{}] and lowest_price != []:
        sorted(lowest_price, key = lambda item: item['BooksRun.com'][0])
        return lowest_price[0]
    else:
        return None


# compares all the prices of rentals or ebooks offered by Booksrun and returns the lowest
def ebook_or_rental_lowest(prices):
  if prices is not None:
    lowest_price = {'BooksRun.com': (100000, "")}
    for value in prices:
      price = value['BooksRun.com'][0]
      if float(price) < float(lowest_price['BooksRun.com'][0]):
          lowest_price = value
  
    if lowest_price['BooksRun.com'][0]!= 100000:
      return lowest_price
    else:
      return None
  else:
    return None


# Driver function
def main():
    api_key = "8mhw4i56nn5p1kasxdyu"
    
    js_mill_isbn = '9780199670802'
    data_structures = '9780132576277'
    aquarium = '9780793820788'
    petit_pays = '9782246857334'
    buildings = '9781564588852'
    cinderella_murder = '9781476763699'
    wrong_isbn = '1892sharabia'
  
    #isbn = input_isbn()
    json = booksrun_api_response(data_structures, api_key)
    if json is not None:
        json_booksrun = from_booksrun(json)
        json_others = from_others(json)

        paperbook_prices1 = get_booksrun_paperbook_prices(json_booksrun)
    #     print(f"\nBooksrun paperbook prices:\n {paperbook_prices1}")
        print("\n")

        ebook_prices = get_ebook_prices(json_booksrun)
        print(f"Booksrun ebook prices:\n {ebook_prices}")
        print("\n")

        lowest_price_ebook = ebook_or_rental_lowest(ebook_prices)
        print(f"Ebook lowest price:\n {lowest_price_ebook}")
        print("\n")


        paperbook_prices2 = get_others_paperbook_prices(json_others)
    #     print(f"Third party sellers:\n {paperbook_prices2}")
    #     print("\n")

        lowest_price_used = used_lowest_price(paperbook_prices1, paperbook_prices2)
        print(f"Used book lowest price:\n {lowest_price_used}")
        print("\n")

        lowest_price_new = new_lowest_price(paperbook_prices1, paperbook_prices2)
        print(f"New book lowest price:\n {lowest_price_new}")
        print("\n")

        rentals_prices = get_rentals_prices(json_booksrun)
        print(f"Price of rentals:\n {rentals_prices}")
        print("\n")

        lowest_price_rental = ebook_or_rental_lowest(rentals_prices)
        print(f"Rental Lowest price:\n {lowest_price_rental}")
        print("\n")
    else:
      print("The API Response was not successful!")


#main()
