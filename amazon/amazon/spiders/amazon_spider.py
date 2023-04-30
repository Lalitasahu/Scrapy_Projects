import scrapy


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["*"]
    # start_urls = ["http://amazon.com/"]
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0'}

    def start_requests(self):
        url = 'https://www.amazon.com/s?i=specialty-aps&bbn=16225005011&rh=n%3A%2116225005011%2Cn%3A196601011&ref=nav_em__nav_desktop_sa_intl_baby_toddler_toys_0_2_10_4'
        yield scrapy.Request(url,callback=self.listpage, headers=self.headers,dont_filter=True)
    
    def listpage(self, response):
        