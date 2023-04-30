import scrapy
import json
import re
from  bs4 import BeautifulSoup as bs


class MaccosmeticsCrawlSpider(scrapy.Spider):
    name = "maccosmetics_crawl"
    allowed_domains = ["*"]
    # start_urls = ["http://maccosmetics.com/"]
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.maccosmetics.in/',
    'Content-Type': 'application/json',
    'business-unit': '2-mc-in-en-ecommv1',
    'Cache-Control': 'no-cache',
    'ClientId': 'stardust-fe-client',
    'authorizationtoken': 'Mi1tYy1pbi1lbi1lY29tbXYxOmh0dHBzOi8vd3d3Lm1hY2Nvc21ldGljcy5pbg==',
    'Origin': 'https://www.maccosmetics.in',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
    }

    json_data = {
        'query': '{\n                products(environment: {prod:true},\n                    filter: [{tags:{filter:{id:{in:["__ID__"]}},includeInnerHits:false}}],\n                    sort: [{tags:{product_display_order:ASCENDING}}]\n                ) {\n                    \n        ... product__collection \n        \n        items {\n            ... product_default ... product_productSkinType ... product_form ... product_productCoverage ... product_benefit ... product_productReview ... product_skinConcern ... product_usage ... product_productFinish ... product_usageOptions ... product_brushTypes ... product_brushShapes \n            skus {\n                total\n                items {\n                    ... product__skus_default ... product__skus_autoReplenish ... product__skus_perlgem ... product__skus_colorFamily ... product__skus_skuLargeImages ... product__skus_skuMediumImages ... product__skus_skuSmallImages ... product__skus_vtoFoundation ... product__skus_vtoMakeup \n                }\n            }\n        }\n    \n    \n                }\n            }\n\nfragment product__collection \n    on product_collection {\n        items {\n            product_id\n            skus {\n                items {\n                    inventory_status\n                    sku_id\n                }\n            }\n        }\n    }\n\n\nfragment product_default \n    on product {\n        default_category {\n            id\n            value\n        }\n        description\n        display_name\n        is_hazmat\n        meta {\n            description\n        }\n        product_badge\n        product_id\n        product_url\n        short_description\n        tags {\n            total\n            items {\n                id\n                value\n                key\n            }\n        }\n    }\n\n\nfragment product_productSkinType \n    on product {\n        skin {\n            type {\n                key\n                value\n            }\n        }\n    }\n\n\nfragment product_form \n    on product {\n        form {\n            key\n            value\n        }\n    }\n\n\nfragment product_productCoverage \n    on product {\n        coverage {\n            key\n            value\n        }\n    }\n\n\nfragment product_benefit \n    on product {\n        benefit {\n            benefits {\n                key\n                value\n            }\n        }\n    }\n\n\nfragment product_productReview \n    on product {\n        reviews {\n            average_rating\n            number_of_reviews\n        }\n    }\n\n\nfragment product_skinConcern \n    on product {\n        skin {\n            concern {\n                key\n                value\n            }\n        }\n    }\n\n\nfragment product_usage \n    on product {\n        usage {\n            content\n            label\n            type\n        }\n    }\n\n\nfragment product_productFinish \n    on product {\n        finish {\n            key\n            value\n        }\n    }\n\n\nfragment product_usageOptions \n    on product {\n        usage_options {\n            key\n            value\n        }\n    }\n\n\nfragment product_brushTypes \n    on product {\n        brush {\n            types {\n                key\n                value\n            }\n        }\n    }\n\n\nfragment product_brushShapes \n    on product {\n        brush {\n            shapes {\n                key\n                value\n            }\n        }\n    }\n\n\nfragment product__skus_default \n    on product__skus {\n        is_default_sku\n        is_discountable\n        is_giftwrap\n        is_under_weight_hazmat\n        iln_listing\n        iln_version_number\n        inventory_status\n        material_code\n        prices {\n            currency\n            is_discounted\n            include_tax {\n                price\n                original_price\n                price_per_unit\n                price_formatted\n                original_price_formatted\n                price_per_unit_formatted\n            }\n        }\n        sizes {\n            value\n            key\n        }\n        shades {\n            name\n            description\n            hex_val\n        }\n        sku_id\n        sku_badge\n        unit_size_formatted\n        upc\n    }\n\n\nfragment product__skus_autoReplenish \n    on product__skus {\n        is_replenishable\n    }\n\n\nfragment product__skus_perlgem \n    on product__skus {\n        perlgem {\n            SKU_BASE_ID\n        }\n    }\n\n\nfragment product__skus_colorFamily \n    on product__skus {\n        color_family {\n            key\n            value\n        }\n    }\n\n\nfragment product__skus_skuLargeImages \n    on product__skus {\n        media {\n            large {\n                src\n                alt\n                height\n                width\n            }\n        }\n    }\n\n\nfragment product__skus_skuMediumImages \n    on product__skus {\n        media {\n            medium {\n                src\n                alt\n                height\n                width\n            }\n        }\n    }\n\n\nfragment product__skus_skuSmallImages \n    on product__skus {\n        media {\n            small {\n                src\n                alt\n                height\n                width\n            }\n        }\n    }\n\n\nfragment product__skus_vtoFoundation \n    on product__skus {\n        vto {\n            is_foundation_experience\n        }\n    }\n\n\nfragment product__skus_vtoMakeup \n    on product__skus {\n        vto {\n            is_color_experience\n        }\n    }\n',
        'variables': {},
    }



    def start_requests(self):
        url = 'https://www.maccosmetics.in/products/13849/products/makeup/face/compactpowder'
        # url = 'https://www.maccosmetics.in/products/13854/Products/Makeup/Lips/Lipstick'
        yield scrapy.Request(url, headers=self.headers, dont_filter=True, callback=self.api)
    
    def api(self, response):
        id = re.search('\d+',response.url).group(0)
        apiurl = 'https://emea.sdapi.io/stardust-prodcat-product-v3/graphql/core/v1/extension/v1'
        # print(apiurl,response)
        yield scrapy.Request(apiurl, headers=self.headers, body=json.dumps(self.json_data).replace('__ID__',id), method='POST', dont_filter= True, callback=self.listpage)

    def listpage(self, response):
        js = response.json()
        products = js['data']['products']['items']
        for product in products:
            product_id = product['product_id']
            display_name = product['display_name']
            product_url = 'https://www.maccosmetics.in'+product['product_url']
            short_description = product['short_description']
            description = product['description']
            average_rating = product['reviews']['average_rating']
            number_of_reviews = product['reviews']['number_of_reviews']
            # benefit = product['benefit']['benefits']
            try:
                usage = bs(product['usage'][0]['content'],'html.parser').text
            except:
                usage = ''

            yield scrapy.Request(product_url, headers=self.headers, callback=self.detail, dont_filter=True, 

            meta= {
                'product_id':product_id,
                'product_url':product_url,
                'display_name':display_name,
                'short_description':short_description,
                'description':description,
                'average_rating':average_rating,
                'number_of_reviews':number_of_reviews,
                # 'benefit':benefit,
                'usage':usage
            })
    
    def detail(self, response):
        Title = response.xpath('//div[@class = "product-full__title"]//text()').get()
        description = response.xpath('//div[@class = "product-overview--description-wrapper js-desc-wrapper body-text"]//text()').get()
        price = response.xpath('//div[@class = "product-full__price-details"]//div[@class = "product-full__price"]//text()')[1].get()
        qty = response.xpath('//div[@class = "product-full__size js-product-full-size"]//text()')[0].get()
        short_des = response.xpath('//h2//text()').get()
        Benefits = response.xpath('//li[@class = "product-overview--about"]//div//text()').get()
        Ingredients = response.xpath('//li[@class = "product-overview--ingredients js-product-overview--ingredients"]//div//text()').get()
        recommend =  response.xpath('//li[@class = "product-overview--product_usage"]//div//text()').get()
        image = response.xpath('//div[@class = "product-full__image js-product-full__image"]//img/@src').get()

        yield {
            'Title':Title,
            'description':description,
            'price':price,
            'qty':qty,
            'short_des':short_des,
            'Benefits':Benefits,
            'Ingredients':Ingredients,
            'recommend':recommend,
            'image':image
        }