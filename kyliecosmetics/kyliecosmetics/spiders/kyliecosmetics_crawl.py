from scrapy.http import JsonRequest
import scrapy
import json
import math

class KyliecosmeticsCrawlSpider(scrapy.Spider):
    name = "kyliecosmetics_crawl"
    # allowed_domains = ["*"]
    allowed_domains = ["https://kyliecosmetics.com","https://frj8qduii9-dsn.algolia.net"]
    # start_urls = ["http://kyliecosmetics.com/"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'content-type': 'application/x-www-form-urlencoded',
        'Origin': 'https://kyliecosmetics.com',
        'Connection': 'keep-alive',
        'Referer': 'https://kyliecosmetics.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }

    data = '{"requests":[{"facets":["product_type","options.shade","meta.variant.shade_grouping","named_tags.skin_type","named_tags.key_ingredient","named_tags.benefit","named_tags.price_range"],"facetFilters":[["collections:__COLLECTION__"]],"indexName":"shopify_us_products","numericFilters":[],"hitsPerPage":20,"page":__PAGE__,"query":"","distinct":1,"ruleContexts":["__COLLECTION__"],"analytics":false,"params":""}]}'



    def start_requests(self):
        url = 'https://kyliecosmetics.com/en-in/collections/kylie-skin'
        yield scrapy.Request(url, callback=self.api, headers=self.headers, dont_filter=True)

    def api(self, response):
        page = 0
        collection = response.url.split('?')[0].split('/')[-1]
        apis = 'https://frj8qduii9-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.15.0)%3B%20Browser%20(lite)&x-algolia-api-key=c8928918302a13ebd41e4887784cec9c&x-algolia-application-id=FRJ8QDUII9'
        yield scrapy.Request(apis,callback=self.listpage,headers=self.headers,body=self.data.replace('__PAGE__',str(page)).replace('__COLLECTION__',str(collection)),dont_filter=True,method='POST', meta={'page': page,'collection':collection})

    def listpage(self, response):
        collection = response.meta.get('collection')
        page = response.meta['page']+1
        js = response.json()
        products = js['results'][0]['hits']
        for prodcut in products:
            title = prodcut['title']
            pro_url = 'https://kyliecosmetics.com/en-in/collections/kylie-skin/products/'+prodcut['handle']
            sku_id = prodcut['sku']
            pro_id = prodcut['id']
            product_image = prodcut['product_image']
            
            yield {
                'title':title,
                'pro_url':pro_url,
                'pro_id':pro_id,
                'sku_id':sku_id,
                'product_image':product_image,
            
            }
        total = math.ceil(js['results'][0]['nbHits'])/20
        if int(total) > js['results'][0]['page']:            
            apis = 'https://frj8qduii9-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.15.0)%3B%20Browser%20(lite)&x-algolia-api-key=c8928918302a13ebd41e4887784cec9c&x-algolia-application-id=FRJ8QDUII9'
            # data = f'{"requests":[{"facets":["product_type","options.shade","meta.variant.shade_grouping","named_tags.skin_type","named_tags.key_ingredient","named_tags.benefit","named_tags.price_range"],"facetFilters":[["collections:kylie-cosmetics-lips-lip-kits"]],"indexName":"shopify_us_products","numericFilters":[],"hitsPerPage":20,"page":str(page),"query":"","distinct":1,"ruleContexts":["kylie-cosmetics-lips-lip-kits"],"analytics":false,"params":""}]}'
            yield scrapy.Request(apis,callback=self.listpage,headers=self.headers,body=self.data.replace('__PAGE__',str(page)).replace('__COLLECTION__',str(collection)),dont_filter=True,method='POST', meta={'page':page})

