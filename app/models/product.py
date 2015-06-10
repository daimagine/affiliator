from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
	__tablename__ = 'product'
	id = Column(Integer, primary_key=True)
	name = Column(String(30), nullable=False)

	is_affiliate_ready = Column(Boolean, default=False)

# metadata
metadata = Base.metadata

def create_all():
	metadata.create_all(engine)