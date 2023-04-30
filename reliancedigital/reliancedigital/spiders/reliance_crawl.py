import scrapy
from bs4 import BeautifulSoup as bs


class RelianceCrawlSpider(scrapy.Spider):
    name = "reliance_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://reliace.com/"]
    # headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0'}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Referer': 'https://www.reliancedigital.in/multimedia-speakers/c/10102015?searchQuery=:relevance:prodfeatures:Bluetooth&page=2',
    'Content-Type': 'application/json',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    'Cookie': 'RT="z=1&dm=www.reliancedigital.in&si=bb9dadc1-7926-4375-bf42-1b7874b32ff6&ss=lg1txzpf&sl=1&tt=54i&rl=1&ld=54j"; _gcl_aw=GCL.1680328391.Cj0KCQjwiZqhBhCJARIsACHHEH8WOrBHOG13C9dRJs4_DtbqhgeYbx-ST0bTA1WpHEBZLWyHiLb-gHsaAj0KEALw_wcB; _gcl_au=1.1.1560453280.1680246725; WZRK_G=5711dd1521f14198ab226975e416efb3; _ga_1DPVQ3BW9G=GS1.1.1680586733.5.1.1680586746.47.0.0; _ga=GA1.2.782144513.1680246725; _gac_UA-27422335-1=1.1680328392.Cj0KCQjwiZqhBhCJARIsACHHEH8WOrBHOG13C9dRJs4_DtbqhgeYbx-ST0bTA1WpHEBZLWyHiLb-gHsaAj0KEALw_wcB; OMG-2337324=SSKey=&UUserID={aa33a9d5-52e1-4d94-9886-ac3130df9241}&fpc=true&attributionMode=fpc&AttributionPartnerRef=Cj0KCQjwiZqhBhCJARIsACHHEH8WOrBHOG13C9dRJs4_DtbqhgeYbx-ST0bTA1WpHEBZLWyHiLb-gHsaAj0KEALw_wcB&channel=Google Adwords; _fbp=fb.1.1680246729220.135206149; version=4.3.1; citrix_ns_id_.reliancedigital.in_%2F_wat=AAAAAAVaUJ87jqt5v6GAA60DcxuERBE5jax9vrqH7_h0mNwBJqeQk-Dq_fXAm0W3gNKY1Z9iF07lQIHuc9qd5dUC5Fcc&; AKA_A2=A; HttpOnly; WZRK_S_8R5-85Z-K95Z=%7B%22p%22%3A1%2C%22s%22%3A1680586733%2C%22t%22%3A1680586733%7D; _uetsid=fbf68770d2aa11eda0862f29fb196f6b; _uetvid=5771ce60cf9311eda9b71110c50e4a61; _gid=GA1.2.1327177219.1680586735; _dc_gtm_UA-27422335-1=1; _gat_UA-27422335-1=1',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

    def start_requests(self):
        page = 0
        url = f'https://www.reliancedigital.in/tablets-ereaders/c/S101712?searchQuery=&page=0{page}'
        # url = 'https://www.reliancedigital.in/multimedia-speakers/c/10102015?searchQuery=:relevance:prodfeatures:Bluetooth&page=1'
        yield scrapy.Request(url, callback=self.apifun, headers=self.headers, dont_filter=True, meta= {'page':page} )

    def apifun(self, response):
        cat_id = response.url.split('?')[0].split('/')[-1]
        page = response.meta['page']+1
        apiurl = f'https://www.reliancedigital.in/rildigitalws/v2/rrldigital/cms/pagedata?pageType=categoryPage&categoryCode={cat_id}&searchQuery=&page={page}&size=24&pc='
        yield scrapy.Request(apiurl, callback=self.listpage, headers=self.headers, dont_filter=True, meta={'page':page, 'cat_id':cat_id})

    def listpage(self, response):
        cat_id = response.meta.get('cat_id')
        page = response.meta['page']+1
        js = response.json()
        products = js['data']['productListData']['results']
        for product in products:
            name = product['name']
            id = product['code']
            pro_url = 'https://www.reliancedigital.in'+product['url']
            description = bs(product['description'],'html.parser').text
            list_price = product['price']['value']
            sale_price = product['price']['formattedValue']
            discount = product['price']['discount']
            image = 'https://www.reliancedigital.in'+product['media'][0]['thumbnailUrl']
            time = product['onlineDate']

            yield {
                'name':name,
                'id':id,
                'page':page,
                'pro_url':pro_url,
                'description':description,
                'list_price':list_price,
                'sale_price':sale_price,
                'discount':discount,
                'image':image,
                'time':time
            }
        
        total = js['data']['productListData']['pagination']['pageSize']
        current_page = js['data']['productListData']['pagination']['currentPage']
        if int(total) > int(current_page):
            apiurl = f'https://www.reliancedigital.in/rildigitalws/v2/rrldigital/cms/pagedata?pageType=categoryPage&categoryCode={cat_id}&searchQuery=&page={page}&size=24&pc='
            yield scrapy.Request(apiurl, callback=self.listpage, headers=self.headers, dont_filter=True, meta={'page':page, 'cat_id':cat_id})