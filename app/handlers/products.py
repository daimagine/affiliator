#tornado
import tornado.web
import json
from tornado import gen
import logging
logger = logging.getLogger('logs/affiliate.application.log')
logger.setLevel(logging.DEBUG)

from ..utils.common import JsonHandler

class ProductHandler(JsonHandler):
	@gen.coroutine
	def get(self):
		try:
			cursor = yield self.db.execute('SELECT * from product;')
			results = cursor.fetchall()
			self.response['message'] = results
			self.write_json()
		except Exception as error:
			logger.exception(error.message)
			message = error.message
			self.send_error(500, message=message)
