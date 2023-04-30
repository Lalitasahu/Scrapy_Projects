import scrapy


class CupsheCrawlSpider(scrapy.Spider):
    name = "cupshe_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://cupshe.com/"]

    def start_requests(self):
        url = 'https://www.cupshe.com/collections/dress?icn=dresses&ici=navbar11'
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:109.0) Gecko/20100101 Firefox/110.0'}
        # headers = {
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
        # 'Accept': 'application/json, text/plain, */*',
        # 'Accept-Language': 'en-US,en;q=0.5',
        # # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Alt-Used': 'www.clovia.com',
        # 'Connection': 'keep-alive',
        # 'Referer': 'https://www.clovia.com/product/skivia-onion-oil-mini-shampoo-with-reetha-keratin-30-ml/',
        # # 'Cookie': 'sessionid=xuc2zldg5x2y4o4ib357ploeq03x8068; http_referer_val="firstclicktime=2023-02-22 23:24:52.521154\\054http_referer=https://www.clovia.com/"; _gcl_au=1.1.1016531704.1677088494; _ga_TC6QEKJ4BS=GS1.1.1677218170.13.1.1677218187.43.0.0; _ga=GA1.1.1332762842.1677088495; _gid=GA1.2.1029297947.1677088495; cto_bundle=jdN_uF84RmNLeDlYbzZ6Mk5GZVdwVHh3bHFWelA1eiUyRnE2c2luelUzVWVScjNWRzBsYiUyRlBNczBraXBpWnFxdERhVGRJaG44N0RyNUNoZGFPOEF3Q3NsZWNwSFNMQWcxTEdpJTJCU3N5ekxrQTNGcnhZa0VnJTJGTWRKMmFRRHNhY0N4Y2FRdVRnSnhJdmlCRiUyRmZsTWNUbkhKMDQ2b1NWZ0pWQnlQMjdseWRvV0xJT3pyYmRZOUJoNGQyVzFmdGdDJTJGbkViN0MxajU; _clck=11t8yox|1|f9e|0; _fbp=fb.1.1677088496378.378404472; g_state={"i_p":1677216546196,"i_l":2}; csrftoken=HxDW4Gl0Y3llNbR5rFGwfx9ilBEruwgR; G_ENABLED_IDPS=google; _qg_fts=1677131805; QGUserId=5955504104362824; _qg_cm=2; iprotrkid=; iprocname=http://hfmail.clovmail.com/; _clsk=7ysszz|1677218183604|2|1|s.clarity.ms/collect; _cfuvid=PpYVzri2bkSkp7XkhortiGiv4qSg5LytY0l1xGsReqk-1677216043236-0-604800000; whatsup_checked=1; _qg_pushrequest=true; nur=None; __cf_bm=5Nb07KaZXDCiKin5y_S53cIP6dEYHJatDWU1g4Vub3s-1677217965-0-AewFiI8Z+y203i5NdfAzrgOsp1rJFtM4EmV8GgKHUkUeqGsV6a0d3QcX0q6d2HWwnurqE78eQYlJTw9p5jFFzA8=; _browsee=eyJfaWQiOiJkNjEwMTJjZDhjNzIiLCJfdCI6MTY3NzIxODE3MDMwOCwiX3IiOjAsIl9wIjp7ImNvIjpmYWxzZSwiZXQiOnRydWUsInByIjpbMV0sIml0IjpbXX19; _browseet=eyJfdCI6MTY3NzIxODE4MjcwMH0=; _gat=1; _gat_UA-62869587-2=1',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-origin',
        # # Requests doesn't support trailers
        # # 'TE': 'trailers',
        # }
        yield scrapy.Request(url,callback=self.apihit, headers=headers, meta={'url':url})
    
    def apihit(self, response):
        landingUrl = response.url
        page = 1
        api = f'https://bff-shopify.cupshe.com/service/col/page?seoUrl=dress&pageNum={page}&pageSize=48&sortId=1&brandId=1&channelId=1&terminalId=1&source=2&siteId=1&langCode=en-GB'
        yield scrapy.Request(api,callback=self.listpage, headers=self.headers, meta = {'landingUrl':landingUrl,'page':0},dont_filter=True)

    def listpage(self,response):
        page = response.meta['page']+1
        landingurl = response.url
        js = response.json()
        products = js['data']['dataDetail']
        for product in products:
            title = product['skcs'][0]['title']
            productId = product['skcs'][0]['productId']
            pro_url = 'https://www.cupshe.com/products/'+product['skcs'][0]['jumpPath']
            color = product['skcs'][0]['color']
            appSkcRetailPrice = product['skcs'][0]['appSkcRetailPrice']
            appSkcDiscountPrice = product['skcs'][0]['appSkcDiscountPrice']
            yield scrapy.Request(pro_url,callback=self.detailpage_api,dont_filter=True,headers=self.headers,
            meta= {
                'landingUrl':response.meta.get('landingUrl'),
                'title':title,
                'productId':productId,
                'pro_url':pro_url,
                'color':color,
                'appSkcRetailPrice':appSkcRetailPrice,
                'appSkcDiscountPrice':appSkcDiscountPrice
            })
        # pageNum = js['data']['pageNum']
        total = (js['data']['total'])//48
        if total >= js['data']['pageNum']:
            api = f'https://bff-shopify.cupshe.com/service/col/page?seoUrl=dress&pageNum={page}&pageSize=48&sortId=1&brandId=1&channelId=1&terminalId=1&source=2&siteId=1&langCode=en-GB'
            yield scrapy.Request(api,callback=self.listpage, meta = {'landingUrl':landingurl,'page':page},dont_filter=True, headers=self.headers)

    def detailpage_api(self, response):
        productId = response.meta.get('productId')
        api = f'https://cfs.cupshe.com/commodity/detail?siteId=1&lang=en-GB&currency=USD&notFilterVedioFlag=false&thirdProductId={productId}&brandId=1&channelId=1&terminalId=1'
        yield scrapy.Request(api, callback=self.detailpage, dont_filter=True, headers=self.headers)
    
    def detailpage(self, response):
        datas = response.json()
        details = datas['data']['commodities']
        for detail in details:
            landingURL = 'https://www.cupshe.com/products/'+detail['jumpPath']
            Title = detail['title']
            Id = detail['productId']
            description = detail['description'] # convert into text 
            images = detail['medias']
            for im in images:
                image = im['src']
            discountPrice = detail['skus'][0]['discountPrice']
            discountPriceStr = detail['skus'][0]['discountPriceStr']
            color = detail['color']
        yield {
            'landingURL':landingURL,
            'Title':Title,
            'Id':Id,
            'color':color,
            'description':description,
            'image': image,
            'discountPrice':discountPrice,
            'discountPriceStr':discountPriceStr
        }
        