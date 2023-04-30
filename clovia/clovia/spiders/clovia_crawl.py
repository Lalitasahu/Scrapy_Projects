import scrapy
from scrapy.http import JsonRequest
import math
from bs4 import BeautifulSoup as BS

class CloviaCrawlSpider(scrapy.Spider):
    name = "clovia_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://clovia.com/"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        # 'Accept-Language': 'en-US,en;q=0.5',
        # # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Alt-Used': 'www.clovia.com',
        # 'Connection': 'keep-alive',
        # 'Cookie': 'sessionid=xuc2zldg5x2y4o4ib357ploeq03x8068; http_referer_val="firstclicktime=2023-02-22 23:24:52.521154\\054http_referer=https://www.clovia.com/"; _gcl_au=1.1.1016531704.1677088494; _ga_TC6QEKJ4BS=GS1.1.1677218170.13.1.1677218591.60.0.0; _ga=GA1.2.1332762842.1677088495; _gid=GA1.2.1029297947.1677088495; cto_bundle=ImTAUV9xeXYxUHFWRlclMkI5TTlkaUFNVU9SOUJjMXhUa21lcnc0NjUwRGdKRXhPakJleFFEZnkxalVhdHhWZFM4b1c2QjBtUUJJVEpSNXM5YTBDJTJGdnNDb3NzMVk2cGxOWEdEdnh6YXVFZE0wUG1uVDI2dFpuY09ld00wdkVYSjVubnFzdnNTSDduc1lFbiUyRjBJQWNTZU9vT2dmRjlNVGU4bExrUDIlMkJORWVOVEpMSFRXNkhFZ0d0RCUyQk9pTiUyQnhsM1ZFdGZiSEg; _clck=11t8yox|1|f9e|0; _fbp=fb.1.1677088496378.378404472; g_state={"i_p":1677216546196,"i_l":2}; csrftoken=HxDW4Gl0Y3llNbR5rFGwfx9ilBEruwgR; G_ENABLED_IDPS=google; _qg_fts=1677131805; QGUserId=5955504104362824; _qg_cm=2; iprotrkid=; iprocname=http://hfmail.clovmail.com/; _clsk=7ysszz|1677218591194|4|1|s.clarity.ms/collect; _cfuvid=PpYVzri2bkSkp7XkhortiGiv4qSg5LytY0l1xGsReqk-1677216043236-0-604800000; whatsup_checked=1; __cf_bm=O1IaNImuXwpPrxbQBzDloD57bNGlqUVazdPpMf_KZow-1677220418-0-AWBhXiSqT+iZnZWZ0BiYeepubDy3msEICYF5aRfkMrcWpcUFKbmkpTrYqZYkFNLukKlFkdh3NrbzT4oPuAdhpL8=; nur=None',
        # 'Upgrade-Insecure-Requests': '1',
        # 'Sec-Fetch-Dest': 'document',
        # 'Sec-Fetch-Mode': 'navigate',
        # 'Sec-Fetch-Site': 'none',
        # 'Sec-Fetch-User': '?1',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }


    def start_requests(self):
        url = 'https://www.clovia.com/nightwear/s/' #'https://www.clovia.com/active-wear/s/'
        # headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:109.0) Gecko/20100101 Firefox/110.0'}
        yield scrapy.Request(url,callback = self.apihit,headers=self.headers,dont_filter=True)

    def apihit(self,response):
        page = 1
        category = response.url.split('/')[-3]
        api = f'https://www.clovia.com/web/api/v1/category-products-desktop/{category}/s/?page={page}'
        yield scrapy.Request(api, headers=self.headers, callback = self.listpage,meta={'page':page,'category':category},dont_filter=True)
    
    def listpage(self,response):
        category = response.meta.get('category')
        page = response.meta['page']+1
        landingUrl = response.url
        js = response.json()
        products = js['result']['products']
        for product in products:
            id = product['id']
            Title = product['name']
            Pro_url = 'https://www.clovia.com/product/'+product['slug']+'/'
            List_price = product['rounded_up_unit_price_ui']
            old_price_ui = product['old_price_ui']
            image = product['images']['second_image_url']
            offer_tag = product['offer_tag']
            yield scrapy.Request(Pro_url, callback= self.detail_api, dont_filter=True, headers=self.headers,
            meta= {
                'id':id,
                'Title':Title,
                'Pro_url':Pro_url,
                'List_price':List_price,
                'old_price_ui':old_price_ui,
                'image':image,
                'offer_tag':offer_tag,
                'landingURL':landingUrl
            })
        total = js['result']['total_count']
        if total >= js['result']['page']:
            api = f'https://www.clovia.com/web/api/v1/category-products-desktop/{category}/s/?page={page}'
            yield scrapy.Request(api, headers=self.headers, callback = self.listpage,meta={'page':page,'category':category},dont_filter=True)
        
    def detail_api(self,response):
        id = response.url.split('/')[-2]
        api = f'https://www.clovia.com/web/api/v1/product-desktop/{id}/'
        # yield JsonRequest(api,hea)
        yield scrapy.Request(api, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0'}, callback=self.detailpage, dont_filter=True)

    def detailpage(self,response):
        js = response.json()
        Title = js['name']
        product_url = js['url']
        sku = js['sku']
        description = ", ".join([i.text.strip() for i in BS(js['description'],'html.parser').find_all('p')])
        # short_description = js['short_description']
        old_price = js['old_price_ui']
        unit_price = js['rounded_up_unit_price_ui']
        gallery = js['gallery']
        images = []
        videos = []
        
        for i in gallery:
            try:
                images.append(i['img_l'])
            except:
                images = ''
            try:
                # if i.get('url'):
                videos.append(i.get('url'))
            except:
                videos = ''
            # vedio = i.get('url')
        yield  {
            'Title':Title,
            'product_url':product_url,
            'sku':sku,
            'old_price':old_price,
            'unit_price':unit_price,
            'description':description,
            # 'short_description':short_description,
            'images':images,
            'video':videos
        }