import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy import desc
from snowball import Stemmer
from dotenv import load_dotenv

Base = declarative_base()

load_dotenv()


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


class SavedRecipes(Base):
    __tablename__ = 'SavedRecipes'
    id = Column(String(250), primary_key=True)
    recipe_id = Column(String(250), nullable=False)
    user_id = Column(Integer, nullable=False)
    recipe_title = Column(String(250), nullable=False)

    def __init__(self, user_id, recipe_id, recipe_title):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.id = str(uuid.uuid4())
        self.recipe_title = recipe_title
        if not self.is_saved_recipe_exists():
            session = DBSession()
            session.expire_on_commit = False
            session.add(self)
            session.commit()
            session.close()

    def is_saved_recipe_exists(self):
        session = DBSession()
        result = bool(session.query(SavedRecipes).filter(SavedRecipes.recipe_id == self.recipe_id).filter(SavedRecipes.user_id == self.user_id).first())
        session.close()
        return result


engine = create_engine(f"postgresql+psycopg2://postgres:{os.environ.get('postgres_pass')}@localhost:5432/recipeDB", echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)


def get_dish_types_all():
    session = DBSession()
    return session.query(Recipe.dish_type, func.count(Recipe.dish_type)).\
        group_by(Recipe.dish_type).order_by(desc(func.count(Recipe.dish_type))).all()


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


def get_recipe_list(query=None, dish_type=None):
    if query and not dish_type:
        return get_recipe_list_by_query(query=query)
    if dish_type and not query:
        return get_recipe_list_by_dish_type(dish_type=dish_type)
    if query and dish_type:
        return get_recipe_list_by_query_and_dish_type(query=query, dish_type=dish_type)
    else:
        raise ValueError('query and dish_type cannot be None')


def get_recipe_list_by_query(query):
    session = DBSession()
    st = Stemmer()
    stem = st.stem(query)
    recipe_list = session.query(Recipe).filter(Recipe.title.ilike(f'%{stem}%')).order_by(desc(Recipe.bookmarks)).limit(
        50).all()
    session.close()
    return recipe_list


def get_recipe_list_by_dish_type(dish_type):
    session = DBSession()
    recipe_list = session.query(Recipe).filter(Recipe.dish_type == dish_type).order_by(desc(Recipe.bookmarks)).limit(
        50).all()
    session.close()
    return recipe_list


def get_recipe_list_by_query_and_dish_type(query, dish_type):
    session = DBSession()
    st = Stemmer()
    stem = st.stem(query)
    recipe_list = session.query(Recipe).\
        filter(Recipe.dish_type == dish_type).\
        filter(Recipe.title.ilike(f'%{stem}%')).order_by(desc(Recipe.bookmarks)).limit(50).all()
    session.close()
    return recipe_list


def get_saved_recipes_list_by_user_id(user_id):
    session = DBSession()
    saved_recipe_list = session.query(SavedRecipes).filter(SavedRecipes.user_id == user_id).all()
    session.close()
    return saved_recipe_list


def get_recipe_by_id(recipe_id):
    session = DBSession()
    recipe = session.query(Recipe).filter(Recipe.id == recipe_id).one()
    session.close()
    return recipe


def delete_saved_recipes_by_user_id(user_id):
    session = DBSession()
    saved_recipe_list = session.query(SavedRecipes).filter(SavedRecipes.user_id == user_id).all()
    for saved_recipe in saved_recipe_list:
        session.delete(saved_recipe)
    session.commit()
    session.close()
    return None


def delete_saved_recipes_by_user_id_by_title(user_id, title):
    session = DBSession()
    # IF recipe title is too long, Tg will cut it for 140 smbls and add '...' (in keyboard)
    # To prevent manage it, cut this string for 130 smbls, just in case
    normalized_title = title[0:130]
    saved_recipe = session.query(SavedRecipes).filter(SavedRecipes.user_id == user_id).\
        filter(SavedRecipes.recipe_title.ilike(f'%{normalized_title}%')).first()
    session.delete(saved_recipe)
    session.commit()
    session.close()
    return None
