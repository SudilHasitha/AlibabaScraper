import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from alibaba.spiders.alibabaHomePage import AlibabaHomePage

process = CrawlerProcess(settings=get_project_settings())
process.crawl(AlibabaHomePage)
process.start()