from sqlalchemy import Column, String, BigInteger, ForeignKey
from sqlalchemy.schema import Sequence, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from ..utils.base import Base

from marshmallow import Schema, fields, pprint

from product import Product, ProductSchema
from customer import Customer, CustomerSchema

class Affiliate(Base):
	__tablename__ = 'affiliate'
	id = Column(BigInteger, Sequence('seq_affiliate_id', start=1, increment=1), primary_key=True)
	# product relationship
	product_id = Column(BigInteger, ForeignKey('product.id'))
	product = relationship("Product", backref="affiliates")
    # customer relationship
	customer_id = Column(BigInteger, ForeignKey('customer.id'))
	customer = relationship("Customer", backref="affiliates")

	UniqueConstraint('product_id', 'customer_id', name='product_customer_affiliate_unique_constraint')


class AffiliateSchema(Schema):
	product = fields.Nested(ProductSchema)
	customer = fields.Nested(CustomerSchema)
	class Meta:
		fields = ('id', 'product', 'customer')

# metadata
metadata = Base.metadata

def create_all():
	metadata.create_all(engine)