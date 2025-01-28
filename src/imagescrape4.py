from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
import io
from PIL import Image
import os
import time
import json

# Path to chromedriver
PATH = "/Users/nkhumalo/VSCode/webscrape/chromedriver"
cService = ChromeService(executable_path=PATH)
wd = webdriver.Chrome(service=cService)

# Function to download image
def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = os.path.join(download_path, file_name)

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print(f"Success: Photo downloaded - {file_path}")
    except Exception as e:
        print(f"FAILED - {e}")

# Function to download PDF
def download_pdf(download_path, url, file_name):
    try:
        response = requests.get(url)
        if response.headers['Content-Type'] == 'application/pdf':
            file_path = os.path.join(download_path, file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Success: PDF downloaded - {file_path}")
        else:
            print(f"Failed: URL does not point to a PDF - {url}")
    except Exception as e:
        print(f"FAILED - {e}")

# Function to get images and corresponding PDFs
def get_images_and_pdfs(wd, delay, max_items, download_dir):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    base_url = "https://www.yarnspirations.com/en-row/collections/patterns?filter.p.m.global.skill_type=Crochet&page="
    page_number = 1
    items_collected = 0
    unique_items = set()

    while items_collected < max_items:
        url = f"{base_url}{page_number}"
        wd.get(url)
        print(f"Processing page: {page_number}")

        scroll_down(wd)

        # Locate images
        images = wd.find_elements(By.CSS_SELECTOR, ".boost-pfs-filter-product-item-main-image.Image--lazyLoad.lazyautosizes.lazyloaded")

        # Locate corresponding PDF links
        pdf_links = wd.find_elements(By.CSS_SELECTOR, "a.download-pattern-btn")

        if not images and not pdf_links:
            print("No more content found. Ending.")
            break

        for i in range(len(images)):
            if i >= len(pdf_links):
                break

            image = images[i]
            pdf_link = pdf_links[i]

            image_src = image.get_attribute('src')
            pdf_href = pdf_link.get_attribute('href')
            product_data = pdf_link.get_attribute('data-product')

            try:
                product_json = json.loads(product_data.replace('&quot;', '"'))
                pattern_name = product_json.get('name', 'Unknown_Pattern').replace(' ', '_')
            except json.JSONDecodeError:
                pattern_name = "Unknown_Pattern"

            if image_src and 'http' in image_src and pdf_href not in unique_items:
                unique_items.add(pdf_href)

                # Create a directory for each pattern
                pattern_dir = os.path.join(download_dir, pattern_name)
                os.makedirs(pattern_dir, exist_ok=True)

                # Download the image
                image_file_name = f"{pattern_name}.jpg"
                download_image(pattern_dir, image_src, image_file_name)

                # Download the PDF
                pdf_file_name = f"{pattern_name}.pdf"
                download_pdf(pattern_dir, pdf_href, pdf_file_name)

                items_collected += 1

            if items_collected >= max_items:
                break

        page_number += 1

# Example usage
download_dir = "downloaded_patterns"
os.makedirs(download_dir, exist_ok=True)

get_images_and_pdfs(wd, 3, 100, download_dir)  # Example to get 10 items

# Quit the WebDriver
wd.quit()
