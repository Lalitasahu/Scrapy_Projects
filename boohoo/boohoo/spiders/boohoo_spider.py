import scrapy
import json

class BoohooSpiderSpider(scrapy.Spider):
    name = "boohoo_spider"
    allowed_domains = ["boohoo.com"]
    # start_urls = ["http://boohoo.com/"]
    headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
        }


    def start_requests (self):
        url = 'https://www.boohoo.com/mens/mens-suits'
        yield scrapy.Request(url, callback=self.listpage, headers=self.headers)

    def listpage(self, response):
        products = response.xpath('//div[@class = "b-product_tile-container"]')
        for product in products:
            
            title = "".join(product.xpath('.//h3//a[@class = "b-product_tile-link"]//text()').getall()).strip()
            Pro_link = product.xpath('.//h3//a[@class = "b-product_tile-link"]/@href').get()
            if 'https:' in Pro_link:
                Pro_link = Pro_link
            else:
                Pro_link = 'https://www.boohoo.com'+Pro_link
            
            sele_price = product.xpath('.//span[@class = "b-price-item m-new"]//text() | //span[@itemprop="price"]/@content').get()
            list_price = product.xpath('.//span[@class = "b-price-item m-old"]//text() | //span[@itemprop="price"]/@content').get()
            off = product.xpath('.//span[@class = "b-price-discount"]//text()').get()   
            yield scrapy.Request(Pro_link,callback=self.detailpage, headers = self.headers,
            meta = {
                'landingpageUrl':response.url,
                'title':title,
                'Pro_link':Pro_link,
                'sele_price':sele_price,
                'list_price':list_price,
                'off':off,
                
                })


        nextpage = response.xpath('//div[@class = "b-load_more"]//a/@href').get()
        if nextpage:
            yield scrapy.Request(nextpage, callback= self.listpage, headers= self.headers)

    def detailpage(self, response):
        breadcrums = '||'.join(response.xpath('//nav[@class = "b-breadcrumbs m-pdp_lastitemmod"]//span[@itemprop="name"]//text()').getall())
        name = response.xpath('//h1//text()').get()
        first_price = response.xpath('//div[@class = "b-product_details-form"]//span[@class = "b-price-item m-new"]//text() | //span[@itemprop="price"]/@content').get()
        second_price = response.xpath('//div[@class = "b-product_details-form"]//span[@class = "b-price-item m-old"]//text() | //span[@itemprop="price"]/@content').get()
        de_off = response.xpath('//div[@class = "b-product_details-form"]//span[@class = "b-price-discount"]//text()').get()
        key = response.xpath('//span[@class = "b-variation_label-name"]//text()').getall()
        value = response.xpath('//span[@class = "b-variation_label-value"]//text()').getall()
        info = dict(zip(key,value))
        return_item =  response.xpath('//div[@class = "b-product_shipping-returns_content"]//text()').getall()
        delivery = ''.join(response.xpath('//div[@class = "b-product_delivery"]//text()').get()).replace('\n','')
        product_details = response.xpath('//div[@class = "b-product_details-content"]//p//text()').get()
        # print(return_item)
        yield{
            'landingpageUrl':response.meta.get('landingpageUrl'),
            'title':response.meta.get('title'),
            'Pro_link':response.meta.get('Pro_link'),
            'sele_price':response.meta.get('sele_price'),
            'list_price':response.meta.get('list_price'),
            'off':response.meta.get('off'),
            'breadcrums':breadcrums,
            'name':name,
            'first_price':first_price,
            'second_price':second_price,
            'de_off':de_off,
            'info':info,
            'return_item':return_item,
            'delivery':delivery,
            'product_details':product_details
        }