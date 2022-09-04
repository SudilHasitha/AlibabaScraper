import scrapy
from scrapy_selenium import SeleniumRequest
import pandas as pd
from selenium.webdriver.common.by import By

class AlibabaitemdetailsSpider(scrapy.Spider):
    name = 'alibabaItemDetails'
    
    def start_requests(self):
        url_list = list(pd.read_csv(r'C:\Users\sudil\Desktop\ML_Projects\Web_scraping\Product_Details_Processed.csv')['product_link'])
        for product_link in url_list:
            if product_link is not None:
                yield SeleniumRequest(
                    url = product_link,
                    script = 'window.scrollTo(0,document.body.scrollHeight);',
                    wait_time = 3,
                    callback = self.parse,
                    meta = {'product_link': product_link}
                )

    def parse(self,response):
      
        driver = response.request.meta['driver']
        product_link = response.request.meta['product_link']
        try:
            company_name = driver.find_element(By.XPATH,'//a[@class="company-name company-name-lite-vb"]').get_attribute('title')
        except:
            company_name = None
        try:
            company_url = driver.find_element(By.XPATH,'//a[@class="company-name company-name-lite-vb"]').get_attribute('href')
        except:
            company_url = None
        if company_name is None:
            try:
                company_name = driver.find_element(By.XPATH,'//div[@class="company-item"]/a/text()').getText()
            except:
                company_name = None
        if company_url is None:
            try:
                company_url = driver.find_element(By.XPATH,'//div[@class="company-item"]/a').get_attribute('href')
            except:
                company_url = None

        # extract images
        product_image_list=[]
        product_media = driver.find_elements(By.CLASS_NAME,'main-item')

        for media in product_media:
            # get the images
            try:
                image_link = media.find_element(By.TAG_NAME,'img').get_attribute('src')
                product_image_list.append(image_link)
            except:
                image_link=None
        # extract video
        try:
            video_link = driver.find_element(By.XPATH,'//div[@class="bc-video-player"]/video').get_attribute('src')
        except:
            video_link = None

        yield {
            "company_name":company_name,
            "company_url": company_url,
            "product_link":product_link,
            "image_links": product_image_list,
            "video_link": video_link
        }
