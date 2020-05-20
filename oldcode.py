# -----------------------------------------------------------------------------
# Start sqlalchemy attempt 1
# -----------------------------------------------------------------------------
import constants
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import Index
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	restaurant_id = Column(String(250), index = True, primary_key = True)
	ages_allowed = Column(String(250))
	price_range = Column(Integer)
	categories = relationship('Category', secondary = 'restaurant_category')

class Category(Base):
	__tablename__  = 'category'
	category_id = Column(Integer, primary_key = True)
	restaurants = relationship('Restaurant', secondary = 'restaurant_category')
	name = Column(String(250), nullable = False)

class Restaurant_Category(Base):
	__tablename__ = 'restaurant_category'
	category_id = Column(Integer, ForeignKey('category.category_id'),
	                     primary_key = True)
	restaurant_id = Column(String(250), ForeignKey('restaurant.restaurant_id'),
						   primary_key = True)


db_path = 'sqlite:///' + constants.BASE_PATH + constants.DB_FILENAME

# Create the DB Engine and get an engine variable
engine = db.create_engine( db_path )

connection = engine.connect( )

Base.metadata.create_all(engine)

# -----------------------------------------------------------------------------
# End sqlalchemy attempt 1
# -----------------------------------------------------------------------------