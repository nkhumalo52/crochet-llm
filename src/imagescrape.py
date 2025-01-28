from selenium import webdriver 
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "/Users/nkhumalo/VSCode/webscrape/chromedriver" #path of chromedriver.exe
cService = webdriver.ChromeService(executable_path=PATH) #setting PATH to chromedriver
wd = webdriver.Chrome(service = cService) #opening new google chrome tab

image_url = "https://cdn.shopify.com/s/files/1/0711/5132/1403/files/RHC0803-036731M_540x.jpg?v=1717168772"


def get_images(wd, delay, max_images ):

    # Find the element with aria-label='Close dialog' and click it
    #email_button = wd.find_element(By.CSS_SELECTOR, "[aria-label='Close dialog']")
    #email_button.click()

    # Find the element with aria-label='Close' and click it
    #cookie_button = wd.find_element(By.CSS_SELECTOR, "[aria-label='Close']")
    #cookie_button.click()


    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        #while(True):
            #pass
    
    url = "https://www.yarnspirations.com/en-row/collections/patterns?filter.p.m.global.skill_type=Crochet"
    wd.get(url)

    image_urls = set()
    while len(image_urls) < max_images:
         #scroll_down(wd)

         images = wd.find_elements(By.CLASS_NAME, "boost-pfs-filter-product-item-main-image Image--lazyLoad lazyautosizes lazyloaded")
         print(images)
         for image in images:
              print(image, " This is the image we're looking at!")
              if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                 print("Source found")
                 image_urls.add(image.get_attribute('src'))
                 print("Found image!")  
    while(True):
            pass
    return image_urls


def download_image(download_path, url, file_name):
    """This function makes a request to get photo content
    from url and saves it as bytes to memory. Then uses Pillow 
    to turn it into a jpeg """

    try:
        image_content = requests.get(url).content # src of desired photo 
        image_file = io.BytesIO(image_content) # saves image as binary to memory 
        image = Image.open(image_file) # saves binary as PIL image
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success: Photo downloaded!!!")
    except Exception as e:
        print("FAILED - ", e)


#download_image("", image_url, "test.jpg")
url = get_images(wd, 2, 1)
print(url)
wd.quit