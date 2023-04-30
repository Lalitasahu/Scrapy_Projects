import scrapy


class BambinifationCrawlSpider(scrapy.Spider):
    name = "Bambinifation_crawl"
    allowed_domains = ["Bambinifation.com"]
    # start_urls = ["http://Bambinifation.com/"]
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0'}

    def start_requests(self):
        url = 'https://bambinifashion.com/girl'
        # url = 'https://bambinifashion.com/girl/arts-crafts'
        yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True)
    
    def listpage(self,response):
        products = response.xpath('//div[@class = "category-list-product has-size-tooltip product-card"]')
        for product in products:
            try:
                Title = product.xpath('.//div[@class = "product-card-title"]//text()').get()
            except:
                Title = ''

            try:
                pro_link = 'https://bambinifashion.com'+product.xpath('.//a[@class = "product-image-carousel"]/@href').get()
            except:
                pro_link = ''

            try:
                price = product.xpath('.//div[@class = "product-price product-card-price"]//span//text()').get()
            except: 
                price = ''

            try:
                brand = product.xpath('.//div[@class = "product-card-brand"]//text()').get().replace('\t','').replace('\n','')
            except:
                brand = ''
            yield scrapy.Request(pro_link,callback=self.detailpage,headers=self.headers, dont_filter=True,
            meta= {
                'Title':Title,
                'pro_link':pro_link,
                'price':price,
                'brand':brand,
                # 'offer':offer
            })
            # yield {
            #         'Title':Title,
            #         'pro_link':pro_link,
            #         'price':price,
            #         'brand':brand,
            #         # 'offer':offer
            #     }
        nextpage = response.xpath('//li[@class = "pagination-item--next"]//a/@href')
        if nextpage:
            yield scrapy.Request('https://bambinifashion.com'+nextpage.get(),callback=self.listpage, headers=self.headers, dont_filter=True)

    def detailpage(self,response):
        session = response.xpath('//div[@class = "product-single-timing product-single-timing--new-season"]//text()').get()
        Name = response.xpath('//h1[@class = "product-single-description"]//text()').get()
        Detail_price = response.xpath('//div[@class = "product-price"]//span//text()').get()
        image = response.xpath('//div[@class = "product-thumbnails"]//div//img/@srcset').get()
        specification = {}
        for heading in response.xpath("//div[@class='product-tab-section--details-column']"):
            h3 = ''.join(heading.xpath(".//h3//text()").getall()).strip().replace("\n","").replace("\t","")
            value = ' | '.join(heading.xpath(".//li/text()").getall()).strip().replace("\n","").replace("\t","")
            specification[h3] = value
        yield {
            'session':session,
            'Name':Name,
            'Detail_price':Detail_price,
            'image':image,
            'specification':specification,
        }