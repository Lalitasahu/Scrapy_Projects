import scrapy
import math
from scrapy.http import JsonRequest


class VijaysalesCrawlSpider(scrapy.Spider):
    name = "vijaysales_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://vijaysales.com/"]


    cookies = {
    'AWSALB': 'oiRQt3yCTvPZCu1lSazGktOP8gMV0QT1R6Nd1Vhe/NuRMG3K99dpAr7OXY7R8WuXxHRMaAfJPEIHr9v4hvGYUcV4rfD+IbUlA44qymyoFc+r26n+Wj1WYGhyVy4Y',
    'AWSALBCORS': 'oiRQt3yCTvPZCu1lSazGktOP8gMV0QT1R6Nd1Vhe/NuRMG3K99dpAr7OXY7R8WuXxHRMaAfJPEIHr9v4hvGYUcV4rfD+IbUlA44qymyoFc+r26n+Wj1WYGhyVy4Y',
    '_gcl_aw': 'GCL.1680347514.CjwKCAjwrJ-hBhB7EiwAuyBVXZryG8Xd3DRDHJEjWpWXK7p_xhkpc9abKAQldwG8qw_f6Yi3YJFugxoC2lYQAvD_BwE',
    '_gcl_au': '1.1.1443720213.1680347514',
    'unbxd.userId': 'uid-1680347514324-84114',
    'mfKey': '176l6f1.1680347514397',
    'mf_visitid': '18hhv04.1680347514397',
    'mf_utms': '%7B%22utm_source%22%3A%22google_search%22%2C%22utm_medium%22%3A%22cpc%22%2C%22utm_campaign%22%3A%22pt-google-vijaysales-na-gs-purchase-brand-na-in-all-24-Oct-2020%22%2C%22utm_term%22%3A%22vijay%2520sales%22%2C%22utm_content%22%3A%22529936422896%22%2C%22adgroup%22%3A%22112819201595%22%2C%22matchtype%22%3A%22e%22%2C%22devicemodel%22%3A%22%22%2C%22device%22%3A%22c%22%2C%22network%22%3A%22g%22%2C%22placement%22%3A%22%22%2C%22gclid%22%3A%22CjwKCAjwrJ-hBhB7EiwAuyBVXZryG8Xd3DRDHJEjWpWXK7p_xhkpc9abKAQldwG8qw_f6Yi3YJFugxoC2lYQAvD_BwE%22%7D',
    '_nv_uid': '38961852.1680347516.67172ed1-e60c-405a-a4ba-2983708ed272.1680757697.1680845374.10.0',
    '_nv_utm': '38961852.1680347516.10.1.dXRtc3JjPWdvb2dsZXx1dG1jY249cHQtZ29vZ2xlLXZpamF5c2FsZXMtbmEtZ3MtcHVyY2hhc2UtYnJhbmQtbmEtaW4tYWxsLTI0LU9jdC0yMDIwfHV0bWNtZD1jcGN8dXRtY3RyPXZpamF5K3NhbGVzfHV0bWNjdD01Mjk5MzY0MjI4OTZ8Z2NsaWQ9Q2p3S0NBandySi1oQmhCN0Vpd0F1eUJWWFpyeUc4WGQzRFJESEpFaldwV1hLN3BfeGhrcGM5YWJLQVFsZHdHOHF3X2Y2WWkzWUpGdWd4b0MybFlRQXZEX0J3RQ==',
    '_nv_did': '38961852.1680347516.2409:4050:d98:c2e5:2d2b:22d9:940c:95aewd15k',
    '_nv_hit': '38961852.1680845629.cHZpZXc9NA==',
    '_ga': 'GA1.2.741139552.1680347515',
    '_gac_UA-26907894-4': '1.1680347515.CjwKCAjwrJ-hBhB7EiwAuyBVXZryG8Xd3DRDHJEjWpWXK7p_xhkpc9abKAQldwG8qw_f6Yi3YJFugxoC2lYQAvD_BwE',
    '_gac_UA-26907894-5': '1.1680347518.CjwKCAjwrJ-hBhB7EiwAuyBVXZryG8Xd3DRDHJEjWpWXK7p_xhkpc9abKAQldwG8qw_f6Yi3YJFugxoC2lYQAvD_BwE',
    '_clck': '15ne5j3|1|fak|0',
    '_fbp': 'fb.1.1680347516239.378660695',
    '_nv_push_times': '1',
    '_clsk': '11i84hk|1680845630606|4|1|d.clarity.ms/collect',
    'ASP.NET_SessionId': '2crjokhihsm4heiicia5kybj',
    '__AntiXsrfToken': 'a270ff73b9c744ae95ae5fd88abbcfcb',
    'Mypreurl': 'https://www.vijaysales.com/home-appliances/air-conditioners',
    'unbxd.visit': 'repeat',
    'unbxd.visitId': 'visitId-1680845374343-95640',
    '_gid': 'GA1.2.1446334716.1680845374',
    '_nv_sess': '38961852.1680845374.jIrf053WjghFuBCUcV9AuWrHuP75m7jXWDKuGMZsX7I3is3Ok7',
    'mycity': 'cityId=1&city=Mumbai&IsPreOrder=false&isDefault=true',
    'UPinT': 'pin=400001',
    'UPinCode': 'pinC=400001',
    '_gat_UA-26907894-4': '1',
    '_gat_UA-26907894-5': '1',
    '_gat_NV_PushNoitfication': '1',
    '_nv_push_neg': '1',
    '_dc_gtm_UA-26907894-5': '1',
    '_uetsid': '2e3dd810d50511ed8a76a5357e34b930',
    '_uetvid': '02bbac50d07e11ed9251673bc01fe8f8',
    }


    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json; charset=utf-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    # 'Referer': 'https://www.vijaysales.com/home-appliances/air-conditioners',
    # 'Cookie': 'AWSALB=1/EF96FeKd+69PBAqiznfMXlHocSv3UdSNlltxUoI6GexqPRic74CKEN9m0+GUDTIRSJLkhg+ou2PCQC1kq6gZ2i97Loc+7lVT2dRjBlf9w4MW+IV9Ke4iQynkaZ; AWSALBCORS=1/EF96FeKd+69PBAqiznfMXlHocSv3UdSNlltxUoI6GexqPRic74CKEN9m0+GUDTIRSJLkhg+ou2PCQC1kq6gZ2i97Loc+7lVT2dRjBlf9w4MW+IV9Ke4iQynkaZ; ASP.NET_SessionId=qjffdxang41ocrd0ekf5fhqk; __AntiXsrfToken=cc93799524f543ef99f05a7d451b83ea; Mypreurl=https://www.vijaysales.com/tv-and-entertainment/televisions; PN=google_search; _gcl_aw=GCL.1680347514.CjwKCAjwrJ-hBhB7EiwAuyBVXZryG8Xd3DRDHJEjWpWXK7p_xhkpc9abKAQldwG8qw_f6Yi3YJFugxoC2lYQAvD_BwE; _gcl_au=1.1.1443720213.1680347514; unbxd.userId=uid-1680347514324-84114; unbxd.visit=first_time; unbxd.visitId=visitId-1680347514328-33079; mfKey=176l6f1.1680347514397; mf_visitid=18hhv04.1680347514397; mf_utms=%7B%22utm_source%22%3A%22google_search%22%2C%22utm_medium%22%3A%22cpc%22%2C%22utm_campaign%22%3A%22pt-google-vijaysales-na-gs-purchase-brand-na-in-all-24-Oct-2020%22%2C%22utm_term%22%3A%22vijay%2520sales%22%2C%22utm_content%22%3A%22529936422896%22%2C%22adgroup%22%3A%22112819201595%22%2C%22matchtype%22%3A%22e%22%2C%22devicemodel%22%3A%22%22%2C%22device%22%3A%22c%22%2C%22network%22%3A%22g%22%2C%22placement%22%3A%22%22%2C%22gclid%22%3A%22CjwKCAjwrJ-hBhB7EiwAuyBVXZryG8Xd3DRDHJEjWpWXK7p_xhkpc9abKAQldwG8qw_f6Yi3YJFugxoC2lYQAvD_BwE%22%7D; _nv_sess=38961852.1680347516.geqTLVZ9gYGvqzmmu30k3YKngt1o8Xg9mICCB7ygMfRdx5Cmyk; _nv_uid=38961852.1680347516.67172ed1-e60c-405a-a4ba-2983708ed272.1680347516.1680347516.1.0; _nv_utm=38961852.1680347516.1.1.dXRtc3JjPWdvb2dsZXx1dG1jY249cHQtZ29vZ2xlLXZpamF5c2FsZXMtbmEtZ3MtcHVyY2hhc2UtYnJhbmQtbmEtaW4tYWxsLTI0LU9jdC0yMDIwfHV0bWNtZD1jcGN8dXRtY3RyPXZpamF5K3NhbGVzfHV0bWNjdD01Mjk5MzY0MjI4OTZ8Z2NsaWQ9Q2p3S0NBandySi1oQmhCN0Vpd0F1eUJWWFpyeUc4WGQzRFJESEpFaldwV1hLN3BfeGhrcGM5YWJLQVFsZHdHOHF3X2Y2WWkzWUpGdWd4b0MybFlRQXZEX0J3RQ==; _nv_did=38961852.1680347516.2409:4050:d98:c2e5:2d2b:22d9:940c:95aewd15k; _nv_hit=38961852.1680348171.cHZpZXc9MTg=; _ga=GA1.2.741139552.1680347515; _gid=GA1.2.1867637052.1680347515; _gac_UA-26907894-4=1.1680347515.CjwKCAjwrJ-hBhB7EiwAuyBVXZryG8Xd3DRDHJEjWpWXK7p_xhkpc9abKAQldwG8qw_f6Yi3YJFugxoC2lYQAvD_BwE; _gac_UA-26907894-5=1.1680347518.CjwKCAjwrJ-hBhB7EiwAuyBVXZryG8Xd3DRDHJEjWpWXK7p_xhkpc9abKAQldwG8qw_f6Yi3YJFugxoC2lYQAvD_BwE; _clck=15ne5j3|1|fae|0; _fbp=fb.1.1680347516239.378660695; _clsk=1orgsi3|1680348172252|18|1|t.clarity.ms/collect; mycity=cityId=1&city=Mumbai&IsPreOrder=false&isDefault=true; UPinT=pin=400001; UPinCode=pinC=400001; mycityclose=true; _nv_push_neg=1; _nv_push_times=1; _gat_NV_PushNoitfication=1; _gat_UA-26907894-4=1; _gat_UA-26907894-5=1; _uetsid=02baa540d07e11ed86756d9efd3e7644; _uetvid=02bbac50d07e11ed9251673bc01fe8f8; _dc_gtm_UA-26907894-5=1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

    def start_requests(self):
        url = 'https://www.vijaysales.com/personal-care/mens-grooming/buy-trimmers-personal-care'
        yield scrapy.Request(url, headers= self.headers, callback = self.api, dont_filter=True)
    
    def api(self, response):
        page = 0
        q = response.xpath('//input[@id = "ContentPlaceHolder1_hfProductKey"]/@value').get()
        catid = response.xpath('//input[@id = "ContentPlaceHolder1_hfCategoryID"]/@value').get()
        cityid = response.xpath('//input[@id = "ContentPlaceHolder1_hfCityID"]/@value').get()
        miniprice = response.xpath('//input[@id = "ContentPlaceHolder1_hfMinAmount"]/@value').get()
        maxprice = response.xpath('//input[@id = "ContentPlaceHolder1_hfMaxAmount"]/@value').get()
        fvids = response.xpath('//input[@id = "ContentPlaceHolder1_hfFilterValueIDs"]/@value').get().replace('#','')
        actul = response.xpath('//input[@id = "ContentPlaceHolder1_hfFilterValueIDs"]/@value').get().replace('#','')
        fid = response.xpath('//input[@id = "ContentPlaceHolder1_hfFilterIDs"]/@value').get()
        apiurl = 'https://www.vijaysales.com/Handlers/getProductData.ashx'
        params = {
        'q': q,
        'catid': str(catid),
        'cityid': str(cityid),
        'fvids': str(fvids)+'#,',
        'fid': fid,
        'Index': str(page),
        'sortBy': '',
        'minPrice': str(miniprice),
        'maxPrice': str(maxprice),
        'actul': str(actul)+'#',
        'BucketID': '0',
        'isND': '1',
        'isAcc': 'False',
        'BrandID': '',
        }
        print(params)
        # for k,v in params.items():
        #     print(k,v)

        # self.params['q'] = q
        # self.params['catid'] = catid
        # self.params['cityid'] = cityid
        # self.params['miniprice'] = miniprice
        # self.params['maxprice'] = maxprice
        # self.params["Index"] = f"{page}"
        # self.params['actul'] = actul
        # self.params['fvids']  = fvids
        
        yield scrapy.FormRequest(apiurl,formdata=params,method='GET',callback=self.listpage,headers=self.headers,dont_filter=True,
            meta ={
                'page':page,
                'q':q,
                'catid':catid,
                'cityid':cityid,
                'miniprice':miniprice,
                'maxprice':maxprice,
                'fvids':fvids,
                'actul':actul,
                'fid':fid
                })
        
    def listpage(self, response):
        # print(response.text)
        page = response.meta['page']+1
        q = response.meta.get('q')
        catid = response.meta.get('catid')
        cityid = response.meta.get('cityid')
        miniprice = response.meta.get('miniprice')
        maxprice = response.meta.get('maxprice')
        fvids = response.meta.get('fvids')
        actul = response.meta.get('actul')
        fid = response.meta.get('fid')

        js = response.json()
        products = js['SearchData']
        for i in products:
            name = i['DName']
            PID = i['PID']
            pro_url = i['URLName']        
            price = i['MRPrice']
            image = i['Pimage']

            yield {
                'name':name,
                'PID':PID,
                'pro_url':pro_url,
                'price':price,
                'image':image
            }
            
        total = math.ceil(js['TotalProducts']/12)
        if total >= page :
            apiurl = 'https://www.vijaysales.com/Handlers/getProductData.ashx'

            params = {
            'q': q,
            'catid': str(catid),
            'cityid': str(cityid),
            'fvids': str(fvids),
            'fid': str(fid),
            'Index': str(page),
            'sortBy': '',
            'minPrice': str(miniprice),
            'maxPrice': str(maxprice),
            'actul': str(actul)+'#',
            'BucketID': '0',
            'isND': '1',
            'isAcc': 'False',
            'BrandID': '',
            }
            # print(params)

            # self.params['q'] = q
            # self.params['catid'] = catid
            # self.params['cityid'] = cityid
            # self.params['miniprice'] = miniprice
            # self.params['maxprice'] = maxprice
            # self.params["Index"] = f"{page}"
            # self.params['actul'] =actul
            # self.params['fvids']  = fvids
            yield scrapy.FormRequest(apiurl,formdata=params,method='GET',callback=self.listpage,headers=self.headers,dont_filter=True,
                meta ={
                'page':page+1,
                'q':q,
                'catid':catid,
                'cityid':cityid,
                'miniprice':miniprice,
                'maxprice':maxprice,
                'fvids':fvids,
                'actul':actul,
                'fid':fid
                })
            
            
        