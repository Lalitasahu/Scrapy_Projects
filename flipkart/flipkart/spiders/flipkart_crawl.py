import scrapy
# from scrapy

class FlipkartCrawlSpider(scrapy.Spider):
    name = "flipkart_crawl"
    allowed_domains = ["flipkart.com"]
    # start_urls = ["http://flipkart.com/"]
    headers ={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
    }


    def start_requests(self):
        # url = "https://www.flipkart.com/search?q=iphone&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"
        url = "https://www.flipkart.com/search?q=dell&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        # for i in urls:
        yield scrapy.Request(url,callback = self.parse_listPage, headers = self.headers)

    def parse_listPage(self,response):
        # print(response)
        
        products = response.xpath('//div[@class="_1AtVbE col-12-12"]')
        for i in products:        
            name = i.xpath('.//div[@class="_4rR01T"]//text()').get()
            link = i.xpath('.//a[@class="_1fQZEK"]/@href').get()
            if name and link:
                yield scrapy.Request('https://www.flipkart.com'+link,callback = self.parse_detail, headers = self.headers,meta={'name':name,'link':link})

         
        nextpage = response.xpath('//nav[@class="yFHi8N"]//a//span[contains(text(),"Next")]/parent::a/@href').get()
        if nextpage:
            yield scrapy.Request('https://www.flipkart.com'+nextpage,callback = self.parse_listPage, headers = self.headers)


    def parse_detail(self,response):

        sold = response.xpath('//div[@class = "_16FRp0"]//text()').get()
        price = response.xpath('//div[@class = "_30jeq3 _16Jk6d"]//text()').get()
        description = response.xpath('//div[@class = "_1mXcCf RmoJUa"]//text()').get()
        yield {
            'sold':sold,
            'price':price,
            'description':description,
            'pro_url': response.url,
            'name':response.meta.get('name'),
            'link':response.meta.get('link')            
        }
        





