import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import classes.RecipesDB
import logging

import tools

browser = webdriver.Chrome()
browser.get(f"https://eda.ru/recepty?page=1")
time.sleep(12)

# Configure loggingingredient
logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


page = 0
while True:
    page += 1
    log.debug(f"TRYING TO GET PAGE #{page}")
    browser.get(f"https://eda.ru/recepty?page={page}")
    log.debug(f"PAGE #{page} has gotten")
    recipe_divs = browser.find_elements(By.CLASS_NAME, 'emotion-1f6ych6')
    log.debug(f"On the page {page} {recipe_divs.__len__()} found")
    if not recipe_divs:
        break

    for recipe_div in recipe_divs:
        recipe = classes.RecipesDB.Recipe()
        log.debug(f"CREATE NEW RECIPE...\n\n\n")
        recipe.id = str(uuid.uuid4())
        log.debug(f"recipe.id {recipe.id}")
        try:
            recipe.title = recipe_div.find_element(By.CLASS_NAME, 'emotion-1pdj9vu').text
            log.debug(f"recipe.title {recipe.title}")
        except:
            pass
        try:
            imgs = recipe_div.find_elements(By.TAG_NAME, 'source')[1].get_property('srcset')
            imgs_list = imgs.split(',')
            recipe.recipe_img_url = imgs_list[-1].split(' ')[1]
            log.debug(f"recipe.recipe_img_url {recipe.recipe_img_url}")
        except:
            pass
        try:
            recipe.recipe_url = recipe_div.find_element(By.TAG_NAME, 'a').get_property('href')
            log.debug(f"recipe.recipe_url {recipe.recipe_url}")
        except:
            pass
        try:
            recipe.dish_type = recipe_div.find_elements(By.CLASS_NAME, 'emotion-xrx6ov')[0].text
            log.debug(f"recipe.dish_type {recipe.dish_type}")
        except:
            pass
        try:
            recipe.cuisine_type = recipe_div.find_elements(By.CLASS_NAME, 'emotion-xrx6ov')[1].text
            log.debug(f"recipe.cuisine_type {recipe.cuisine_type}")
        except:
            pass
        try:
            recipe.count_of_portions = recipe_div.find_element(By.CLASS_NAME, 'emotion-dnepme').text
            log.debug(f"recipe.count_of_portions {recipe.count_of_portions}")
        except:
            pass
        try:
            recipe.time_text = recipe_div.find_element(By.CLASS_NAME, 'emotion-14gsni6').text
            log.debug(f"recipe.time {recipe.time}")
        except:
            pass
        try:
            recipe.time_int = tools.get_minutes_from_mixed_string(recipe.time_text)
            log.debug(f"recipe.time {recipe.time}")
        except:
            pass
        try:
            recipe.bookmarks = recipe_div.find_elements(By.CLASS_NAME, 'emotion-71sled')[0].text
        except:
            pass
        try:
            recipe.likes = recipe_div.find_elements(By.CLASS_NAME, 'emotion-71sled')[1].text
        except:
            pass
        try:
            log.debug(f"try to add recipe to DB")
            recipe.add_item()
        except Exception as e:
            log.error(f"ADD TO DB {recipe.title} FAILED. Ingredients wont be added. {e} \n\n")
            continue

        try:
            recipe_div.find_element(By.CLASS_NAME, 'emotion-d6nx0p').click()
        except:
            pass
        try:
            ingredient_parent_div = recipe_div.find_element(By.CLASS_NAME, 'emotion-1jiqa3z')
            ingredient_divs = ingredient_parent_div.find_elements(By.CLASS_NAME, 'emotion-ydhjlb')
            log.debug(f"On the recipe {recipe.title} {ingredient_divs.__len__()} ingredients found")
        except:
            pass

        for ingr_div in ingredient_divs:
            ingredient = classes.RecipesDB.Ingredients()
            ingredient.id = str(uuid.uuid4())
            try:
                ingredient.recipe_id = recipe.id
                log.debug(f"ingredient.recipe_id {ingredient.recipe_id}")
            except:
                pass
            try:
                ingredient.name = ingr_div.find_element(By.CLASS_NAME, 'emotion-nqq8jd').text
                log.debug(f"ingredient.name {ingredient.name}")
            except:
                pass
            try:
                ingredient.quantity = ingr_div.find_element(By.CLASS_NAME, 'emotion-wbmxm3').text
                log.debug(f"ingredient.quantity {ingredient.quantity}")
            except:
                pass
            try:
                log.debug(f"try to add ingredient to DB")
                ingredient.add_item()
            except Exception as e:
                log.error(f"ADD TO DB {ingredient.name} FAILED!!!! {e}\n\n")
        try:
            recipe_div.find_element(By.CLASS_NAME, 'emotion-14tqfr').click()
        except:
            pass


browser.quit()
