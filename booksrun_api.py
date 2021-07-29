import requests

def input_isbn():
  return input("Enter book ISBN: ")
  
def booksrun_api_response(isbn, api_key):
  url = "https://booksrun.com/api/v3/price/buy/" + isbn + "?key=" + api_key
  resp = requests.get(url)
  json = resp.json()
  return json['result']['offers']

def from_booksrun(json):
   return json['booksrun']

def from_others(json):
  return json['marketplace']
  
def get_booksrun_paperbook_prices(json_booksrun):
  buy_used = None
  if json_booksrun['used'] != 'none':
    buy_used = json_booksrun['used']
    
  buy_new = None
  if json_booksrun['new'] != 'none':
    buy_new = json_booksrun['new']
    
  rent = None
  if json_booksrun['rent'] != 'none':
    rent = {}
    for days, info in json_booksrun['rent'].items():
      rent[days] = json_booksrun['rent'][days]
  
  return buy_used, buy_new, rent

def get_others_paperbook_prices(json_marketplace):
  buy_used = []
  for element in json_marketplace:
      item = {}
      item[element['seller']] = element['used']
      buy_used.append(item)
  
  buy_new = []
  for element in json_marketplace:
      item = {}
      item[element['seller']] = element['used']
      buy_used.append(item)
      
  return buy_used, buy_new  

def get_ebook_prices(json):
  ebook = None
  if json['ebook']!= 'none':
    ebook = {}
    for length, info in json['ebook'].items():
      ebook[length] = json['ebook'][length]
    
  return ebook
  
def main():
  api_key = "8mhw4i56nn5p1kasxdyu"
  isbn = input_isbn()
  json = booksrun_api_response(isbn, api_key)
  json_booksrun = from_booksrun(json)
  json_others = from_others(json)
  
  paperbook_prices1 = get_booksrun_paperbook_prices(json_booksrun)
  print(f"Booksrun paperbook prices:\n {paperbook_prices1}")
  print("\n")
  
  ebook_prices = get_ebook_prices(json_booksrun)
  print(f"Booksrun ebook prices:\n {ebook_prices}")
  print("\n")
  
  paperbook_prices2 = get_others_paperbook_prices(json_others)
  print(f"Third party sellers:\n {paperbook_prices2}")
  print("\n")
  
  
  
main()