import requests

# Makes a call to the google api and returns a json response format
def g_search(api_key, isbn):
  url = "https://www.googleapis.com/books/v1/volumes?q=+isbn:" + isbn + "&key=" + api_key
  resp = requests.get(url)
  json = resp.json()
  return json


def main():
  api_key = "I have it in my local repo"
  js_mill_isbn = '9780199670802'
  data_structures = '9780132576277'
  aquarium = '9780793820788'
  petit_pays = '9782246857334'
  buildings = '9781564588852'
  cinderella_murder = '9781476763699'
  print(g_search(api_key, js_mill_isbn))

main()
