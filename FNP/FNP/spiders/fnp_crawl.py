import scrapy
import re
from bs4 import BeautifulSoup as bs


class FnpCrawlSpider(scrapy.Spider):
    name = "fnp_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://fnp.com/"]
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'x-device-type': 'desktop',
    'x-domain': 'www.fnp.com',
    'Origin': 'https://www.fnp.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.fnp.com/',
    # 'Cookie': 'AMCV_43C357DF589484E40A495D80%40AdobeOrg=-408604571%7CMCIDTS%7C19435%7CMCMID%7C58089079171669955481761007840489044653%7CMCAAMLH-1679727333%7C12%7CMCAAMB-1679727333%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1679129733s%7CNONE%7CvVersion%7C4.6.0; AMCVS_43C357DF589484E40A495D80%40AdobeOrg=1; s_cc=true; localCurrency=INR; _gcl_au=1.1.687821302.1679122533; AMO-tid=312549610; usid=1819312847; _ga_Q3470S4J87=GS1.1.1679149091.2.0.1679149091.60.0.0; _ga=GA1.1.1699291.1679122534; _gid=GA1.2.1521758041.1679122534; _fbp=fb.1.1679122534679.41387439; cto_bundle=ODpk-193dnZTbThsaTRzU2hHOVpBYUxCelZGNFluOUZJWEM5TlRWOCUyRkltVyUyRmRnOHVTRFY0Q0RsakJhOXBYaDBuSnRDZGhMTHdHbDBIMnVtVVJWbGhuTDBXVXJrcmNhWEQyYVJnU2JOS1VNMGltcGh5UVA3TyUyRmFPRXh0cWdHMnpGTCUyRnhNayUyRkZnMjJUN3Eyb2IzS1RCeld2biUyQm81ekNCWU1NeVJDc1VnZTZHbEgyRlBrQWJ0QjB3bTRsbHlMT0U0MDlLWEI; language-preference=en; _uetsid=e1038830c55911ed9b17ad40aea2b433; _uetvid=e1037770c55911ed920297199eee1fcb; gpv_pn=fnp%20ind%3Aplp%3Acanada%3Agifts%20to%20vancouver',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

    # params = {
    #     'currency': 'INR',
    #     'geoId': 'canada',
    #     'isFacetEnabled': 'true',
    #     'page': '2',
    #     'size': '36',
    #     'categoryUrl': 'fnp.com/canada/gifts/vancouver-lp',
    #     'domainId': 'fnp.com',
    #     'lang': 'en',
    #     'isOnScroll': 'true',
    # }
    def start_requests(self):
        url = 'https://www.fnp.com/cakes/wedding-lp?promo=cakesmenu_dt_hm'
        yield scrapy.Request(url, headers=self.headers, callback=self.api, dont_filter=True)
    
    def api(self, response):
        catlogID = response.url.split('?')[0].replace('https://www.','')
        page = 1
        
        apiurl = f'https://atcdel.fnp.com/columbus/v1/productList?currency=INR&geoId=canada&isFacetEnabled=true&page={page}&size=36&categoryUrl={catlogID}&domainId=fnp.com&lang=en&isOnScroll=true'
        yield scrapy.Request(apiurl, headers=self.headers,dont_filter=True, callback=self.listpage, meta={'page':page, 'catlogID': catlogID})

    def listpage(self, response):
        js = response.json()
        catlogID = response.meta.get('catlogID')
        page = response.meta['page']+1
        products = js['data']
        for i  in products:
            productId = i['productId']
            productName = i['productName']
            productUrl = 'https://www.fnp.com'+i['productUrl']
            sku = i['sku']
            listPriceMax = i['price']['listPriceMax']
            price = i['price']['mrp']
            image = 'https://www.fnp.com'+i['productImage']['imageUrl']
            yield scrapy.Request(productUrl, callback=self.detailpage, dont_filter=True, headers=self.headers,
            meta = {
                'productId':productId,
                'productName':productName,
                'productUrl':productUrl,
                'sku':sku,
                'listPriceMax':listPriceMax,
                'price':price,
                'image':image
            })
            
        if js['totalPages'] > js['currentPage']:
            apiurl = f'https://atcdel.fnp.com/columbus/v1/productList?currency=INR&geoId=canada&isFacetEnabled=true&page={page}&size=36&categoryUrl={catlogID}&domainId=fnp.com&lang=en&isOnScroll=true'
            yield scrapy.Request(apiurl, headers=self.headers,dont_filter=True, callback=self.listpage,meta={'page':page, 'catlogID':catlogID} )
    
    def detailpage(self, response):
        Title = response.xpath('//h1//text()').get()    
        Price = response.xpath('//span[@class = "odometer odometer-auto-theme"]//text()').get()
        image = response.xpath('//div[@class = "slick-list"]//img[@id ="thumbnail_1"]/@data-image').get()
        Specification = {}
        for i in response.xpath('//div[@class = "product-desc-desktop_descriptionTitle__2Q-Ha"]'):
            hd = i.xpath('//h4//text()').get()
            dd = i.xpath('//ul//text()').get()
            Specification[hd] = dd
        # for j in response.xpath('//div[@class = "slide-item active"]'):
        #     img = j.xpath('.//img/@src').get()
        # soup = bs(response.text,'html.parser')
        # Title = soup.find('h1').get()
        # Price = soup.find('span','odometer odometer-auto-theme').text
        # Specification = {}
        # for i in soup.find_all('div','product-desc-desktop_descriptionTitle__2Q-Ha'):
        #     hd = i.find('h4').tex
        #     dd = i.find('ul').text
        #     Specification[hd] = dd
        # for i in soup.find_all('div','slide-item active'):
        #     img = i.find('img').get('src')

        yield {
            'Title':Title,
            'Price':Price,
            'Specification':Specification,
            'image':image
        }