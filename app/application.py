# tornado
import tornado.web
import json
#cache
from utils.cache import RedisCacheBackend, CacheMixin
import redis

import logging
logger = logging.getLogger('logs/affiliate.application.log')
logger.setLevel(logging.DEBUG)

from utils.common import JsonHandler

# sqla
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# resource handler
from handlers.products import ProductHandler
from handlers.product_affiliates import ProductAffiliateHandler

class Application(tornado.web.Application):
    def __init__(self):
        api_version = "v1"
        handlers = [
            (r"/", HomeHandler),
            (r"/api/%s/products" % api_version, ProductHandler),
            (r"/api/%s/products/([0-9]+)" % api_version, ProductHandler),
            (r"/api/%s/affiliates" % api_version, ProductAffiliateHandler),
            (r"/api/%s/affiliates/([0-9]+)/actions/join" % api_version, ProductAffiliateHandler)
        ]
        settings = dict(
            xsrf_cookies=False,
            debug=True,
        )
        self.redis = redis.Redis()
        self.cache = RedisCacheBackend(self.redis)
        
        # sqla
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/shortlrdb', echo=True)
        self.db = scoped_session(sessionmaker(bind=engine))

        super(Application, self).__init__(handlers, **settings)

class HomeHandler(JsonHandler):
    def get(self):
        #write response
        self.response['title'] = "Jualio Affiliate API"
        self.write_json()
