# Do not use this code.
from itertools import product
from selenium import webdriver
from lxml import html
from time import sleep
from selenium.webdriver.common.by import By
import re
from shutil import which
from selenium.webdriver.chrome.options import Options



chrome_driver = which('chromedriver')
chrome_options = Options()
chrome_options.add_argument("--headless")

product_name = input("Name of the product: ")
page_range = int(input("Number of pages required: "))
driver = webdriver.Chrome(executable_path=chrome_driver)
# driver = webdriver.Chrome(executable_path=chrome_driver,options=chrome_options)


links = []
for page_no in range(1,page_range+1):
    search_query = f"https://www.alibaba.com/trade/search?IndexArea=product_en&SearchText={product_name}&page={page_no}"
    
    # product detail extractor
    driver.get(search_query)
    sleep(5)

    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    sleep(3)

    product = driver.find_elements(By.CLASS_NAME, "traffic-product-card")
    # product = driver.find_elements(By.CLASS_NAME, "app-organic-search__list")

    for i in product:
        try:
            product_name = i.find_element(By.CLASS_NAME,"elements-title-normal__content").text
        except:
            product_name = None
        try:
            price = i.find_element(By.CLASS_NAME,"elements-offer-price-normal").text
        except:
            price = None 
        try:
            product_link = i.find_element(By.CLASS_NAME,"elements-title-normal").get_attribute('href')
            links.append(product_link)
        except:
            product_link = None
        try:
            rating_score= i.find_element(By.CLASS_NAME,"seb-supplier-review-gallery-test__score").text
        except:
            rating_score = None
        try:
            no_reviews = i.find_element(By.CLASS_NAME,"seb-supplier-review__review-count").text
        except:
            no_reviews = None
        try:
            tags = i.find_element(By.CLASS_NAME,"tags-below-title__chuc-container").text
        except:
            tags = None
        try:
            country = i.find_element(By.CLASS_NAME,"seller-tag__country").get_attribute('title')
        except:
            country = None

        print(product_name,price,product_link,rating_score,no_reviews,tags,country)

# link collector
def get_image():
    product_image_dict = {}
    for link in links:
        driver.get(link)
        sleep(5)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        sleep(3)
        product_media = driver.find_elements(By.CLASS_NAME,'main-item')

        product_image_dict[link] = []
        for media in product_media:
            # get the images
            try:
                image_link = media.find_element(By.TAG_NAME,'img').get_attribute('src')
                product_image_dict[link].append(image_link)
            except:
                image_link=None
            # print(product_image_dict)

           
    print(product_image_dict)

def get_video():
    product_video_dict = {}
    for link in links:
        driver.get(link)
        sleep(5)
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        sleep(3)
        try:
            # get the video
            video_link = driver.find_element(By.CLASS_NAME,"bc-video-player").get_attribute('src') 
            product_video_dict[link].append(video_link)
        except:
            video_link = None
    print(product_video_dict)

# get_image()
# get_video()

# review extractor
def review_extractor():
    pass

