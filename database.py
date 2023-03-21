import sqlalchemy.orm
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, exc
from sqlalchemy.orm import mapper, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


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


    def update_user_recipe_settings(self, user_id, ingr=None, diet=None, health=None, cuisineType=None, dishType=None, time=None, excluded=None):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()


engine = create_engine("sqlite:///recipe.db", echo=True)
Base.metadata.create_all(engine)


def save_user_recipe_settings(data):
    new_set = UserRecipeSettings(user_id=data.get('user_id'), ingr=data.get('ingr'), diet=data.get('diet'),
                                 health=data.get('health'), cuisineType=data.get('health'),
                                 dishType=data.get('dishType'), time=data.get('time'), excluded=data.get('excluded'))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.add(new_set)
    session.commit()


def get_user_recipe_settings_by_user_id(user_id):
    # check if user has settings
    res = find_user_recipe_settings_by_user_id(user_id)
    urs = res[0]
    session = res[1]
    if urs:
        return urs,session
    else:
        # if doesnt - create new settings (with write to db yet)
        res = create_user_recipe_settings_by_user_id(user_id)

        return res[0],res[1]


def find_user_recipe_settings_by_user_id(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(UserRecipeSettings).filter_by(user_id=user_id).first(), session


def create_user_recipe_settings_by_user_id(user_id):
    DBSession = sessionmaker(bind=engine)
    new_urs_object = UserRecipeSettings(user_id=user_id)
    session = DBSession()
    session.expire_on_commit = False
    session.add(new_urs_object)
    session.commit()
    return new_urs_object, session


def update_user_recipe_settings(urs_object: UserRecipeSettings, session: sqlalchemy.orm.session.Session):
    session.commit()


def test(a: UserRecipeSettings, session: sqlalchemy.orm.session.Session):

    session.commit()
    return a


def test2():
    res = test3()
    a = res[0]
    session = res[1]
    a.ingr="TSAS"
    test(a, session)
    print()

def test3():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.expire_on_commit = False
    # a = session.query(UserRecipeSettings).filter_by(user_id=313781825).first()
    a = UserRecipeSettings(user_id=12323)
    session.add(a)
    session.commit()
    return a, session
