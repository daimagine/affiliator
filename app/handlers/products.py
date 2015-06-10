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
	def get(self):
		try:
			criteria = self.db.query(Product)

			# filtering
			if 'is_affiliate_ready' in self.request.arguments:
				criteria.filter(Product.is_affiliate_ready == self.request.get('is_affiliate_ready'))

			products = criteria.all()
			self.response = products
			self.write_json()
		except Exception as error:
			logger.exception(error.message)
			message = 'Failed to fetch data'
			self.send_error(500, message=message)
