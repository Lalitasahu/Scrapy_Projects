import scrapy
from scrapy.http import JsonRequest




params = {
    'aliasURL': 'new/bags/br/f30e74',
    's': 'c',
    'c': 'Bags',
    'n': 'n',
    'navsrc': 'subnew',
    'pageNum': '2',
}

class RevolveCrawlSpider(scrapy.Spider):
    name = "revolve_crawl"
    allowed_domains = ["revolve.com"]
    # start_urls = ["http://revolve.com/"]
    cookies = {
    'viewNumR1': '100',
    'isPopupEnabledR1': 'true',
    'pocketViewR1': 'front',
    'currency': 'USD',
    'currencyOverride': 'INR',
    'userLanguagePref': 'en',
    'altexp': '%7B%22896%22%3A0%2C%221537%22%3A1%2C%221668%22%3A1%2C%221031%22%3A1%2C%221671%22%3A1%2C%221674%22%3A0%2C%221677%22%3A0%2C%221424%22%3A1%2C%221680%22%3A0%2C%221298%22%3A0%2C%221555%22%3A0%2C%221683%22%3A1%2C%221686%22%3A1%2C%221304%22%3A0%2C%221433%22%3A0%2C%221689%22%3A0%2C%221179%22%3A1%2C%221439%22%3A0%2C%221695%22%3A0%2C%221570%22%3A1%2C%221442%22%3A1%2C%221698%22%3A1%2C%22677%22%3A1%2C%221445%22%3A1%2C%221701%22%3A1%2C%221576%22%3A1%2C%221448%22%3A1%2C%221704%22%3A0%2C%221194%22%3A0%2C%221579%22%3A0%2C%221197%22%3A1%2C%221582%22%3A0%2C%221585%22%3A0%2C%221457%22%3A1%2C%221591%22%3A0%2C%22951%22%3A0%2C%221463%22%3A1%2C%221081%22%3A1%2C%221340%22%3A1%2C%221597%22%3A1%2C%221469%22%3A1%2C%221086%22%3A0%2C%221600%22%3A0%2C%221346%22%3A1%2C%221475%22%3A0%2C%221349%22%3A1%2C%221606%22%3A0%2C%221609%22%3A0%2C%221355%22%3A1%2C%221484%22%3A1%2C%221615%22%3A1%2C%221232%22%3A0%2C%221361%22%3A1%2C%221618%22%3A1%2C%221235%22%3A1%2C%221621%22%3A0%2C%221493%22%3A0%2C%221624%22%3A1%2C%221496%22%3A0%2C%221627%22%3A0%2C%221630%22%3A1%2C%221636%22%3A1%2C%221508%22%3A1%2C%221382%22%3A0%2C%221639%22%3A1%2C%221642%22%3A0%2C%221514%22%3A0%2C%22876%22%3A1%2C%221645%22%3A1%2C%221262%22%3A0%2C%221648%22%3A1%2C%22752%22%3A1%2C%221651%22%3A0%2C%221268%22%3A1%2C%221654%22%3A0%2C%221526%22%3A1%2C%221656%22%3A0%2C%221016%22%3A0%2C%221403%22%3A0%2C%221659%22%3A0%2C%221662%22%3A1%2C%221535%22%3A1%7D',
    'originalsource': 'https%3A%2F%2Fwww.google.com%2F',
    'remarketing': 'TypeB',
    'userClosedNtfDialogCount': '1',
    'userLastSeenNtfDialogDate': '2022-10-26',
    'userSeenNtfDialogDate': '2023-02-12',
    '_ga_9Z139SMQQ8': 'GS1.1.1676265945.18.1.1676266220.20.0.0',
    '_ga': 'GA1.2.1465283199.1666850476',
    'requestBrowserIdMapping': '1',
    'visitor-cookie1': 'true',
    '_tt_enable_cookie': '1',
    '_ttp': 'c5f16c42-432b-4aad-bdce-7c1125b24fcb',
    '_pxvid': 'de4255e6-55bc-11ed-97ef-6f775a594d6d',
    '__rtbh.lid': '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22w0rOVZsDVBrfOYpTMjqn%22%7D',
    '_px_f394gi7Fvmc43dfg_user_id': 'YzVkNGJlYTAtNTViYy0xMWVkLTkwMzItMjEzOWFlZTc0ODkz',
    'cjConsent': 'MHxOfDB8Tnww',
    'cjUser': '146dda99-c4fa-4138-873c-87c7a29264cc',
    'lastRskxRun': '1676266185561',
    'rskxRunCookie': '0',
    'rCookie': 'lwa0twi1hu21xg0xrc7e8l9qnqlhc',
    'SSP_AB_StyleFinder_20160425': 'Test',
    'SSP_AB_876878223': 'test1',
    '_sp_id.9084': 'd4e040c9-d4a6-418d-bae1-e3f67328b435.1666850497.13.1676266185.1676111315.fb26f081-ed39-4182-85da-3b6f34c9ae6b',
    'name.cookie.last.visited.product': 'NOCH-WD38',
    '__rtbh.uid': '%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D',
    'JSESSIONID2': 'B75B8F7EBA88A0839E24FD6B79F3E83F.tc-chuck_tomcat4',
    'sortByR2': 'featured',
    'bb_PageURL': '%2Fcontent%2Fproducts%2FlazyLoadProductsRevolve%3Furl%3Dhttps%253A%252F%252Fwww.revolve.com%252Fr%252FBrands.jsp%253FaliasURL%253Dnew%252Fbags%252Fbr%252Ff30e74%2526navsrc%253Dsubnew%2526pageNum%253D1%2526%2526n%253Dn%2526s%253Dc%2526c%253DBags%26sortBy%3Dfeatured%26productsPerRow%3D4%26preLoadCategory%3D%26preLoadDesigner%3D%26lazyLang%3Den%26lazyCountryCode%3DIN%26lazyCurrency%3DINR%26_%3D1676266180802',
    'fontsLoaded': '1',
    'ntfPopupSuppressionCount': '8',
    '--btsc--': 'true',
    'pxcts': '307bae69-a9f7-11ed-b4ff-4670644b6f4c',
    '_gcl_au': '1.1.973293430.1676111237',
    '_fbp': 'fb.1.1676111239927.1621004192',
    '_taggstar_vid': 'b0a9e89b-a9f6-11ed-9989-79207a0eb812',
    'pageSize': '100',
    '_px2': 'eyJ1IjoiNmE0YmQxYjAtYWI1Zi0xMWVkLTgzOGItYTc5YTM2Y2RjOGI3IiwidiI6ImRlNDI1NWU2LTU1YmMtMTFlZC05N2VmLTZmNzc1YTU5NGQ2ZCIsInQiOjE2NzYyNjY3MTU0NDMsImgiOiIxNDE1YjlmNDdmYTIwNzk4YTBiZGFiYTBkYTg2OWJjOTU4NjQzYjFhOGY0MTI2YzI5ZTg5YjkxYTlhZDUxZWNmIn0=',
    '__cf_bm': 'gjUFX_UnBXNXANkiB5uJ9ou17kr57Su3ReMZVGjWFk8-1676266177-0-ATBJxPs/C45w2Yz3USMZ8Oksb4OYhE+Y5UIy96w3B8q9T+z0LufbTN5Gcn2n36uC8muRjwfBZ6YcE5Wtq/ufNrs=',
    'requestSessionID': '4817498299',
    '_gid': 'GA1.2.1293377046.1676265949',
    '_sp_ses.9084': '*',
    '_taggstar_ses': 'e3046ada-ab5e-11ed-9e68-155693c352ac',
    '_pxff_cc': 'U2FtZVNpdGU9TGF4Ow==',
    '_gat': '1',
    '_uetsid': 'e091c460ab5e11ed99c817a5cec43bc4',
    '_uetvid': 'c623f41055bc11edb3a05d0c5c762448',
    'browserID': 'aXxTbOH1r97dqKALQ5vrNqCtrYQMIZ',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.revolve.com/new/bags/br/f30e74/?navsrc=subnew&pageNum=2',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        # 'Cookie': 'viewNumR1=100; isPopupEnabledR1=true; pocketViewR1=front; currency=USD; currencyOverride=INR; userLanguagePref=en; altexp=%7B%22896%22%3A0%2C%221537%22%3A1%2C%221668%22%3A1%2C%221031%22%3A1%2C%221671%22%3A1%2C%221674%22%3A0%2C%221677%22%3A0%2C%221424%22%3A1%2C%221680%22%3A0%2C%221298%22%3A0%2C%221555%22%3A0%2C%221683%22%3A1%2C%221686%22%3A1%2C%221304%22%3A0%2C%221433%22%3A0%2C%221689%22%3A0%2C%221179%22%3A1%2C%221439%22%3A0%2C%221695%22%3A0%2C%221570%22%3A1%2C%221442%22%3A1%2C%221698%22%3A1%2C%22677%22%3A1%2C%221445%22%3A1%2C%221701%22%3A1%2C%221576%22%3A1%2C%221448%22%3A1%2C%221704%22%3A0%2C%221194%22%3A0%2C%221579%22%3A0%2C%221197%22%3A1%2C%221582%22%3A0%2C%221585%22%3A0%2C%221457%22%3A1%2C%221591%22%3A0%2C%22951%22%3A0%2C%221463%22%3A1%2C%221081%22%3A1%2C%221340%22%3A1%2C%221597%22%3A1%2C%221469%22%3A1%2C%221086%22%3A0%2C%221600%22%3A0%2C%221346%22%3A1%2C%221475%22%3A0%2C%221349%22%3A1%2C%221606%22%3A0%2C%221609%22%3A0%2C%221355%22%3A1%2C%221484%22%3A1%2C%221615%22%3A1%2C%221232%22%3A0%2C%221361%22%3A1%2C%221618%22%3A1%2C%221235%22%3A1%2C%221621%22%3A0%2C%221493%22%3A0%2C%221624%22%3A1%2C%221496%22%3A0%2C%221627%22%3A0%2C%221630%22%3A1%2C%221636%22%3A1%2C%221508%22%3A1%2C%221382%22%3A0%2C%221639%22%3A1%2C%221642%22%3A0%2C%221514%22%3A0%2C%22876%22%3A1%2C%221645%22%3A1%2C%221262%22%3A0%2C%221648%22%3A1%2C%22752%22%3A1%2C%221651%22%3A0%2C%221268%22%3A1%2C%221654%22%3A0%2C%221526%22%3A1%2C%221656%22%3A0%2C%221016%22%3A0%2C%221403%22%3A0%2C%221659%22%3A0%2C%221662%22%3A1%2C%221535%22%3A1%7D; originalsource=https%3A%2F%2Fwww.google.com%2F; remarketing=TypeB; userClosedNtfDialogCount=1; userLastSeenNtfDialogDate=2022-10-26; userSeenNtfDialogDate=2023-02-12; _ga_9Z139SMQQ8=GS1.1.1676265945.18.1.1676266220.20.0.0; _ga=GA1.2.1465283199.1666850476; requestBrowserIdMapping=1; visitor-cookie1=true; _tt_enable_cookie=1; _ttp=c5f16c42-432b-4aad-bdce-7c1125b24fcb; _pxvid=de4255e6-55bc-11ed-97ef-6f775a594d6d; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22w0rOVZsDVBrfOYpTMjqn%22%7D; _px_f394gi7Fvmc43dfg_user_id=YzVkNGJlYTAtNTViYy0xMWVkLTkwMzItMjEzOWFlZTc0ODkz; cjConsent=MHxOfDB8Tnww; cjUser=146dda99-c4fa-4138-873c-87c7a29264cc; lastRskxRun=1676266185561; rskxRunCookie=0; rCookie=lwa0twi1hu21xg0xrc7e8l9qnqlhc; SSP_AB_StyleFinder_20160425=Test; SSP_AB_876878223=test1; _sp_id.9084=d4e040c9-d4a6-418d-bae1-e3f67328b435.1666850497.13.1676266185.1676111315.fb26f081-ed39-4182-85da-3b6f34c9ae6b; name.cookie.last.visited.product=NOCH-WD38; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; JSESSIONID2=B75B8F7EBA88A0839E24FD6B79F3E83F.tc-chuck_tomcat4; sortByR2=featured; bb_PageURL=%2Fcontent%2Fproducts%2FlazyLoadProductsRevolve%3Furl%3Dhttps%253A%252F%252Fwww.revolve.com%252Fr%252FBrands.jsp%253FaliasURL%253Dnew%252Fbags%252Fbr%252Ff30e74%2526navsrc%253Dsubnew%2526pageNum%253D1%2526%2526n%253Dn%2526s%253Dc%2526c%253DBags%26sortBy%3Dfeatured%26productsPerRow%3D4%26preLoadCategory%3D%26preLoadDesigner%3D%26lazyLang%3Den%26lazyCountryCode%3DIN%26lazyCurrency%3DINR%26_%3D1676266180802; fontsLoaded=1; ntfPopupSuppressionCount=8; --btsc--=true; pxcts=307bae69-a9f7-11ed-b4ff-4670644b6f4c; _gcl_au=1.1.973293430.1676111237; _fbp=fb.1.1676111239927.1621004192; _taggstar_vid=b0a9e89b-a9f6-11ed-9989-79207a0eb812; pageSize=100; _px2=eyJ1IjoiNmE0YmQxYjAtYWI1Zi0xMWVkLTgzOGItYTc5YTM2Y2RjOGI3IiwidiI6ImRlNDI1NWU2LTU1YmMtMTFlZC05N2VmLTZmNzc1YTU5NGQ2ZCIsInQiOjE2NzYyNjY3MTU0NDMsImgiOiIxNDE1YjlmNDdmYTIwNzk4YTBiZGFiYTBkYTg2OWJjOTU4NjQzYjFhOGY0MTI2YzI5ZTg5YjkxYTlhZDUxZWNmIn0=; __cf_bm=gjUFX_UnBXNXANkiB5uJ9ou17kr57Su3ReMZVGjWFk8-1676266177-0-ATBJxPs/C45w2Yz3USMZ8Oksb4OYhE+Y5UIy96w3B8q9T+z0LufbTN5Gcn2n36uC8muRjwfBZ6YcE5Wtq/ufNrs=; requestSessionID=4817498299; _gid=GA1.2.1293377046.1676265949; _sp_ses.9084=*; _taggstar_ses=e3046ada-ab5e-11ed-9e68-155693c352ac; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _gat=1; _uetsid=e091c460ab5e11ed99c817a5cec43bc4; _uetvid=c623f41055bc11edb3a05d0c5c762448; browserID=aXxTbOH1r97dqKALQ5vrNqCtrYQMIZ',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    def start_requests(self):
        # response = requests.get('https://www.revolve.com/r/BrandsContent.jsp', params=params, cookies=cookies, headers=headers)
        # m_url = 'https://www.revolve.com/new/bags/br/f30e74/?navsrc=subnew&pageNum=1'
        api = 'https://www.revolve.com/r/BrandsContent.jsp?aliasURL=new/bags/br/f30e74&s=c&c=Bags&n=n&navsrc=subnew&pageNum=2'
        # yield scrapy.Request(url= api,cookies=self.cookies, headers=self.headers,callback=self.listpage)
        yield JsonRequest(api, callback = self.listpage, headers=self.headers,cookies = self.cookies)

    def listpage(self, response):
        products = response.xpath('//div[@class = "plp_image_wrap u-center image-hover"]')
        for product in products:
            name = product.xpath('.//div[@class = "product-name u-margin-t--lg js-plp-name"]//text()').get()
            
            yield{
                'name':name
            }