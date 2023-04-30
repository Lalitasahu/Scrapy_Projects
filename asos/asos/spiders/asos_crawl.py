import scrapy


class AsosCrawlSpider(scrapy.Spider):
    name = "asos_crawl"
    allowed_domains = ["asos.com"]
    # start_urls = ["http://asos.com/"]
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0'}

    def start_requests(self):
        url = 'https://www.asos.com/women/a-to-z-of-brands/miss-selfridge/cat/?cid=25520&ctaref=hp|ww|prime|moment|2|edit|missselfridge'
        yield scrapy.Request(url, callback=self.listpage, headers=self.headers)
    
    def listpage(self, response):
        # soup = BS(response.text,'html.parser')
        products = response.xpath('//article[@class = "productTile_U0clN"]')
        for product in products:
            Title = product.xpath('.//div[@class = "overflowFade_zrNEl"]//text()').get()
            pro_link = product.xpath('//a[@class = "productLink_KM4PI"]/@href').get()
            list_price = product.xpath('.//p[@class = "container_WYZEU"]//span[@class = "price_CMH3V"]//text()').get()
            sale_price = product.xpath('.//p[@class = "container_WYZEU"]//span[@class = "reducedPrice_lSm0L"]//text()').get()
            # image = tree.xpath('//a[@class = "productLink_KM4PI"]//div[@class ="container_ApgHk"]//img/@srcset'# image con't find ?
            # yield scrapy.Request(pro_link,callback=self.listpage, dont_filter=True,headers=self.headers,
            yield {
                'landingUrl':response.url,
                'Title':Title,
                'pro_link':pro_link,
                'list_price':list_price,
                'sale_price':sale_price,
            }
        nextpage = response.xpath('//a[@class ="loadButton_i3U2b"]/@href')
        if nextpage:
            yield scrapy.Request(nextpage.get(), callback=self.listpage, headers=self.headers,dont_filter=True)


    def detailpage(self, response):
        bread = []
        for i in response.xpath('//nav[@class = "_1MMuO3r"]'):
            breadcurms = i.xpath('.//li//a//text()')
            bread.append(breadcurms).get()
        Name = response.xpath('//h1//text()').get()
        