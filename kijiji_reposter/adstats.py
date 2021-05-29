
from collections import namedtuple

TITLE = "title"
PRICE = "price"
DATE_POSTED = 'date_posted'
DATE_DELETED = 'date_deleted'
VIEWS = 'views'
REPLIES = 'replies'
PAGE_NO = 'page_no'
MAIN_IMG = 'main_img'

schema = [TITLE, PRICE, DATE_POSTED, DATE_DELETED, VIEWS, 
    REPLIES, PAGE_NO, MAIN_IMG]

schema_str = ' '.join(schema)

StatItem = namedtuple("StatItem", schema_str)


