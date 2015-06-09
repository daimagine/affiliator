#tornado
import tornado.web
import logging
logger = logging.getLogger('logs/affiliate.application.log')

from ..utils.common import BaseHandler

class ProductHandler(BaseHandler):
	def get(self):
		#TODO: get affiliate ready product list
		pass

