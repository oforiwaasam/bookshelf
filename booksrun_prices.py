import requests


# The user inputs the ISBN of the book
def input_isbn():
    return input("Enter book ISBN: ")


# Getting the response from the API of Booksrun.com
def booksrun_api_response(isbn, api_key):
    url = "https://booksrun.com/api/v3/price/buy/" + isbn + "?key=" + api_key
    resp = requests.get(url)
    json = resp.json()
    return json['result']['offers']


# prices given by Booksrun (usually no shipping fee)
def from_booksrun(json):
    return json['booksrun']


# prices from third party sellers selling on Booksrun (there is usually a
# shipping fee)
def from_others(json):
    return json['marketplace']


# prices of hard copy books sold by Booksrun
# return: prices and cart urls of used, new, and rented books
def get_booksrun_paperbook_prices(json_booksrun):
    buy_used = None
    if json_booksrun['used'] != 'none':
        buy_used = json_booksrun['used']['price'], json_booksrun['used']['cart_url']

    buy_new = None
    if json_booksrun['new'] != 'none':
        buy_new = json_booksrun['new']['price'], json_booksrun['new']['cart_url']

    rent = None
    if json_booksrun['rent'] != 'none':
        rent = {}
        for days, info in json_booksrun['rent'].items():
            rent[days] = json_booksrun['rent'][days]['price'], json_booksrun['rent'][days]['cart_url']

    return buy_used, buy_new, rent


# prices of hard copy books sold by third party sellers on Booksrun
# return: prices and cart urls of used, new, and rented books
def get_others_paperbook_prices(json_marketplace):

    if json_marketplace != 'none':
        buy_used = []
        for element in json_marketplace:
            item = {}
            if element['used'] != 'none':
                element['used']['price'] += element['shipping']
                del element['used']['condition']
                price_and_url = element['used']['price'], element['used']['cart_url']
                buy_used.append(price_and_url)

        buy_new = []
        for element in json_marketplace:
            item = {}
            if element['new'] != 'none':
                element['new']['price'] += element['shipping']
                del element['new']['condition']
                price_and_url = element['new']['price'], element['new']['cart_url']
                buy_used.append(price_and_url)

        return buy_used, buy_new
    else:
        return None


# prices of ebooks sold by Booksrun
# return: prices, length of rent and cart urls of the ebooks
def get_ebook_prices(json):
    ebook = None
    if json['ebook'] != 'none':
        ebook = {}
        for length, info in json['ebook'].items():
            ebook[length] = json['ebook'][length]['price'], json['ebook'][length]['cart_url']

    return ebook


# compares all the prices offered by Booksrun and returns the lowest
# def used_lowest_price(bookrun_paper_prices, third_party_prices):
#      lowest_price = []
#      if bookrun_paper_prices != None:
#         for i in range(2):
#           if bookrun_paper_prices[i]  != None
#               lowest_price.append[bookrun_paper_prices[i]['']]
  

# Driver function
def main():
    api_key = "8mhw4i56nn5p1kasxdyu"
    isbn = input_isbn()
    json = booksrun_api_response(isbn, api_key)
    json_booksrun = from_booksrun(json)
    json_others = from_others(json)

    paperbook_prices1 = get_booksrun_paperbook_prices(json_booksrun)
    print(f"\nBooksrun paperbook prices:\n {paperbook_prices1}")
    print("\n")

    ebook_prices = get_ebook_prices(json_booksrun)
    print(f"Booksrun ebook prices:\n {ebook_prices}")
    print("\n")

    paperbook_prices2 = get_others_paperbook_prices(json_others)
    print(f"Third party sellers:\n {paperbook_prices2}")
    print("\n")


main()
