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

from sqlalchemy.sql import exists
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from ..models.product import Product
from ..models.customer import Customer
from ..models.affiliate import Affiliate, AffiliateSchema

class ProductAffiliateHandler(CacheJsonHandler):
	@gen.coroutine
	def get(self):
		try:
			criteria = self.db.query(Affiliate).options(joinedload(Affiliate.customer)).options(joinedload(Affiliate.product))
			# filtering
			if 'customer_id' in self.request.arguments:
				customer_id = int(self.get_argument('customer_id'))
				logger.debug('customer_id criteria: %s' % customer_id)
				criteria = criteria.filter(Customer.id == customer_id)

			affiliates = criteria.all()
			serializer = AffiliateSchema(many=True)
			self.response = serializer.dump(affiliates).data
			self.write_json()

		except Exception as error:
			logger.exception(error.message)
			message = 'Failed to fetch data'
			self.send_error(500, message=message)


	@gen.coroutine
	@cache(cache_enabled=False)
	def post(self, product_id):
		try:
			customer_id = self.request.data['customer_id']
			logger.debug('customer_id %s', customer_id)

			# check duplicate
			stmt = exists().where(Affiliate.product_id == product_id).where(Affiliate.customer_id == customer_id)
			if self.db.query(stmt).scalar():
				self.response['message'] = 'Customer already joined affiliate for this product'
			else:
				product = self.db.query(Product).filter(Product.id == product_id).first()
				customer = self.db.query(Customer).filter(Customer.id == customer_id).first()

				if product == None:
					message = 'Product is not found'
					self.send_error(404, message=message)
					return

				elif customer == None:
					message = 'Customer is not found'
					self.send_error(404, message=message)
					return

				else:
					affiliate = Affiliate(product=product, customer=customer)
					self.db.add(affiliate)
					result = self.db.commit()

					self.response['message'] = 'Customer %s has been join affiliate for product %s successfully' % (customer.email, product.name)

			self.write_json()

		except NoResultFound as error:
			logger.exception(error.message)
			message = 'Resource Unavailable'
			self.send_error(404, message=message)

		except Exception as error:
			logger.exception(error.message)
			message = 'Failed to update product affiliate'
			self.send_error(500, message=message)

