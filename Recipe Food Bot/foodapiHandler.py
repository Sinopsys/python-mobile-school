# coding: utf8
import unirest
import re

# Получение рецептов в JSON
def get_meals(lst, quantity):
    try:
        lst1 = make_ingredients(lst)
        response = unirest.get(
        "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?"
        "fillIngredients=false&"
        "ingredients="
        "{0}"
        "&limitLicense=false"
        "&number={1}"
        "&ranking=2".format(''.join(lst1), quantity),
        headers={
            "X-Mashape-Key": "m8ElunDBXbmshHKyr0iS5b6mdPs6p1DW9EMjsnAT1EWTBz47U7",
            "Accept": "application/json"
        }
    )
        return response.body
    except:
        return 'null'
    

    
def make_ingredients(lst):
    return '%2C'.join(lst).replace(" ", "+")
    # res = []
    # [res.append('%2C' + item) for item in lst]
    # res[0] = res[0][3:]
    # return res


# Инициализация получения рецептов
def find_food(ingredients, quantity):
    lst = [] 
    try:
         food_lst = []
         requests = get_meals(ingredients, quantity)
         if requests != 'null':
             i = 0
             lst = []    
             for item in requests:
                 image = item["image"]
                 id = item["id"]
                 title = item["title"]
                 recipe = re.sub(r'\s+', ' ', get_food_by_id(id)["instructions"])
                 time_to_cook = get_food_by_id(id)["readyInMinutes"]
                 lst.append([id, title, image, recipe, time_to_cook])
             return lst        
         else:
             return 'null'
    except:
        if(len(lst) >= 1):
            return lst;
        else:
            return 'null'

def get_food_by_id(id):
    response = unirest.get(
        "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{}"
        "/information?includeNutrition=false".format(id),
        headers={
            "X-Mashape-Key": "m8ElunDBXbmshHKyr0iS5b6mdPs6p1DW9EMjsnAT1EWTBz47U7",
            "Accept": "application/json"
        }
    )
    return response.body