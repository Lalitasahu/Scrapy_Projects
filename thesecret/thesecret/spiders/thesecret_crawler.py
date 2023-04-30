import scrapy
import mysql.connector

class ThesecretCrawlerSpider(scrapy.Spider):
    conn = mysql.connector.connect(host="localhost", user="root", passwd="Lalita@123", db="crawling",charset="utf8", use_unicode=True)
    cursor = conn.cursor(dictionary=True)

    name = "thesecret_crawler"
    allowed_domains = ["thesecret.tv"]
    # start_urls = ["http://thesecret.tv/"]
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/112.0'
    }
    
    def start_requests(self):
        page = 1
        url = f'https://www.thesecret.tv/the-secret-stories/page/{page}/'
        yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True,meta={'page':page,'url':url})
    
    def listpage(self, response):
        url = response.meta.get('url')
        page = response.meta['page']+1
        blogs =  response.xpath('//div[@class="post-story"]')
        for blog in blogs:
            post_data = blog.xpath('.//div[@class="date"]//text()').get().strip()
            blog_link = blog.xpath('.//a[@class = "button-main normal-button-color"]/@href').get()
            
            yield scrapy.Request(blog_link, callback=self.detailpage, headers=self.headers, dont_filter=True,
                                 meta={'post_data':post_data,
                                       'blog_link':blog_link,
                                       'url':url})
            # yield {
            #     'post_data':post_data,
            #     'blog_link':blog_link
            # }

        total = int(response.xpath('//a[@class="page-numbers"]//text()').getall()[-1])
        # total = 10
        if total > page:
            url = f'https://www.thesecret.tv/the-secret-stories/page/{page}/'
            yield scrapy.Request(url, callback=self.listpage, headers=self.headers, dont_filter=True,meta={'page':page,'url':url})

            
        
    def detailpage(self, response):
        landingUrl = response.meta.get('url')
        blog_link = response.meta.get('blog_link')
        post_data = response.meta.get('post_data')
        Title = response.xpath('//h2//text()').get()
        submit_by = response.xpath('//h4//text()').get()
        Location = response.xpath('//span[@class = "author_location"]//text()').get()
        Author_bio = response.xpath('//p[@class="author_bio"]//text()').get()
        description = ''.join(response.xpath('//div[@class="mstory-content"]//text()').getall()).strip()
        category = '||'.join(response.xpath('//div[@class="mstory-tags"]//text()').getall()).strip()

        yield {
                'landingUrl':landingUrl,
                'blog_link':blog_link,
                'post_data':post_data,
                'Title':Title,
                'submit_by':submit_by,
                'Location':Location,
                'Author_bio':Author_bio,
                'description':description,
                'category':category,

        }
        query = "insert into Thesecret(landingUrl,blog_link,post_data,Title,submit_by,Location,Author_bio,description,category) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = [landingUrl,blog_link,post_data,Title,submit_by,Location,Author_bio,description,category]
        self.cursor.execute(query,values)
        self.conn.commit()
        # print(values)

