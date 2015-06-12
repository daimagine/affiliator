from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.schema import Sequence
from sqlalchemy.orm import relationship, backref
from ..utils.base import Base

class Category(Base):
	__tablename__ = 'category'
	id = Column(BigInteger, Sequence('seq_affiliate_id', start=1, increment=1), primary_key=True)
	name = Column(String(255), nullable=False)

# metadata
metadata = Base.metadata

def create_all():
	metadata.create_all(engine)