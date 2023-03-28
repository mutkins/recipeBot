
class UserRecipeRequest:
    def __init__(self, user_id, search_query=None, dish_type=None):
        self.user_id = user_id
        self.search_query = search_query
        self.dish_type = dish_type


def get_user_recipe_request(user_id, search_query=None, dish_type=None):
    return UserRecipeRequest(user_id, search_query, dish_type)
