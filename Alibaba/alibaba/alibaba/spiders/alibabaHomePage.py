import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
import pandas as pd


class AlibabaHomePage(scrapy.Spider):
    name = 'alibabahomepage'

    def start_requests(self):
        
        product_list = list(pd.read_csv('C:\\Users\\sudil\\Desktop\\ML_Projects\\Web_scraping\\Alibaba\\alibaba\\alibaba\\spiders\\products.csv')['Product_name'])
        product_names = list(map(lambda x: x.replace(" ","_"),product_list))
        for product_name in product_names:
            search_query = f"https://www.alibaba.com/trade/search?IndexArea=product_en&SearchText={product_name}"
            yield SeleniumRequest(
                url = search_query,
                script = 'window.scrollTo(0,document.body.scrollHeight);',
                wait_time = 3,
                callback = self.parse
            )

    def parse(self, response):
     
        driver = response.meta['driver']
        
        
        product = driver.find_elements(By.CLASS_NAME, "traffic-product-card")

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
            try:
                cover_img_url = i.find_element(By.CLASS_NAME,'J-img-switcher-item').get_attribute('src')
            except:
                cover_img_url = None
            
            yield{
                    "product_name": product_name,
                    "price": price,
                    "product_link": product_link,
                    "rating_score":rating_score,
                    "no_reviews": no_reviews,
                    "tags": tags,
                    "country": country,
                    "cover_img":cover_img_url
                  }
        try:
            next_page_element = driver.find_element(By.XPATH,'//span[@class="seb-pagination__pages-link active"]/following::a')
            next_page = next_page_element.get_attribute("href")
        except:
            next_page = None

        if next_page is not None:
            yield SeleniumRequest(
                    url = next_page,
                    script = 'window.scrollTo(0,document.body.scrollHeight);',
                    wait_time = 3,
                    callback = self.parse
                )
       
    







        