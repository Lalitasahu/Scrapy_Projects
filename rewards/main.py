import os
from datetime import datetime

file_name = datetime.now().strftime("%Y%m%d_%H%M%S")
crawler_name = 'reward_crawl'

os.system(f'python3 -m scrapy crawl reward_crawl -o {crawler_name}_{file_name}.json -o {crawler_name}_{file_name}.xlsx')
