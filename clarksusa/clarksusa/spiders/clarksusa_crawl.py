import scrapy
import json

class ClarksusaCrawlSpider(scrapy.Spider):
    name = "clarksusa_crawl"
    allowed_domains = ["clarksusa.com"]
    # start_urls = ["http://clarksusa.com/"]
    
    def start_requests(self): 
        url = 'https://www.clarksusa.com/womens/all-styles/c/w2'
        headers ={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
        }

        yield scrapy.Request(url, callback=self.Url_api, headers=headers)
    
    def Url_api(self, response):
        api = 'https://www.clarksusa.com/category-search-ajax?categoryCode=w2'
        yield scrapy.Request(api, callback=self.listpage )

    def listpage(self, response):
        js = json.loads(response.text)
        products = js['products']
        for product in products:
            Title = product['name']
            ID = product['code']
            pro_url = 'https://www.clarksusa.com'+product['url']
            try:
                price = product['wasPrice']['formattedValue']
            except:
                
                try:
                    price = product['price']['formattedValue']
                except:
                    price = ''
            imageUrl = product['imageUrl']
            
            yield {
                'Title':Title,
                'ID':ID,
                'pro_url':pro_url,
                'price':price,
                'imageUrl':imageUrl
            }
            print(Title)
