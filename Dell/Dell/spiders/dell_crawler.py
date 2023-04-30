import scrapy
import math
import mysql.connector

class DellCrawlerSpider(scrapy.Spider):
    conn = mysql.connector.connect(host="localhost", user="root", passwd="Lalita@123", db="crawling",charset="utf8", use_unicode=True)
    cursor = conn.cursor(dictionary=True)

    name = "dell_crawler"
    allowed_domains = ["*"]
    # start_urls = ["http://dell.com/"]
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0'
    }
    def start_requests(self):
        url = ['https://www.dell.com/en-in/shop/scc/sr/desktops/inspiron-desktops?page=1']
        for i in url:
            yield scrapy.Request(i, headers=self.headers, callback=self.urlall, dont_filter=True)


    def urlall(self, response):
        page = 1
        seotext = response.xpath('//input[@type="radio"]/@seotext').get()
        typeL_D = response.url.split('/')[-2]
        categery = response.url.split('/')[-1]
        url = f'https://www.dell.com/en-in/shop/{seotext}/sr/{typeL_D}/{categery}?page={page}'
        # url = f'https://www.dell.com/en-in/shop/laptops-2-in-1-pcs/sr/laptops/inspiron-laptops?page={page}'
        yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True, meta={'page':page})
    
    def listpage(self, response):
        page = response.meta['page']+1
        # print(response)
        # total = math.ceil(int(response.xpath('//span[@class = "pageinfo"]//text()').get().replace('1 to 12 of ','').replace(' Results',''))/12)
        # for i in range(1,total+1):
        products = response.xpath('//article')
        for product in products:
            Title = product.xpath('.//div[@class = "ps-system-title-container ps-title-container"]//a//text()').get().strip()
            Pro_link = product.xpath('.//h3/a/@href').get().strip()
            key = products.xpath('.//div[@class = "ps-iconography-container"]//span[@class = "ps-iconography-specs-title"]//text()').getall()
            value = products.xpath('.//div[@class = "ps-iconography-container"]//span[@class = "ps-iconography-specs-label"]//text()').getall()
            info = dict(zip(key, value))
            for i in info:
                if i.strip() == 'Processor':
                    processor = info.get(i).strip()
                elif i.strip() == 'OS':
                    OS = info.get(i).strip()
                elif i.strip()  == 'Graphics':
                    Graphics = info.get(i).strip()
                elif (i.strip() == 'Memory'):
                    Memory = info.get(i).strip()
                elif (i.strip() == 'Storage'):
                    Storage = info.get(i).strip()
                elif (i.strip() == 'Display'):
                    Display = info.get(i).strip()
            online_price = product.xpath('.//div[@class = "ps-pricing-container"]//span[@class = "strike-through"]//text()').get().strip()
            sale_price = product.xpath('.//div[@class = "ps-dell-price ps-simplified"]//span//text()').get().strip()
            save_price = "".join(product.xpath('.//div[@class = "ps-pricing-container"]//div[@class = "ps-sav"]')[0].xpath('./span//text()').extract())
            offer = product.xpath('.//ul//li//button[@class = "ps-special-offers-expanded-link"]//text()').get().strip()
            Financing = response.xpath('.//div[@class = "ps-fin  "]//p//a//text()').get().strip()
            yield {
                    'Title':Title,
                    'Pro_link':Pro_link,
                    'processor':processor,
                    'OS':OS,
                    'Graphics':Graphics,
                    'Memory':Memory,
                    'Storage':Storage,
                    'Display':Display,
                    'online_price':online_price,
                    'sale_price':sale_price,
                    'save_price':save_price,
                    'offer':offer,
                    'Financing':Financing   
                }
            #raw = [Title, Pro_link, info÷÷]
            query = "insert into Dell_info(Title,Pro_link,processor,OS,Graphics,Memory,Storage,Display,online_price,sale_price,save_price,offer,Financing) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values = [Title,Pro_link,processor,OS,Graphics,Memory,Storage,Display,online_price,sale_price,save_price,offer,Financing]
            # print(values)
            self.cursor.execute(query,values)
            self.conn.commit()
            # print(f"inserted...{Title}")

        # total_Product = int(response.xpath('//span[@class = "pageinfo"]//text()').get().replace('1 to 12 of ','').replace(' Results',''))/12
        # total = math.ceil(total_Product)
        # if total >= page:
        nextp = response.xpath('//button[@data-disabled = "False"]//text()').getall()
        for i in nextp:
            if i == "Next":
                url = f'https://www.dell.com/en-in/shop/laptops-2-in-1-pcs/sr/laptops/inspiron-laptops?page={page}'
                yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True, meta={'page':page})

            