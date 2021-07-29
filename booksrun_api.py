import requests

def input_isbn():
  return input("Enter book ISBN: ")
  
def booksrun_api_response(isbn, api_key):
  url = "https://booksrun.com/api/v3/price/buy/" + isbn + "?key=" + api_key
  resp = requests.get(url)
  json = resp.json()
  return json['result']['offers']['booksrun']

def get_paperbook_prices(json):
  buy_used = None
  if json['used'] != 'none':
    buy_used = json['used']['price']
    
  buy_new = None
  if json['new'] != 'none':
    buy_new = json['new']['price']
    
  rent = None
  if json['rent'] != 'none':
    rent = {}
    for days, info in json['rent'].items():
      rent[days] = json['rent'][days]['price']
  
  return buy_used, buy_new, rent
    
  
def main():
  api_key = "8mhw4i56nn5p1kasxdyu"
  isbn = input_isbn()
  json = booksrun_api_response(isbn, api_key)
  paperbook_prices = get_paperbook_prices(json)
  print(paperbook_prices)
  
  
main()