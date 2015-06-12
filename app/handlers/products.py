#tornado
import tornado.web
import json
from tornado import gen
import collections
from ..utils.cache import cache
import logging
logger = logging.getLogger('logs/affiliate.application.log')
logger.setLevel(logging.DEBUG)

from ..utils.common import ParseUtil, JsonHandler, CacheJsonHandler
from ..models.product import Product

class ProductHandler(CacheJsonHandler):
	@gen.coroutine
	def get(self, id=None):
		try:
			criteria = self.db.query(Product)
			if id == None:
				# filtering
				if 'affiliate' in self.request.arguments:
					affiliate = ParseUtil.parseBool(self.get_argument('affiliate'))
					logger.debug('affiliate criteria: %s' % affiliate)
					criteria = criteria.filter(Product.is_affiliate_ready == affiliate)

				products = criteria.all()
				self.response = products
			else:
				criteria = self.db.query(Product).filter(Product.id == id)
				product = criteria.one()
				self.response = product
			self.write_json()

		except Exception as error:
			logger.exception(error.message)
			message = 'Failed to fetch data'
			self.send_error(500, message=message)

