import sqlalchemy.orm
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, exc
from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
engine = create_engine("sqlite:///recipe.db", echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

# при создании класса создается таблица сразу, а если существует - то подключается к ней
class UserRecipeSettings(Base):
    __tablename__ = 'UserRecipeSettings'
    user_id = Column(Integer, primary_key=True)
    ingr = Column(String(250), nullable=True)
    diet = Column(String(250), nullable=True)
    health = Column(String(250), nullable=True)
    cuisineType = Column(String(250), nullable=True)
    dishType = Column(String(250), nullable=True)
    time = Column(String(250), nullable=True)
    excluded = Column(String(250), nullable=True)

    # def __init__(self, user_id, ingr=None, diet=None, health=None, cuisineType=None, dishType=None, time=None, excluded=None):
    #     self.user_id = user_id
    #     self.ingr = ingr
    #     self.diet = diet
    #     self.health = health
    #     self.cuisineType = cuisineType
    #     self.dishType = dishType
    #     self.time = time
    #     self.excluded = excluded


def get_user_recipe_settings_by_user_id(user_id):
    session = DBSession()
    # check if user has settings
    urs = find_user_recipe_settings_by_user_id(user_id, session)
    if not urs:
        create_user_recipe_settings_by_user_id(user_id, session)
        get_user_recipe_settings_by_user_id(user_id)
    return [urs, session]


def find_user_recipe_settings_by_user_id(user_id, session: sqlalchemy.orm.session.Session):
    return session.query(UserRecipeSettings).filter_by(user_id=user_id).first()


def create_user_recipe_settings_by_user_id(user_id, session: sqlalchemy.orm.session.Session):
    new_urs_object = UserRecipeSettings(user_id=user_id)
    session.add(new_urs_object)
    session.commit()


def update_user_recipe_settings(session: sqlalchemy.orm.session.Session):
    session.commit()
    session.close()
