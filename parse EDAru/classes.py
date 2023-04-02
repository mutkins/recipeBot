import sqlalchemy.orm
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, exc
from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

# Configure loggingingredient
logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

Base = declarative_base()
engine = create_engine("sqlite:///eda_ru.db", echo=True)


class Recipe(Base):
    __tablename__ = 'Recipes'
    id = Column(String(250), primary_key=True)
    title = Column(String(250), nullable=True)
    recipe_url = Column(String(250), unique=True, nullable=False)
    recipe_img_url = Column(String(250), nullable=True)
    dish_type = Column(String(250), nullable=True)
    cuisine_type = Column(String(250), nullable=True)
    count_of_portions = Column(String(250), nullable=True)
    time_text = Column(String(250), nullable=True)
    time_int = Column(Integer, nullable=True)
    bookmarks = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)


    def add_item(self):
        session = DBSession()
        session.expire_on_commit = False
        try:
            session.add(self)
            session.commit()
            session.close()
        except:
            session.rollback()
            session.close()
            raise
    # def __init__(self, id=None, title=None, recipe_url=None, recipe_img_url=None, dish_type=None, cuisine_type=None,
    #              count_of_portions=None, time=None):
    #     self.id = id
    #     self.title = title
    #     self.recipe_url = recipe_url
    #     self.recipe_img_url = recipe_img_url
    #     self.dish_type = dish_type
    #     self.cuisine_type = cuisine_type
    #     self.count_of_portions = count_of_portions
    #     self.time = time


class Ingredients(Base):
    __tablename__ = 'Ingredients'
    id = Column(String(250), primary_key=True)
    recipe_id = Column(String(250), nullable=True)
    name = Column(String(250), nullable=True)
    quantity = Column(String(250), nullable=True)

    def add_item(self):
        session = DBSession()
        session.expire_on_commit = False
        try:
            session.add(self)
            session.commit()
            session.close()
        except:
            session.rollback()
            session.close()
            raise
    # def __init__(self, id=None, name=None, quantity=None):
    #     self.id = id
    #     self.name = name
    #     self.quantity = quantity


Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

