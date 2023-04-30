import scrapy


class ClarkurlSpider(scrapy.Spider):
    name = "clarkUrl"
    allowed_domains = ["clarksusa.com"]
    # start_urls = ["http://clarksusa.com/"]

    def start_requests(self):
        url = 'https://www.clarksusa.com/'
        yield scrapy.Request(url,callback=self.cat_url)

    def cat_url(self, response):
        urls =  response.xpath('//li[@class = "new-header__flyout-menu-column-list-item"]//a/@href')
        yield {
            'urls':urls
        }