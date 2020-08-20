import requests

url = "https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/"

querystring = {"ip":"67.225.162.5"}

headers = {
    'x-rapidapi-host': "ip-geolocation-ipwhois-io.p.rapidapi.com",
    'x-rapidapi-key': "789d22491amsh9cf6fe5ac3b3cf8p195e80jsn0b807e6d418c"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)