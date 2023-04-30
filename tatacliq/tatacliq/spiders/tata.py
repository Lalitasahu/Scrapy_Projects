import scrapy
import mysql.connector

class TatacliqCrawlSpider(scrapy.Spider):
    # def __init__(self):
    conn = mysql.connector.connect(host="localhost", user="root", passwd="Lalita@123", db="crawling",charset="utf8", use_unicode=True)
    cursor = conn.cursor(dictionary=True)


    name = "tatacliq_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://tatacliq.com/"]
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0'}

    def start_requests(self):
        main_url = 'https://www.tatacliq.com/shirts/c-msh1116101?&icid2=regu:nav:main:mnav:m1116101:mulb:best:03:R3'
        # main_url = 'https://www.tatacliq.com/bed-sheets/c-msh2213101/?q=:relevance:category:MSH2213101:inStockFlag:true&icid2=nav:regu:homnav:m2213:mulb:best:02:R2:clp:bx:010'
        yield scrapy.Request(main_url,headers=self.headers, dont_filter=True, callback=self.apihit)

    def apihit(self, response):
        page = 0
        if response.url.split('c-')[1].split('?')[0].replace('msh','MSH'):
            catid = response.url.split('c-')[1].split('?')[0].replace('msh','MSH')
        elif response.url.split(':')[4]:
            catid = response.url.split(':')[4]
        elif response.url.split('category:')[1].split(':')[0]:
             catid = response.url.split('category:')[1].split(':')[0]

        url = f'https://searchbff.tatacliq.com/products/mpl/search?searchText=:relevance:category:{catid}:inStockFlag:true&isKeywordRedirect=false&isKeywordRedirectEnabled=false&channel=WEB&isMDE=true&isTextSearch=false&isFilter=false&qc=false&test=invizbff.qpsv3-inviz.bs&page={page}&mcvid=66134890374905082130978610156833886508&customerId=&isSuggested=false&isPwa=true&pageSize=40&typeID=all'
        # print(url)
        yield scrapy.Request(url, headers=self.headers, dont_filter=True,callback=self.listpage, meta={'page':page, 'catid':catid})
    
    def listpage(self, response):
        js = response.json()
        catid = response.meta.get('catid')
        page = response.meta['page']+1
        products = js.get('searchresult')
        if products :
            for product in products:
                ussid = product['ussid']
                brandname =product.get('brandname')
                product_url = 'https://www.tatacliq.com'+product.get('webURL')
                productId = product.get('productId')
                productname = product.get('productname')
                imageURL = product.get('imageURL')
                sale_price = product.get('price').get('sellingPrice').get('formattedValue')
                mrp = product.get('price').get('mrpPrice').get('formattedValue')
                
                yield {
                    'ussid':ussid,
                    'brandname':brandname,
                    'product_url':product_url,
                    'productId':productId,
                    'productname':productname,
                    'imageURL':imageURL,
                    'sale_price':sale_price,
                    'mrp':mrp
                    
                }
                query = "insert into tata_cliq_list(user_id,brand,product_url,product_id,product_name,img_url,sale_price,mrp) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                values = [ussid,brandname,product_url,productId,productname,imageURL,sale_price,mrp]
                self.cursor.execute(query,values)
                print(f"inserted...{productId}")
                # print(f"----------{c}")
                self.conn.commit()


            total = js['pagination']['totalPages']
            current = js['pagination']['currentPage']
            if total > current:
                url = f'https://searchbff.tatacliq.com/products/mpl/search?searchText=:relevance:category:{catid}:inStockFlag:true&isKeywordRedirect=false&isKeywordRedirectEnabled=false&channel=WEB&isMDE=true&isTextSearch=false&isFilter=false&qc=false&test=invizbff.qpsv3-inviz.bs&page={page}&mcvid=66134890374905082130978610156833886508&customerId=&isSuggested=false&isPwa=true&pageSize=40&typeID=all'
                yield scrapy.Request(url, headers=self.headers, dont_filter=True,callback=self.listpage, meta= { 'page':page, 'catid':catid})