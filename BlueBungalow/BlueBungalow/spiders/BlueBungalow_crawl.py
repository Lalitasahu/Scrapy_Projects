import scrapy
import json

class BluebungalowCrawlSpider(scrapy.Spider):
    name = "BlueBungalow_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://BlueBungalow.com/"]

    
    def start_requests(self):
        url = 'https://bluebungalow.com.au/collections/shoes-sandals'
        
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://bluebungalow.com.au',
        'Connection': 'keep-alive',
        'Referer': 'https://bluebungalow.com.au/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        }

        yield scrapy.Request(url,headers=headers, callback=self.apihits,dont_filter=True)
    
    def apihits(self,response):
        page = 0
        for i in range(0,6):
            api = f'https://search.unbxd.io/ac541912a18c803bfeab27f04ccbebf4/prod-bluebungalow-au4941591590495/category?&rows=30&p=categoryPath%3A%22shoes-sandals%22&format=json&view=grid&start={i*30}&stats=price&fields=title,uniqueId,collection_tag,plain_tags,publishedAt,secondaryImageUrl,documentType,imageUrl,price,sellingPrice,priceMax,sku,imageUrl,sizeMap,relevantDocument,productUrl,variantId,brand,availability,altImageUrl,altImageTag,imageList&facet.multiselect=true&pagetype=boolean&version=V2&indent=off&filter=documentType:product&filter=publishedAt:*&device-type=Desktop&unbxd-url=https%3A%2F%2Fbluebungalow.com.au%2Fcollections%2Fshoes-sandals&unbxd-referrer=https%3A%2F%2Fbluebungalow.com.au%2F&user-type=new&api-key=ac541912a18c803bfeab27f04ccbebf4'
            yield scrapy.Request(api,callback=self.listpage,dont_filter=True)#,meta={'page':0})

    def listpage(self,response):
        # page = response.meta['page'] + 30
        data = json.loads(response.text)
        products = data['response']['products']
        for product in products:
            name = product['title']
            Id = product['uniqueId']
            productUrl = 'https://bluebungalow.com.au'+product['productUrl']
            price = product['price']
            images = product['imageList']

            # print(name)
            yield{
                'name':name,
                'Id':Id,
                'productUrl':productUrl,
                'price':price,
                'images':images
            }
        # if data['response']['numberOfProducts'] >= data['response']['start']:
        #     api = f'https://search.unbxd.io/ac541912a18c803bfeab27f04ccbebf4/prod-bluebungalow-au4941591590495/category?&rows=30&p=categoryPath%3A%22shoes-sandals%22&format=json&view=grid&start={response.meta["page"]+30}&stats=price&fields=title,uniqueId,collection_tag,plain_tags,publishedAt,secondaryImageUrl,documentType,imageUrl,price,sellingPrice,priceMax,sku,imageUrl,sizeMap,relevantDocument,productUrl,variantId,brand,availability,altImageUrl,altImageTag,imageList&facet.multiselect=true&pagetype=boolean&version=V2&indent=off&filter=documentType:product&filter=publishedAt:*&device-type=Desktop&unbxd-url=https%3A%2F%2Fbluebungalow.com.au%2Fcollections%2Fshoes-sandals&unbxd-referrer=https%3A%2F%2Fbluebungalow.com.au%2F&user-type=new&api-key=ac541912a18c803bfeab27f04ccbebf4'
        #     yield scrapy.Request(api,callback=self.listpage,dont_filter=True,meta={'page':response.meta['page']+30})
