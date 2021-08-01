import requests as req

# ISBNdb api response
def i_api_response(api_key, isbn):
  h = {'Authorization': api_key}
  resp = req.get("https://api2.isbndb.com/book/" + isbn + "?with_prices=1", headers=h)
  return resp.json()['book']


# returns listed price of the book
def i_listed_price(json):
  return json['msrp']


# returns prices from different merchants
# @param condition: can be "Rental", "eBook", "Used", "New"
def i_merchant_prices(json, condition):
  price_info_list = json['prices']
  merchant_prices = []
  for i in range(len(price_info_list)):
    merchant = price_info_list[i]['merchant']
    to_append = {}
    if price_info_list[i]['condition'] == condition:
      to_append[merchant] = price_info_list[i]['total'], price_info_list[i]['link']
      merchant_prices.append(to_append)
  
  return merchant_prices

def i_lowest_used_price(json):
  used_prices = i_merchant_prices(json, 'Used')
  return used_prices[0]

def i_lowest_new_price(json):
  new_prices = i_merchant_prices(json, 'New')
  return new_prices[0]

def i_lowest_rental_price(json):
  rental_prices = i_merchant_prices(json, 'Rental')
  return rental_prices[0]

def i_lowest_ebook_price(json):
  ebook_prices = i_merchant_prices(json, 'eBook')
  return ebook_prices[0]

def main():
  api_key = "46445_4b9207100f7b3236200445a31f95a377"
  js_mill_isbn = '9780199670802'
  data_structures = '9780132576277'
  aquarium = '9780793820788'
  petit_pays = '9782246857334'
  buildings = '9781564588852'
  cinderella_murder = '9781476763699'
  json = i_api_response(api_key, data_structures)
  listed_price = i_listed_price(json)
  condition = "New"
  merchant_prices = i_merchant_prices(json, condition)
  print(merchant_prices)
  lowest_ebook = i_lowest_ebook_price(json)
  # print(lowest_ebook)
  lowest_used = i_lowest_used_price(json)
  # print(lowest_used)
  lowest_new = i_lowest_new_price(json)
  print(lowest_new)
  lowest_rental = i_lowest_rental_price(json)
  # print(lowest_rental)

main()
  