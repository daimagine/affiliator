#tornado
import tornado.web
import json
import logging
logger = logging.getLogger('logs/affiliate.application.log')

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
				for k, v in json_data.items():
                    # Tornado expects values in the argument dict to be lists.
                    # in tornado.web.RequestHandler._get_argument the last argument is returned.
					json_data[k] = [v]
				self.request.arguments.pop(self.request.body)
				self.request.arguments.update(json_data)
			except ValueError, e:
				logger.debug(e.message)
				message = 'Unable to parse JSON.'
				self.send_error(400, message=message) # Bad Request

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
		output = json.dumps(self.response)
		self.write(output)