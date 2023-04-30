import scrapy


class MyerCrawlerSpider(scrapy.Spider):
    name = "myer_crawler"
    allowed_domains = ["*"]
    # start_urls = ["http://myer.com/"]
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0'
    }
    

    def start_requests(self):
        page = 1
        keyword = 'lips'
        # https://www.myer.com.au/search?query=lips&pageNumber=4
        # url = f'https://www.myer.com.au/search?pageNumber={page}&query={keyword}'#for the keyword 
        url = f'https://www.myer.com.au/c/men/mens-shoes/mens-sneakers?pageNumber={page}' # for the category
        yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True, meta= {'page':page, 'keyword':keyword} )

    def listpage(self, response):
        keyword = response.meta.get('keyword')
        page = response.meta['page'] +1
        products = response.xpath('//li[@class =" css-1xh07ad"]')
        for product in products:
            Title = product.xpath('.//h3//span[@class ="screen-reader-text"]//text()').get()
            Product_link = 'https://www.myer.com.au'+product.xpath('.//a/@href').get()
            Brand = product.xpath('.//span[@class = "MuiTypography-root makeStyles-root-1 makeStyles-root-329 css-1gvk5yl MuiTypography-body1"]//text()').get()
            Price = product.xpath('.//div[@class = "MuiGrid-root MuiGrid-item"]//span[@data-automation = "product-price-was"]//text()').get()
            image = product.xpath('.//div[@class = "css-wxpm9l"]//img/@src').get()
            yield scrapy.Request(Product_link, callback=self.detailpage, dont_filter=True, headers=self.headers,
            meta = {
                'landingUrl':response.url,
                'Title':Title,
                'Product_link':Product_link,
                'Brand':Brand,
                'Price':Price,
                'image':image,
            })
        nextpage = response.xpath('//a[@aria-label = "Next Page"]/@href').get()
        if nextpage:
            # url = f'https://www.myer.com.au/search?pageNumber={page}&query={keyword}'
            url = f'https://www.myer.com.au/c/men/mens-shoes/mens-sneakers?pageNumber={page}'
            yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True, meta= {'page':page, 'keyword':keyword} )
            
    def detailpage(self, response):
        Name = response.xpath('//span[@data-automation = "product-title"]//text()').get()
        D_price = response.xpath('//h3//text()').get()
        Colors = response.xpath('//div[@data-automation = "pdp-colour-container-desktop"]//@value').get()
        descriiption = response.xpath('//div[@data-automation = "product-description-description"]//text()').get()
        delivery = response.xpath('//div[@class ="css-4cxybv"]//div[@class = "row"]//p//text()').get()
        images_all = response.xpath('//ol[@class = "css-1ui811p"]//li//a//img/@src').get()

        yield {
            'landingUrl':response.meta.get('url'),
            'Title':response.meta.get('Title'),
            'Product_link':response.meta.get('Product_link'),
            'Brand':response.meta.get('Brand'),
            'Price':response.meta.get('Price'),
            'image':response.meta.get('image'),
            'Name':Name,
            'D_price':D_price,
            'Colors':Colors,
            'descriiption':descriiption,
            'delivery':delivery,
            'images_all':images_all
        }
