#tornado
import tornado.web
import json
from tornado import gen
from ..utils.cache import cache
import logging
logger = logging.getLogger('logs/affiliate.application.log')
logger.setLevel(logging.DEBUG)

from ..utils.common import JsonHandler, CacheJsonHandler

class ProductHandler(CacheJsonHandler):
	@gen.coroutine
	@cache(60) # set the cache expires
	def get(self):
		try:
			cursor = yield self.db.execute('SELECT * from product;')
			self.response['product_list'] = cursor.fetchall()
			self.write_json()
		except Exception as error:
			logger.exception(error.message)
			message = 'Failed to fetch data'
			self.send_error(500, message=message)
