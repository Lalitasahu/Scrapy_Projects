import scrapy


class BebellacosmeticsCrwalSpider(scrapy.Spider):
    name = "bebellacosmetics_crwal"
    allowed_domains = ["bebellacosmetics.com"]
    # start_urls = ["http://bebellacosmetics.com/"]

    def start_requests(self):
        url = 'https://bebellacosmetics.com/collections/face'
        yield scrapy.Request(url,callback=self.listpage)
    
    def listpage(self,response):
        products = response.xpath('//div[@class = "product--root"]')
        for product in products:
            name = product.xpath('.//div[@class = "product--title font--block-heading"]//text()').get()
            link = 'https://bebellacosmetics.com'+product.xpath('.//div[@class = "product--details"]//a/@href').get()
            price = product.xpath('.//span[@class = "money"]//text()').get()
            images = product.xpath('//div[@class = "image--container"]//img[@class = "lazyload lazypreload"]/@data-src').get()
            # meta = {
            #     'name':name,
            #     'link':link,
            #     'price':price,
            #     'images':images

            # }
            yield scrapy.Request(link,callback=self.detailpage)
    def detailpage(self,response):
        bread = response.xpath('//li[@class = "font--block-link"]//text()').get()
        Title = response.xpath('//li[@class = "font--accent"]//text()').get()
        images = response.xpath('//div[@class = "product-page--thumbs-container"]//img/@data-src').get().replace('{width}','883')
        sele_price = response.xpath('//p[@class = "price--container"]//span[@class = "actual-price font--accent money"]//text()').get()
        description = response.xpath('//div[@class = "rte-content"]//text()').get()
        ingredients = response.xpath('//h6//span//text()').get()
        yield{
            'bread':bread,
            'Title':Title,
            'images':images,
            'sele_price':sele_price,
            'description':description,
            'ingredients':ingredients
        }




import scrapy


class A21favesCrawlSpider(scrapy.Spider):
    name = "faves_crawl"
    allowed_domains = ["faves.com"]
    # start_urls = ["http://21faves.com/"]

def start_requests(self):
    url = 'https://www.21faves.com/collections/one-pieces?spm=..index.products_1'
    yield scrapy.Request(url,callback=self.listpage)

def listpage(self,response):
    total_product = response.xpath('//span[@class = "collection__number"]//text()').replace('products','').get()
    products = response.xpath('//div[@class = "col-6 col-md-3 common__product-gap"]')
    for product in products:
        Pro_link = product.xpath('.//a/@href').get()
        images = product.xpath('//a//img/@src').get()
        title = product.xpath('//div[@class = "col-6 col-md-3 common__product-gap"]//a//text()').get()
        price = product.xpath('//span[@class = "text-truncate dj_skin_product_price money"]//text()').get()
        list_price = product.xpath('//del[@class = "text-truncate dj_skin_product_compare_at_price money"]//text()').get()
        yield{
            'Pro_link':Pro_link,
            'images':images,
            'title':title,
            'price':price,
            'list_price':list_price
        }