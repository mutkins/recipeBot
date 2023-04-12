import random
from classes.RecipesDB import Recipe
from classes.RecipesDB import Ingredients


def get_random_item_from_list(lst):
    r = random.randrange(0, lst.__len__())
    return lst[r]


def convert_recipe_and_ingr_obj_to_message(recipe: Recipe, ingredients_list):

    ingredients_srt = ''
    for ingr in ingredients_list:
        ingredients_srt = ingredients_srt + f"<b>{ingr.name}:</b> {ingr.quantity}\n"

    d = {
        'photo': recipe.recipe_img_url,
        'caption': f'<b><a href="{recipe.recipe_url}">{recipe.title}</a></b>, {recipe.time_text}\n\n'
                   f'{ingredients_srt}',
        'parse_mode': 'HTML'
    }
    return d




