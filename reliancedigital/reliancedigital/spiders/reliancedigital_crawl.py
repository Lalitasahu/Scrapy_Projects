import scrapy


class ReliancedigitalCrawlSpider(scrapy.Spider) :
    name = "reliancedigital_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://reliancedigital.com/"]
    headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0'
    }

    # def start_requests(self):
    #     m_url = 'https://www.reliancedigital.in'
    #     yield scrapy.Request(m_url, callback=self.allUrl, headers=self.headers, dont_filter=True)

    def start_requests(self):
        # cat = 
        # out_of_stock = 
        page = 0
        url = f'https://www.reliancedigital.in/multimedia-speakers/c/10102015?searchQuery=:relevance:prodfeatures:Bluetooth&page={page}'
        yield scrapy.Request(url, callback=self.listpage, dont_filter=True, headers=self.headers, meta = {'page':page})
    
    def listpage(self, response):
        page = response.meta['page'] +1
        products = response.xpath('//div[@class = "sp grid"]')
        for product in products:
            product_link = 'https://www.reliancedigital.in'+product.xpath('.//a/@href').get()
            product_Name = product.xpath('.//p[@class ="sp__name"]//text()').get()
            price = product.xpath('.//span[@class = "TextWeb__Text-sc-1cyx778-0 llZwTv"]//text()').getall()
            list_price = product.xpath('.//em//text()').getall()
            discount_price = product.xpath('.//span[@class ="TextWeb__Text-sc-1cyx778-0 UGvlv Block-sc-u1lygz-0 bsVFzL"]//text()').get()
            image = 'https://www.reliancedigital.in'+product.xpath('.//img/@src').get()

            yield {
                'product_link':product_link,
                'product_Name':product_Name,
                'price':price,
                'list_price':list_price,
                'discount_price':discount_price,
                'image':image

            }
        nextpage = response.xpath('//i[@class = "fa fa-angle-right"]').get()
        if nextpage:
            url = f'https://www.reliancedigital.in/multimedia-speakers/c/10102015?searchQuery=:relevance:prodfeatures:Bluetooth&page={page}'
            yield scrapy.Request(url, callback=self.listpage, dont_filter=True, headers=self.headers, meta={'page':page})

