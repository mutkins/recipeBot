import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

class Recipe(ABC):
    pass


class Recipe_EDAMAM(Recipe):

    app_id = os.environ.get('edamam_app_id')
    app_key = os.environ.get('edamam_app_key')
    url = os.environ.get('edamam_api_url')
    recipes_type = "public"
    Accept_Language = "en"


class Recipe_EDAMAM_user(Recipe_EDAMAM):

    def __init__(self, ingr, diet,health, cuisineType="", dishType="", time="", excluded=""):
        self.ingr = ingr
        self.diet = diet
        self.health = health
        self.cuisineType = cuisineType
        self.dishType = dishType
        self.time = time
        self.excluded = excluded


class Recipe_EDAMAM_user_session(Recipe_EDAMAM_user):

    def __init__(self, ingr, diet, health, cuisineType="", dishType="", time="", excluded="", mealType="", ):
        super().__init__(ingr, diet, health, cuisineType, dishType, time, excluded)
        self.mealType = mealType

# load from bd
a = Recipe_EDAMAM_user_session(5,"Healfy", "Dietly", "American", "main course", "1", "pork")
a.mealType = "Breakfast"

print()
