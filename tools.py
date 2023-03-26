import RecipesDB


def get_available_dish_types():
    dish_types = RecipesDB.get_dish_types_all()
    dish_types_list = []
    for i in range(dish_types.__len__()):
        dish_types_list.append(dish_types[i][0])
    return dish_types_list
