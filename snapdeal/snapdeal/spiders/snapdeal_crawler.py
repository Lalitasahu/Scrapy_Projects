import scrapy


class SnapdealCrawlerSpider(scrapy.Spider):
    name = "snapdeal_crawler"
    allowed_domains = ["*"]
    # start_urls = ["http://snapdeal.com/"]
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0'
    }

    def start_requests(self):
        url =  'https://www.snapdeal.com/products/mens-footwear-sports-shoes?sort=plrty'
        yield scrapy.Request(url, callback= self.api, dont_filter=True, headers= self.headers)

    def api(self, response):
        total_pro = response.xpath('//span[@class = "category-name category-count"]//text()').get().replace('\t','').replace('\n','').replace('\r','').replace('Items','').replace('(','').replace(')','')
        page_no = 20
        main_url = response.url
        apiurl = f"https://www.snapdeal.com/acors/json/product/get/search/255/{page_no}/20?q=&sort=plrty&brandPageUrl=&keyword=&searchState=k3=true|k5=0|k6=0|k8=0&pincode=&vc=&webpageName=categoryPage&campaignId=&brandName=&isMC=false&clickSrc=unknown&showAds=true&cartId=&page=cp"
        yield scrapy.Request(apiurl, callback= self.listpage, dont_filter=True, headers=self.headers, meta={'page_no':page_no, 'main_url':main_url, 'total_pro':total_pro})

    def listpage(self, response):
        total_pro = response.meta.get('total_pro')
        page_no = response.meta.get('page_no')+20
        main_url = response.meta.get('main_url')
        # for i in range(int(total_pro)):
        # nextpage = True
        products = response.xpath('//div[@class = "col-xs-6  favDp product-tuple-listing js-tuple "]')
        for product in products:
            pro_link = product.xpath('.//a[@class = "dp-widget-link noUdLine"]/@href').get()
            name = product.xpath('.//div[@class = "product-desc-rating "]//p//text()').get()
            price = product.xpath('.//div[@class = "lfloat marR10"]//span//text()').get()
            offer = product.xpath('.//div[@class = "product-discount"]//span//text()').get()
            rating_count = product.xpath('.//p[@class ="product-rating-count"]//text()').get()
            # yield scrapy.Request(pro_link, callback=self.detailpage, dont_filter=True, headers=self.headers,
            yield {
                'main_url': main_url,
                'page_no':page_no,
                'pro_link':pro_link,
                'name':name,
                'price':price,
                'offer':offer,
                'rating_count':rating_count
            }
        if products:
            apiurl = f"https://www.snapdeal.com/acors/json/product/get/search/255/{page_no}/20?q=&sort=plrty&brandPageUrl=&keyword=&searchState=k3=true|k5=0|k6=0|k8=0&pincode=&vc=&webpageName=categoryPage&campaignId=&brandName=&isMC=false&clickSrc=unknown&showAds=true&cartId=&page=cp"
            yield scrapy.Request(apiurl, callback= self.listpage, dont_filter=True, headers=self.headers, meta={'page_no':page_no , 'main_url':main_url})

    def detailpage(self, response):
        Title = response.xpath('//h1//text()').get().strip()
        Detail_price = response.xpath('//span[@class = "pdp-final-price"]//span//text()').get()
        Highlights = response.xpath('//ul[@class ="dtls-list clear"]//li//span[@class ="h-content"]//text()').getall()
        Other_Details = response.xpath('//table[@class ="product-spec"]//tr//td//text()').getall()
        description = response.xpath('//div[@class = "spec-body"]//div//text()').get().replace('\t','')
        Teams_conditions = response.xpath('//div[@class = "detailssubbox"]//p//text()').getall()
        images_all = response.xpath('//a[@href = ""]//img/@lazysrc').getall()

        yield {
            'main_url': response.meta.get('main_url'),
            'page_no':response.meta.get('page_no'),
            'pro_link':response.meta.get('pro_link'),
            'name':response.meta.get('name'),
            'price': response.meta.get('price'),
            'offer':response.meta.get('offer'),
            'rating_count': response.meta.get('rating_count'),
            'Title':Title,
            'Detail_price':Detail_price,
            'Highlights':Highlights,
            'Other_Details':Other_Details,
            'description':description,
            'Teams_conditions':Teams_conditions,
            'images_all':images_all
        }

