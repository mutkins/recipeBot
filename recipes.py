import os
import urllib
import random
import requests
from dotenv import load_dotenv

load_dotenv()


def get_recipe(meal_type):
    recipes_json = get_recipes_json_from_edamam(meal_type=meal_type)
    recipe = choose_recipe(recipes_json=recipes_json)
    return recipe['label']


def get_recipes_json_from_edamam(meal_type):

    params = {
        "type": "public",
        "app_id": os.environ.get('edamam_app_id'),
        "app_key": os.environ.get('edamam_app_key'),
        "mealType": meal_type
    }
    res = requests.get(url=os.environ.get('edamam_api_url'), params=urllib.parse.urlencode(params))
    return res.json()


def choose_recipe(recipes_json):
    count_recipes_in_json = recipes_json['hits'].__len__()
    return recipes_json['hits'][random.randrange(count_recipes_in_json)]['recipe']
