# tornado
import tornado.web
import json
import logging
logger = logging.getLogger('logs/affiliate.application.log')
logger.setLevel(logging.DEBUG)

from utils.common import JsonHandler

# resource handler
from handlers.products import ProductHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/products", ProductHandler)
        ]
        settings = dict(
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)

class HomeHandler(JsonHandler):
    def get(self):
        #write response
        self.response['title'] = "Jualio Affiliate Web Service"

        self.write_json()
