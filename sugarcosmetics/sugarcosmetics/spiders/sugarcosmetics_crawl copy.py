import scrapy
import json
import math

class SugarcosmeticsCrawlSpider(scrapy.Spider):
    name = "sugarcosmetics_crawl"
    allowed_domains = ["sugarcosmetics.com"]
    # start_urls = ["http://sugarcosmetics.com/"]
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Origin': 'https://in.sugarcosmetics.com',
    'Connection': 'keep-alive',
    'Referer': 'https://in.sugarcosmetics.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }



    json_data = {
    'collection_handle': 'matte-lipsticks',
    'sort': 'relevance',
    'filter': {},
    'skip': 0,
    'count': 20,
    'device_id': '7c16-925c-4d4f-8042-21edcaca7191',
    }
    
    def start_requests(self):
        url = 'https://in.sugarcosmetics.com/collections/merch-station'
        # url = 'https://in.sugarcosmetics.com/collections/matte-lipsticks'
        yield scrapy.Request(url, headers=self.headers, dont_filter=True, callback=self.api)
    
    def api(self, response):
        collection = response.url.split('/')[-1]
        page = 0
        skip = 0
        apiurl = 'https://prod.api.sugarcosmetics.com/collections/prod/getCollectionv2'
        yield scrapy.Request(apiurl, headers=self.headers, method='POST', body=json.dumps(self.json_data), dont_filter=True, callback=self.listpage, meta={'page':page, 'skip':skip, 'collection':collection})
    
    def listpage(self, response):
        js = response.json()
        # page = 1
        # skip = 20
        collection = response.meta.get('collection')
        page = response.meta['page']+1
        skip = response.meta['skip']+20
        # while True:
        # print(js)
        products = js['resbody']['result']
        for product in products:
            pro_url = 'https://in.sugarcosmetics.com/products/'+product['handle']
            Title = product['product_json']['title']
            created_at = product['product_json']['created_at']
            pro_id = product['id']
            vendor = product['product_json']['vendor']
            image = product['product_json']['image']['src']
            collection_handle = product['collection_handle']
            Price = product['product_price']
            
            yield {
                'pro_url':pro_url,
                'Title':Title,
                'created_at':created_at,
                'pro_id':pro_id,
                'vendor':vendor,
                'image':image,
                'collection_handle':collection_handle,
                'Price':Price
            }
        
        # par_page = 31
        total_no = math.ceil(js['resbody']['total_count'][0])/21
        if total_no > page:
            apiurl = 'https://prod.api.sugarcosmetics.com/collections/prod/getCollectionv2'
            # json_data['skip']: skip
            json_data = {
                'collection_handle': collection,
                'sort': 'relevance',
                'filter': {},
                'skip': skip,
                'count': 20,
                'device_id': '7c16-925c-4d4f-8042-21edcaca7191',
                }
            yield scrapy.Request(apiurl, headers=self.headers, method='POST', body=json.dumps(json_data), dont_filter=True, callback=self.listpage, meta={'page':page, 'skip':skip,'collection':response.meta.get('collection')})