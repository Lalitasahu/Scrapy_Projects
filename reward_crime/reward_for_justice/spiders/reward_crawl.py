import scrapy
import json
from datetime import datetime
from bs4 import BeautifulSoup as BS
from scrapy.http import JsonRequest,FormRequest

class RewardCrawlSpider(scrapy.Spider):
    name = 'reward_crawl'
    allowed_domains = ['rewardsforjustice.net']
    # start_urls = ['http://reward.com/']

    data = {
        'action': 'jet_smart_filters',
        'provider': 'jet-engine/rewards-grid',
        'query[_tax_query_crime-category][]': [
            '1070',
            '1071',
            '1073',
            '1072',
            '1074',
        ],
        'defaults[post_status][]': 'publish',
        'defaults[post_type][]': [
            'north-korea',
            'rewards',
        ],
        'defaults[posts_per_page]': '9',
        'defaults[paged]': '1',
        'defaults[ignore_sticky_posts]': '1',
        'settings[lisitng_id]': '22078',
        'settings[columns]': '3',
        'settings[columns_tablet]': '1',
        'settings[columns_mobile]': '1',
        'settings[post_status][]': 'publish',
        'settings[use_random_posts_num]': '',
        'settings[posts_num]': '9',
        'settings[max_posts_num]': '',
        'settings[not_found_message]': 'No data was found',
        'settings[is_masonry]': '',
        'settings[equal_columns_height]': '',
        'settings[use_load_more]': '',
        'settings[load_more_id]': '',
        'settings[load_more_type]': 'click',
        'settings[load_more_offset][unit]': 'px',
        'settings[load_more_offset][size]': '0',
        'settings[loader_text]': '',
        'settings[loader_spinner]': '',
        'settings[use_custom_post_types]': 'yes',
        'settings[custom_post_types][]': [
            'north-korea',
            'rewards',
        ],
        'settings[hide_widget_if]': '',
        'settings[carousel_enabled]': '',
        'settings[slides_to_scroll]': '3',
        'settings[arrows]': 'true',
        'settings[arrow_icon]': 'fa fa-angle-left',
        'settings[dots]': '',
        'settings[autoplay]': '',
        'settings[autoplay_speed]': '5000',
        'settings[infinite]': '',
        'settings[center_mode]': '',
        'settings[effect]': 'slide',
        'settings[speed]': '500',
        'settings[inject_alternative_items]': '',
        'settings[injection_items][0][item]': '90086',
        'settings[injection_items][0][_id]': 'a4c8515',
        'settings[injection_items][0][item_num]': '1',
        'settings[injection_items][0][inject_once]': 'yes',
        'settings[injection_items][0][meta_key]': 'dprk',
        'settings[injection_items][0][item_condition_type]': 'item_meta',
        'settings[injection_items][0][static_item]': 'yes',
        'settings[scroll_slider_enabled]': '',
        'settings[scroll_slider_on][]': [
            'desktop',
            'tablet',
            'mobile',
        ],
        'settings[custom_query]': '',
        'settings[custom_query_id]': '',
        'settings[_element_id]': 'rewards-grid',
        'settings[jet_cct_query]': '',
        'settings[jet_rest_query]': '',
        'props[found_posts]': '181',
        'props[max_num_pages]': '21',
        'props[page]': '1',
        'paged': '1',
        'referrer[uri]': '/index/?jsf=jet-engine:rewards-grid&tax=crime-category:1070%2C1071%2C1073%2C1072%2C1074',
        'referrer[info]': '',
        'referrer[self]': '/index.php',
        'indexing_filters': '[41852,41851]',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://rewardsforjustice.net',
        'Connection': 'keep-alive',
        'Referer': 'https://rewardsforjustice.net/index/?jsf=jet-engine:rewards-grid&tax=crime-category:1070%2C1071%2C1073%2C1072%2C1074',
        # 'Cookie': '_ga_BPR2J8V0QK=GS1.1.1681378168.2.1.1681379041.0.0.0; _ga=GA1.1.1980574960.1681374747; wp-wpml_current_language=en; cookie_notice_accepted=true',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    api_url = 'https://rewardsforjustice.net/wp-admin/admin-ajax.php'
    def start_requests(self):
        yield FormRequest(url = self.api_url,headers = self.headers,method='POST',formdata = self.data,callback = self.parse, meta={'page':1})

    def parse(self, response):
        # print(response.text)
        # pass
        js = response.json()
        page_number = response.meta['page']

        soup = BS(js['content'],'html.parser')
        for i in soup.find_all('div','jet-listing-grid__item'):
            profile_url = i.find('div','jet-engine-listing-overlay-wrap').get('data-url')
            category = i.find('div','elementor-widget-wrap elementor-element-populated').find('h2').text.strip()
            yield scrapy.Request(profile_url,headers=self.headers,callback=self.parse_detail,meta={'profile_url':profile_url,'category':category})
        
        if js['pagination']['max_num_pages'] >= page_number:
            self.data['paged'] = str(page_number+1)
            yield FormRequest(url = self.api_url,headers = self.headers,method='POST',formdata = self.data,callback = self.parse, meta={'page':page_number+1})
            


    def parse_detail(self,response):
        profile_url = response.meta.get('profile_url')
        category = response.meta.get('category')
        soup = BS(response.text)
        try:
            Title = soup.find('h2','elementor-heading-title').text
        except:
            Title = 'None'
        
        try:
            rewards_amound = [i.text for i in soup.find_all('h2','elementor-heading-title elementor-size-default')][1]
        except:
            rewards_amound = "None"

        try:
            Associated_Organization = [i.text for i in soup.find_all('div','jet-listing jet-listing-dynamic-terms')][1]
        except:
            Associated_Organization = 'None'
        try:
            Associated_Location = [i.text for i in soup.find('div','elementor-element elementor-element-fcb86f5 dc-has-condition dc-condition-empty elementor-widget elementor-widget-text-editor')]
        except:
            Associated_Location = 'None'
        try:
            About = soup.find('div','elementor-element elementor-element-52b1d20 elementor-widget elementor-widget-theme-post-content').text.strip()
        except:
            About = 'None'
        try:
            image = soup.find('picture','attachment-medium size-medium').find('img').get('src').replace('-300x169','')
        except:
            image = 'None'
        
        try:
            # D_O_B = soup.find('div','elementor-element elementor-element-9a896ea dc-has-condition dc-condition-empty elementor-widget elementor-widget-text-editor').find('div').text.strip()
            D_O_B = soup.find('div',attrs={'data-id':'9a896ea'}).text.strip().split(';')[0]
            datetime.strptime(D_O_B,'%d %B %Y').isoformat()
        except:
            D_O_B = 'None'
        
        
        yield {
            "name":Title,
            'cat':category,
            'profile_url':profile_url,
            'rewards_amound':rewards_amound,
            'Associated_Organization':Associated_Organization,
            'Associated_Location':Associated_Location,
            'About':About,
            'image':image,
            'D_O_B':D_O_B

            }


