import requests as req
from book_apis import *
# ISBNdb api response
def i_api_response(api_key, isbn):
    h = {'Authorization': api_key}
    resp = req.get("https://api2.isbndb.com/book/" + isbn + "?with_prices=1", headers=h)

    if resp.status_code == 200:
        return resp.json()['book']
    else: 
        return None



# returns listed price of the book
def i_listed_price(json):

    if json is not None:
        return json['msrp']
    else:
        return None



# returns prices from different merchants
# @param condition: can be "Rental", "eBook", "Used", "New"
def i_merchant_prices(json, condition):
    if json is not None:
        price_info_list = json['prices']
        merchant_prices = []
        for i in range(len(price_info_list)):
            merchant = price_info_list[i]['merchant']
            to_append = {}
            if condition in price_info_list[i].values():
                to_append[merchant] = price_info_list[i]['total'], price_info_list[i]['link']
                merchant_prices.append(to_append)

        return merchant_prices
    else:
        return None

def i_lowest_used_price(json):
    if json is not None:
        used_prices = i_merchant_prices(json, 'Used')
        if used_prices is not None and used_prices != []:
            return used_prices[0]
        else:
            return None
    else:
        return None
    
 # 
def i_lowest_new_price(json):
    if json is not None:
        new_prices = i_merchant_prices(json, 'New')
        if new_prices is not None and new_prices != []:
            return new_prices[0]
        else:
            return None
    else:
        return None

 # 
def i_lowest_rental_price(json):
    if json is not None:
        rental_prices = i_merchant_prices(json, 'Rental')
        if rental_prices is not None and rental_prices != []:
            return rental_prices[0]
        else:
            return None
    else:
        return None

def i_lowest_ebook_price(json):
    if json is not None:
        ebook_prices = i_merchant_prices(json, 'eBook')
        if ebook_prices is not None and ebook_prices != []:
            return ebook_prices[0]
        else:
            return None
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
        api_key = "46445_4b9207100f7b3236200445a31f95a377"
        json = i_api_response(api_key, ISBN)
        data = []
        if json is not None:
    #         print(f"Prices from different merchants: {json['prices']}")
    #         print("\n")
            listed_price = i_listed_price(json)
            lowest_ebook = i_lowest_ebook_price(json)
    #         print(f"Lowest price for ebook: {lowest_ebook}")
    #         print("\n")
            lowest_used = i_lowest_used_price(json)
    #         print(f"lowest price for used books: {lowest_used}")
    #         print("\n")
            lowest_new = i_lowest_new_price(json)
    #         print(f"Lowest price for new books: {lowest_new}")
    #         print("\n")
            lowest_rental = i_lowest_rental_price(json)
    #         print(f"Lowest price for rented books: {lowest_rental}")
            # [listed_price,lowest_ebook,lowest_used,lowest_new,lowest_rental]  
            temp = [lowest_ebook,lowest_used,lowest_new,lowest_rental]
            count = 0
            for elem in temp:
                if elem != None:
                    data.append((count,elem))
                count+=1

            return setprices(data)
        else:
            print("No Results: You've probably entered a wrong ISBN")  

    
def main():
    data_lst=get_data('9780199670802')
#     print(data_lst)
    for data in data_lst:
        print("source", data[0])
        print("prices",data[1])
        print("link",data[2])
        print("name",data[3])

#   api_key = "46445_4b9207100f7b3236200445a31f95a377"
#   js_mill_isbn = '9780199670802'
#   data_structures = '9780132576277'
#   aquarium = '9780793820788'
#   petit_pays = '9782246857334'
#   buildings = '9781564588852'
#   cinderella_murder = '9781476763699'
#   wrong_isbn = '1829kdlsk'
#   json = i_api_response(api_key, data_structures)
#   if json is not None:
#     listed_price = i_listed_price(json)
#     lowest_ebook = i_lowest_ebook_price(json)
#     print(f"Lowest price for ebook: {lowest_ebook}")
#     print("\n")
#     lowest_used = i_lowest_used_price(json)
#     print(f"lowest price for used books: {lowest_used}")
#     print("\n")
#     lowest_new = i_lowest_new_price(json)
#     print(f"Lowest price for new books: {lowest_new}")
#     print("\n")
#     lowest_rental = i_lowest_rental_price(json)
#     print(f"Lowest price for rented books: {lowest_rental}")
#   else:
#     print("No Results: You've probably entered a wrong ISBN")



#main()
  