import random
import classes
from classes.RecipesDB import Recipe
def get_random_item_from_list(lst):
    r = random.randrange(0, lst.__len__())
    return lst[r]


def convert_recipe_obj_to_message(recipe: Recipe):

    d = {
        'photo': recipe.recipe_img_url,
        'caption': f'<b><a href="{recipe.recipe_url}">{recipe.title}</a></b>',
        'parse_mode': 'HTML'
    }
    return d




