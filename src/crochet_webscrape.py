import requests
from bs4 import BeautifulSoup
import statistics

"""Define desired website url"""
BASE_URL = "https://www.yarnspirations.com/" # desired website

url = BASE_URL + "en-row/collections/patterns?filter.p.m.global.skill_type=Crochet" # free crochet pattern

""" Send request to website server and send response/website content """
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

# explore some divs
divs = soup.find_all("div")
#print(divs)

# grab desired images
#product_images = soup.find_all("img", {"boost-pfs-filter-product-item-main-image Image--lazyLoad lazyautosizes lazyloaded"})
product_images = soup.find_all("img")

print(product_images)
for img in product_images:
    image_url = img.get("src")
    if image_url != "None":
        print(image_url)
        name = image_url.split('/')[-1] # get image name
        img_response = requests.get(image_url) # request image from site
        file = open(name, "wb") # create file
        file.write(img_response.content) # write image to file
        file.close() # close file 


# grab skill level 
skill = soup.find_all("div", {"class": "pattern-card__skill-container xsmall-heading"})