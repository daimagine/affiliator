#tornado
import tornado.web
import json
import decimal
import datetime
#sqla
from sqlalchemy.ext.declarative import DeclarativeMeta
#cache
from cache import RedisCacheBackend, CacheMixin
from encoder import model_json
import logging
logger = logging.getLogger('logs/affiliate.application.log')
logger.setLevel(logging.DEBUG)

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

class JsonHandler(BaseHandler):
	"""RequestHandler for JSON request and response"""
	def prepare(self):
		if self.request.body:
			try:
				json_data = json.loads(self.request.body)
				#for k, v in json_data.items():
                    # Tornado expects values in the argument dict to be lists.
                    # in tornado.web.RequestHandler._get_argument the last argument is returned.
				#	json_data[k] = [v]
				#self.request.arguments.update(json_data)
				self.request.data = json_data
				logger.debug('request body json data')
				logger.debug(json_data)
			except ValueError, e:
				logger.debug(e.message)
				message = 'Unsupported Media Type'
				self.send_error(415, message=message) # Bad Request

		# Set up response dictionary.
		self.response = dict()

	def set_default_headers(self):
		self.set_header('Content-Type', 'application/vnd.api+json')

	def write_error(self, status_code, **kwargs):
		logger.exception('write_error with status_code %i' % status_code)
		response = dict()
		if 'message' not in kwargs:
			if status_code == 405:
				response['message'] = 'Invalid HTTP method.'
			else:
				response['message'] = 'Unknown error.'
		else:
			response['message'] = kwargs['message']

		output = json.dumps(response)
		self.write(output)

	def write_json(self):
		output = model_json(self.response)
		self.write(output)


class CacheJsonHandler(CacheMixin, JsonHandler):
	def prepare(self):
		super(CacheJsonHandler, self).prepare()


class ParseUtil(object):
	@staticmethod
	def parseBool(str):
		return str[0].upper() == 'T'