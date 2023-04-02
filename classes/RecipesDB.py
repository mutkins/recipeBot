from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import desc
from snowball import Stemmer
import tools

from classes import UserRecipeRequest, UserRecipeSettings

Base = declarative_base()




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
        session.add(self)
        session.commit()
        session.close()


class Ingredients(Base):
    __tablename__ = 'Ingredients'
    id = Column(String(250), primary_key=True)
    recipe_id = Column(String(250), nullable=True)
    name = Column(String(250), nullable=True)
    quantity = Column(String(250), nullable=True)

    def add_item(self):
        session = DBSession()
        session.expire_on_commit = False
        session.add(self)
        session.commit()
        session.close()


engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/recipeDB", echo=True)
sa.orm.configure_mappers()
Base.metadata.create_all(engine)


DBSession = sessionmaker(bind=engine)


def get_dish_types_all():
    session = DBSession()
    return session.query(Recipe.dish_type, func.count(Recipe.dish_type)).\
        group_by(Recipe.dish_type).order_by(desc(func.count(Recipe.dish_type))).all()


# ТУТ функция получения рецептов
def get_recipes(urr: UserRecipeRequest, urs: UserRecipeSettings=None):
    session = DBSession()
    recipe_list =\
        session.query(Recipe).filter(Recipe.dish_type == urr.dish_type).order_by(desc(Recipe.bookmarks)).limit(50).all()
    recipe = tools.get_random_item_from_list(recipe_list)
    return recipe


def get_available_dish_types():
    dish_types = get_dish_types_all()
    dish_types_list = []
    for i in range(dish_types.__len__()):
        dish_types_list.append(dish_types[i][0])
    return dish_types_list


def get_ingredients_by_recipe(recipe: Recipe):
    session = DBSession()
    ingredients_list = session.query(Ingredients).filter(Ingredients.recipe_id == recipe.id).all()
    return ingredients_list


def get_recipes_by_query(text):
    session = DBSession()
    st = Stemmer()
    stem = st.stem(text)
    recipe_list = session.query(Recipe).filter(Recipe.title.ilike(f'%{stem}%')).order_by(desc(Recipe.bookmarks)).limit(50).all()
    recipe = tools.get_random_item_from_list(recipe_list)
    return recipe
