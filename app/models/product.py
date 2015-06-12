
from sqlalchemy import Column, String, BigInteger, Numeric, Boolean
from sqlalchemy.schema import Sequence
from ..utils.base import Base

from marshmallow import Schema, fields, pprint

class Product(Base):
	__tablename__ = 'product'
	id = Column(BigInteger, Sequence('seq_affiliate_id', start=1, increment=1), primary_key=True)
	name = Column(String(255), nullable=False)
    
	is_affiliate_ready = Column(Boolean, default=False)
	affiliate_percentage  = Column(Numeric(3, 2))
	affiliate_fee = Column(Numeric(12, 2))
	affiliate_fee_type = Column(String(1))


class ProductSchema(Schema):
	class Meta:
		fields = ('id', 'name', 'is_affiliate_ready', 'affiliate_percentage', 'affiliate_fee', 'affiliate_fee_type')


# metadata
metadata = Base.metadata

def create_all():
	metadata.create_all(engine)