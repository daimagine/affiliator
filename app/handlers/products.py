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

class ProductHandler(CacheJsonHandler):
	@gen.coroutine
	@cache(60) # set the cache expires
	def get(self):
		try:
			cursor = yield self.db.execute('SELECT * from product as p inner join customer as c on p.customer_id = c.id;')
			rows = cursor.fetchall()
			results = []
			for row in rows:
				p = collections.OrderedDict()
				p['id'] = row['id']
				p['name'] = row['name']
				results.append(p)

			self.response['product_list'] = results
			self.write_json()
		except Exception as error:
			logger.exception(error.message)
			message = 'Failed to fetch data'
			self.send_error(500, message=message)
