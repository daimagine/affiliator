#tornado
import tornado.web
import json
import decimal
import datetime
#sqla
from sqlalchemy.ext.declarative import DeclarativeMeta
#cache
from cache import RedisCacheBackend, CacheMixin
import logging
logger = logging.getLogger('logs/affiliate.application.log')
logger.setLevel(logging.DEBUG)

class BaseHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

class AlchemyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, decimal.Decimal):
			return float(obj)
		elif isinstance(obj, datetime.datetime):
			return obj.isoformat()
		elif isinstance(obj.__class__, DeclarativeMeta):
			# an SQLAlchemy class
			fields = {}
			for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
				data = obj.__getattribute__(field)
				try:
					json.dumps(data) # this will fail on non-encodable values, like other classes
					fields[field] = data
				except TypeError:
					fields[field] = None
			# a json-encodable dict
			return fields
		else:
			return json.JSONEncoder.default(self, obj)

class JsonHandler(BaseHandler):
	"""RequestHandler for JSON request and response"""
	def prepare(self):
		if self.request.body:
			try:
				json_data = json.loads(self.request.body)
				for k, v in json_data.items():
                    # Tornado expects values in the argument dict to be lists.
                    # in tornado.web.RequestHandler._get_argument the last argument is returned.
					json_data[k] = [v]
				self.request.arguments.pop(self.request.body)
				self.request.arguments.update(json_data)
			except ValueError, e:
				logger.debug(e.message)
				message = 'Unsupported Media Type'
				self.send_error(415, message=message) # Bad Request

		# Set up response dictionary.
		self.response = dict()

	def set_default_headers(self):
		self.set_header('Content-Type', 'application/vnd.api+json')

	def write_error(self, status_code, **kwargs):
		if 'message' not in kwargs:
			if status_code == 405:
				kwargs['message'] = 'Invalid HTTP method.'
			else:
				kwargs['message'] = 'Unknown error.'

		self.response = kwargs
		self.write_json()

	def write_json(self):
		output = json.dumps(self.response, cls=AlchemyEncoder)
		# logger.info('write output %s' % output)
		self.write(output)

class CacheJsonHandler(CacheMixin, JsonHandler):
	def prepare(self):
		super(CacheJsonHandler, self).prepare()

