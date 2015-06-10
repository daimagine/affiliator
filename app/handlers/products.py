#tornado
import tornado.web
import json
from tornado import gen
import collections
from ..utils.cache import cache
import logging
logger = logging.getLogger('logs/affiliate.application.log')
logger.setLevel(logging.DEBUG)

from ..utils.common import JsonHandler, CacheJsonHandler
from ..models.product import Product

class ProductHandler(CacheJsonHandler):
	@gen.coroutine
	@cache(60) # set the cache expires
	def get(self):
		try:
			products = self.db.query(Product).all()
			self.response['product_list'] = products
			self.write_json()
		except Exception as error:
			logger.exception(error.message)
			message = 'Failed to fetch data'
			self.send_error(500, message=message)
