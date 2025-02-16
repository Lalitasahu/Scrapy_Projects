import json
import scrapy
from urllib.parse import urljoin
import re

class AmazonSearchProductSpider(scrapy.Spider):
    name = "amazon_search_product"
    def start_requests(self):
        keyword_list = ['ipad']
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': 1})

    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 
            
        ## Get All Pages
        if page == 1:
            available_pages = response.xpath(
                '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            ).getall()

            last_page = available_pages[-1]
            for page_num in range(2, int(last_page)):
                amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': page_num})


# import scrapy
# import os
# from scrapy.crawler import CrawlerProcess

# class AmazonSpiderSpider(scrapy.Spider):
#     name = "amazon_spider"
#     # allowed_domains = ["*"]
#     custom_settings = { "FEEDS" : {'results.csc': {'format':'csv'}}}
#     start_urls = ["https://www.amazon.in/s?k=webscraping+book"]
#     # headers = {
#     #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0'
#     #     }
#     # try:
#     #     os.remove['results.csv']
#     #     # os.['results.csv']
#     # except OSError:
#     #     pass
     
#     def parse(self,response):
#         pass



# if __name__ == "__main__" :
#     process = CrawlerProcess()
#     process.crawl(AmazonSpiderSpider)
#     process.start()
    


