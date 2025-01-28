from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
import io
from PIL import Image
import time

# Path to chromedriver
PATH = "/Users/nkhumalo/VSCode/webscrape/chromedriver"
cService = ChromeService(executable_path=PATH)
wd = webdriver.Chrome(service=cService)

def get_images(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.yarnspirations.com/en-row/collections/patterns?filter.p.m.global.skill_type=Crochet"
    wd.get(url)

    image_urls = set()
    while len(image_urls) < max_images:
        scroll_down(wd)

        # Use CSS_SELECTOR to locate elements by multiple classes
        images = wd.find_elements(By.CSS_SELECTOR, ".boost-pfs-filter-product-item-main-image.Image--lazyLoad.lazyautosizes.lazyloaded")

        for image in images:
            src = image.get_attribute('src')
            if src and 'http' in src:
                image_urls.add(src)
                print(f"Found image: {src}")

        if len(image_urls) >= max_images:
            break

    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print(f"Success: Photo downloaded - {file_path}")
    except Exception as e:
        print(f"FAILED - {e}")

# Get the image URLs
image_urls = get_images(wd, 2, 2)  # Example to get 5 images
print(image_urls)

# Download the images
for i, url in enumerate(image_urls):
    download_image("", url, f"test_{i}.jpg")

# Quit the WebDriver
wd.quit()
