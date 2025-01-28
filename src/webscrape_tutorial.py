import requests
from bs4 import BeautifulSoup
import statistics

"""" response = requests.get("books") # send request and save response

soup = BeautifulSoup(response.text) # save response as soup object

# use soup object to get certain elements """


BASE_URL = "https://books.toscrape.com/"

url = BASE_URL + "catalogue/category/books/philosophy_7/index.html" # desired page

""" def proxy_requests(url):
    payload = { # what we are sending to the proxy server so it knows where it should go
        "source": "universal",
        "url": url,
        "geo_location": "Germany"
    }

    response = requests.request(
        "POST", "https://realtime.oxylabs.io/v1/queries",
        auth = 
    )
    return """
    
response = requests.get(url) # send request to website server
soup = BeautifulSoup(response.text, "lxml") # save response/website content
price_tags = soup.find_all("p", {"class": "price_color"}) # p with class price_color

prices = [float(price.text[2:]) for price in price_tags] # list with only prices
print(prices)

""" This is the version of the program without proxys!

response = requests.get(url) # send request to website server
soup = BeautifulSoup(response.text, "lxml") # save response/website content

#print(soup.find_all("p")) # this will find all paragraphs

#print(soup.find_all("a")) # this will find all anchors

price_tags = soup.find_all("p", {"class": "price_color"}) # p with class price_color
#print(price_tags)

prices = [float(price.text[2:]) for price in price_tags] # list with only prices
print(prices)
print(statistics.mean(prices))"""