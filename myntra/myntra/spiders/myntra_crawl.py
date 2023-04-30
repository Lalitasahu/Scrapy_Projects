import scrapy
import json
import re

class MyntraCrawlSpider(scrapy.Spider):
    name = "myntra_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://myntra.com/"]
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0'}

    def start_requests(self):
        page = 1
        url = f'https://www.myntra.com/laundry-bag?p=1'
        yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True, meta={'page':page})

    def listpage(self, response):

        page = response.meta['page']+1
        catID = response.url.split('/')[-1].split('?')[0]
        links=re.findall('"landingPageUrl":"(.*?)"',response.text.replace('u002F','').replace('\\','/'))
        name= re.findall('"product":"(.*?)",',response.text)
        for i,nm in zip(links,name):
            link='https://www.myntra.com/'+i
            yield scrapy.Request(link, callback=self.detailpage, headers=self.headers, dont_filter=True, meta={'page':page, 'catID':catID})
            # yield{
            #     'link':link,
            #     'name':nm
            # }
        nextpage = response.xpath('//link[@rel="next"]/@href')
        if nextpage:
            url = f'https://www.myntra.com/{catID}?p={page}'
            yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True, meta={'page':page, 'catID':catID})

    def detailpage(self, response):
        id=re.search('"id":(.*?),',response.text).group(1)
        brand=re.search('"brand":"(.*?)"',response.text).group(1)
        name=re.search('"name":"(.*?)"',response.text).group(1)
        images='||'.join(re.findall('{"src":"(.*?)",',response.text.replace('u002F','').replace('\\','/').replace('($height)','720').replace('($qualityPercentage)','90').replace('($width)','540')))
        sp = json.loads(re.search('articleAttributes":(.*?),"systemAttr',response.text).group(1))
        specifications = {}
        for i in sp:
            if sp[i] != 'NA':
                specifications[i] = sp[i]
        yield {
            'id':id,
            'brand':brand,
            'name':name,
            'images':images,
            'specifications':specifications
        }
         