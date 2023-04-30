import scrapy
from bs4 import BeautifulSoup as bs
import json
import re

class AlibabaCrawlSpider(scrapy.Spider):
    name = "alibaba_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://alibaba.com/"]


    cookies = {
    'ali_apache_id': '33.2.245.202.1677892998825.163003.8',
    'cookie2': 's285940091ac2b94e6c49b56d2977280',
    'intl_locale': 'en_US',
    'sc_g_cfg_f': 'sc_b_locale=en_US&sc_b_site=IN&sc_b_currency=INR',
    't': 'c455548326c47110c1a803dbb7c3e633',
    '_tb_token_': 'e7ea991b6eb8e',
    '_m_h5_tk': 'f88cc775475e7b402ff6d7d31f9950ec_1677912180929',
    '_m_h5_tk_enc': '1a772ba4b77b9b000ac012c200308a30',
    'xman_us_f': 'x_l=1',
    'acs_usuc_t': 'acs_rt=180cdfe709564ef78ea63588714651c9',
    'xman_t': '4mErrDaaeAl7eqPONFDiNU3vpws0xHeCs2IxzWyH0vse6yHtPZwj5h7MOAqA3DSMG3jO4KcN/o/iIg0xLahYhB11kaNLSM0e',
    'xman_f': 'I/p4bYU85Ngg4GvKjY2V+EmRwR/VnnNd352AS7DbCvIsorKBnY1O5UXMWYEejaK4puM5mGtKpzbBd2d6lf5ouhmAToEEbzZLXwnGBGTJjuDDLCW6stNinQ==',
    'ali_apache_track': '""',
    'ali_apache_tracktmp': '""',
    'cna': 'iYuJHLz1NQoCAWcQHg6j9okb',
    'isg': 'BD09yjf5BV48JKEy8qWMYaVvT5832nEs4bIeVv-CeBTDNl1oxynF_JTg4PJwrYnk',
    'l': 'fBLc-OmgNOKy5mBAKOfaourza779sIOYYuPzaNbMi9fP_D5p5WCdW1G2FYY9Cn6NF6S6R3-uIHU6BeYBcIbPcEkNbrsCJwMmndLHR35..',
    'tfstk': 'cAfhBVsmxhij5S7eCMOQikgkzzyAZSHeA_5d_PaJW6IBZQ5FigDZ3ueaShrbYY1..',
    'ug_se_c': 'free_1677901735153',
    'XSRF-TOKEN': '6bc9253f-2828-4f1a-8288-3408b13d2622',
    '_bl_uid': 'asl53e87t0ea1Uamp7mRlL02j1dn',
    '__wpkreporterwid_': '6d8a5820-d039-4c0d-2451-2fbd7d15cd36',
    '_csrf_token': '1677893202267',
    '_samesite_flag_': 'true',
    }

    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://dropshipping.alibaba.com/saas/filter-product.html?categoryIds=339&keyword=&scene=ALL',
    'Content-Type': 'application/json; charset=utf-8',
    'bx-v': '2.2.3',
    'EagleEye-TraceID': '5d689b73167790786637110038167e',
    'EagleEye-SessionID': '6kl0peUhts3j4d0zvrz94sRst6w4',
    'EagleEye-pAppName': 'iw0okbwm8i@a81c870bdd8167e',
    'Origin': 'https://dropshipping.alibaba.com',
    'Connection': 'keep-alive',
    # 'Cookie': 'ali_apache_id=33.2.245.202.1677892998825.163003.8; cookie2=s285940091ac2b94e6c49b56d2977280; intl_locale=en_US; sc_g_cfg_f=sc_b_locale=en_US&sc_b_site=IN&sc_b_currency=INR; t=c455548326c47110c1a803dbb7c3e633; _tb_token_=e7ea991b6eb8e; _m_h5_tk=f88cc775475e7b402ff6d7d31f9950ec_1677912180929; _m_h5_tk_enc=1a772ba4b77b9b000ac012c200308a30; xman_us_f=x_l=1; acs_usuc_t=acs_rt=180cdfe709564ef78ea63588714651c9; xman_t=4mErrDaaeAl7eqPONFDiNU3vpws0xHeCs2IxzWyH0vse6yHtPZwj5h7MOAqA3DSMG3jO4KcN/o/iIg0xLahYhB11kaNLSM0e; xman_f=I/p4bYU85Ngg4GvKjY2V+EmRwR/VnnNd352AS7DbCvIsorKBnY1O5UXMWYEejaK4puM5mGtKpzbBd2d6lf5ouhmAToEEbzZLXwnGBGTJjuDDLCW6stNinQ==; ali_apache_track=""; ali_apache_tracktmp=""; cna=iYuJHLz1NQoCAWcQHg6j9okb; isg=BD09yjf5BV48JKEy8qWMYaVvT5832nEs4bIeVv-CeBTDNl1oxynF_JTg4PJwrYnk; l=fBLc-OmgNOKy5mBAKOfaourza779sIOYYuPzaNbMi9fP_D5p5WCdW1G2FYY9Cn6NF6S6R3-uIHU6BeYBcIbPcEkNbrsCJwMmndLHR35..; tfstk=cAfhBVsmxhij5S7eCMOQikgkzzyAZSHeA_5d_PaJW6IBZQ5FigDZ3ueaShrbYY1..; ug_se_c=free_1677901735153; XSRF-TOKEN=6bc9253f-2828-4f1a-8288-3408b13d2622; _bl_uid=asl53e87t0ea1Uamp7mRlL02j1dn; __wpkreporterwid_=6d8a5820-d039-4c0d-2451-2fbd7d15cd36; _csrf_token=1677893202267; _samesite_flag_=true',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }   

    params = {
    '_tb_token_': 'e7ea991b6eb8e',
    }

    json_data = {
    'endpoint': 'pc',
    'keyword': '',
    'category': '339',
    'currency': 'INR',
    'countryCode': 'IN',
    'sortType': 'COMPREHENSIVE_DESC',
    'newProduct': None,
    'supplierType': None,
    'sellerAliId': None,
    'cluster': None,
    'companyAuthTag': None,
    'productAuthTag': None,
    'productFeature': None,
    'priceFrom': None,
    'priceTo': None,
    'scene': 'ALL',
    'sellerCompanyId': None,
    'pageNo': 1,
    'pageSize': 20,
    }

    # response = requests.post(
    # 'https://dropshipping.alibaba.com/saas/ajax/product/search/query_product',
    # params=params,
    # cookies=cookies,
    # headers=headers,
    # json=json_data,
    # )

    def start_requests(self):
        url = 'https://dropshipping.alibaba.com/saas/filter-product.html?categoryIds=339&keyword=&scene=ALL'
        yield scrapy.Request(url,callback=self.listapifun, method='POST', cookies=self.cookies, headers=self.headers, body = json.dumps(self.json_data), dont_filter=True)
    
    def listapifun(self, response):
        api = 'https://dropshipping.alibaba.com/saas/ajax/product/search/query_product?_tb_token_=e7ea991b6eb8e'
        yield scrapy.Request(api, callback=self.listpage, method='POST', cookies=self.cookies, headers=self.headers, body = json.dumps(self.json_data), dont_filter=True)

    def listpage(self, response):
        js = json.loads(response.text)
        prodcuts = js['data']['list']
        for product in prodcuts:
            product_id = product['productId'] 
            name = product['subject']
            pro_url = 'https:'+product['detail']
            image = product['image']
            dsPromotionPrice = product['dsPromotionPrice']
            dsPrice = product['dsPrice']
            freightPrice =product['freightPrice']
            qty = product['moq']
            shippingTime = product['shippingTime']
            moqUnit = product['moqUnit']
            companyName = product['companyName']
            companyProfileUrl = product['companyProfileUrl']
            
            yield scrapy.Request(pro_url, callback=self.detailapifun, method='POST', cookies=self.cookies, headers=self.headers, body = json.dumps(self.json_data), dont_filter=True,
            meta= {
                'product_id':product_id,
                'pro_url': pro_url,
                'name':name,
                'image':image,
                'dsPromotionPrice':dsPromotionPrice,
                'dsPrice':dsPrice,
                'freightPrice':freightPrice,
                'qty':qty,
                'shippingTime':shippingTime,
                'moqUnit':moqUnit,
                'companyName':companyName,
                'companyProfileUrl':companyProfileUrl
            })
        
        if js['data']['list']:
            self.json_data['pageNo']+=1
            api = 'https://dropshipping.alibaba.com/saas/ajax/product/search/query_product?_tb_token_=e7ea991b6eb8e'
            yield scrapy.Request(api, callback=self.listpage, method='POST', cookies=self.cookies, headers=self.headers, body = json.dumps(self.json_data), dont_filter=True)
         
            
    def detailapifun(self, response):
        pro_cat = response.meta.get('pro_url').split('?')[0].replace('https://www.alibaba.com/','')
        cookies = {
            '__wpkreporterwid_': 'ec86a8d4-0a26-4b62-237c-9a792463c840',
            'ali_apache_id': '33.2.245.202.1677892998825.163003.8',
            'intl_locale': 'en_US',
            'sc_g_cfg_f': 'sc_b_locale=en_US&sc_b_currency=INR&sc_b_site=IN',
            't': 'c455548326c47110c1a803dbb7c3e633',
            '_bl_uid': '1wlabeq3t0yagX6464IOfCju5syj',
            'xman_us_f': 'x_l=1',
            'xman_f': 'bByOqGAOzpHnFkjoB1QB5KkYU5x5OJn5oz9RJG66aX2VzfzDn1NRLNRD4p8S7c1UdCjagXhkMdWdldgr0XEKrAyUBLB57Tsd9ObWFNOrPNrFTcHpSwrXfw==',
            'ali_apache_track': '""',
            'cna': 'iYuJHLz1NQoCAWcQHg6j9okb',
            'isg': 'BAEBcRMOAV69zm1mTpEInUFzE0sbLnUgBR7SYmNW8ohmSiEcqH-t8V3LLCYM2Q1Y',
            'l': 'fBLc-OmgNOKy5r4iBOfanurza77OjIOYYuPzaNbMi9fP_q1v5rSPB1GFJxTJCn6NFs3283-uIHU6BeYBcuE-nxvtuEHxijHmndLHR35..',
            'tfstk': 'c585BuXvbpL2PA64ATGqTo0B8Z_fZ7a5gb6DNYjW9kCgsZRfinUNCND9t-QF9s1..',
            'ug_se_c': 'free_1678684826611',
            '__wpkreporterwid_': 'c4b0d34e-cccd-43a3-bd77-00d2879d8aeb',
            '_m_h5_tk': '53c54fff41c3a6b66e4d27dc1254fe6e_1678686618920',
            '_m_h5_tk_enc': 'a2881ea2ef639ab4408ddde02e5fd601',
            'xman_t': 'ctqNwIXyngER/fdvwNT1M922MsQJDwTkNat7gn4qT10mqz3W4trp2kX6Eu1ha3NHYQGfJB2aPrtbg7HT5h8YpC2d+f/BcToK',
            'cookie2': 'sa95e73e3fce7499943c37cbabf9df67',
            '_tb_token_': 'ee6e6ee733eed',
            'ali_apache_tracktmp': '""',
            'XSRF-TOKEN': 'e4b416dd-0c83-4187-8082-d229bc6300f6',
            'acs_usuc_t': 'acs_rt=fa621f2a370249e690e9cc3e9fbf3bbe',
            'JSESSIONID': 'E9E094C1CB9275E67781072249261A20',
            '_csrf_token': '1678679168915',
            '_samesite_flag_': 'true',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://dropshipping.alibaba.com/',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Connection': 'keep-alive',
            # 'Cookie': '__wpkreporterwid_=ec86a8d4-0a26-4b62-237c-9a792463c840; ali_apache_id=33.2.245.202.1677892998825.163003.8; intl_locale=en_US; sc_g_cfg_f=sc_b_locale=en_US&sc_b_currency=INR&sc_b_site=IN; t=c455548326c47110c1a803dbb7c3e633; _bl_uid=1wlabeq3t0yagX6464IOfCju5syj; xman_us_f=x_l=1; xman_f=bByOqGAOzpHnFkjoB1QB5KkYU5x5OJn5oz9RJG66aX2VzfzDn1NRLNRD4p8S7c1UdCjagXhkMdWdldgr0XEKrAyUBLB57Tsd9ObWFNOrPNrFTcHpSwrXfw==; ali_apache_track=""; cna=iYuJHLz1NQoCAWcQHg6j9okb; isg=BAEBcRMOAV69zm1mTpEInUFzE0sbLnUgBR7SYmNW8ohmSiEcqH-t8V3LLCYM2Q1Y; l=fBLc-OmgNOKy5r4iBOfanurza77OjIOYYuPzaNbMi9fP_q1v5rSPB1GFJxTJCn6NFs3283-uIHU6BeYBcuE-nxvtuEHxijHmndLHR35..; tfstk=c585BuXvbpL2PA64ATGqTo0B8Z_fZ7a5gb6DNYjW9kCgsZRfinUNCND9t-QF9s1..; ug_se_c=free_1678684826611; __wpkreporterwid_=c4b0d34e-cccd-43a3-bd77-00d2879d8aeb; _m_h5_tk=53c54fff41c3a6b66e4d27dc1254fe6e_1678686618920; _m_h5_tk_enc=a2881ea2ef639ab4408ddde02e5fd601; xman_t=ctqNwIXyngER/fdvwNT1M922MsQJDwTkNat7gn4qT10mqz3W4trp2kX6Eu1ha3NHYQGfJB2aPrtbg7HT5h8YpC2d+f/BcToK; cookie2=sa95e73e3fce7499943c37cbabf9df67; _tb_token_=ee6e6ee733eed; ali_apache_tracktmp=""; XSRF-TOKEN=e4b416dd-0c83-4187-8082-d229bc6300f6; acs_usuc_t=acs_rt=fa621f2a370249e690e9cc3e9fbf3bbe; JSESSIONID=E9E094C1CB9275E67781072249261A20; _csrf_token=1678679168915; _samesite_flag_=true',
        }

        # params = {
        #     'spm': 'a27ef.saas-filter-product.0.0.50d239ceG4mdIV',
        #     'ecology_token': 'alisaas',
        # }
        # api = f'https://www.alibaba.com/product-detail/{pro_cat}?spm=a27ef.saas-filter-product.0.0.50d239ceG4mdIV&ecology_token=alisaas'
        api = f'https://www.alibaba.com/{pro_cat}?=&ecology_token=alisaas'
        # url = 'https://www.alibaba.com/product-detail/HN0001-Custom-print-3D-logo-OTTO_62266219306.html'
        # response = requests.get(
        #     'https://www.alibaba.com/product-detail/HN0001-Custom-print-3D-logo-OTTO_62266219306.html',
        #     params=params,
        #     cookies=cookies,
        #     headers=headers,
        # )
        yield scrapy.Request(api, callback=self.detail, headers= headers, cookies= cookies, dont_filter=True, method="POST")
    
    def detail(self, response):
        soup = bs(response.text,'html.parser')
        # Title = re.search('"puretitle":"(.*?)",',response.text).group(1)
        Title =  response.xpath('//h1//text()').get()
        for i in soup.find_all('li','ma-ladder-price-item'):
            pr = i.find('span','pre-inquiry-price').text
            sl = i.find('span','priceVal').text
        # product_details = json.loads(re.search('"productBasicProperties":(.*?),"productCategoryId"',response.text).group(1))
        try:
            product_details = {}
            for i in json.loads(re.search('"productBasicProperties":(.*?),"productCategoryId"',response.text).group(1)):
                key = i.get('attrName')
                value = i.get('attrValue')
                product_details[key] = value
        except:
            product_details = ''

        yield {
            'Title':Title,
            'pirce':pr,
            'sale_price':sl,
            'product_details':product_details
        }
            