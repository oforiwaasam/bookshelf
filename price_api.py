import requests
from requests.structures import CaseInsensitiveDict

url = "https://api.priceapi.com/v2/jobs"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"

data = "token=HYYWTNBFPRRTROCWSIRSIUKUJFOGJGGBZISUQRUHCDNYAGOCTYYUABBXHMJCNGSO&country=us&source=google_shopping&topic=search_results&key=term&max_age=43200&max_pages=1&sort_by=ranking_descending&condition=any&values=the art of problem solving"

resp = requests.post(url, headers=headers, data=data)
resp_json = resp.content

print(resp.status_code)
print(resp_json)

