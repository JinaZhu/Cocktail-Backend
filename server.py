from flask import Flask, session, jsonify, request
from flask_bcrypt import Bcrypt
from model import connect_to_db, db, User, Cocktail
from model_helper import add_user
import os
import requests


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'TEMP'
cocktail_api_key = os.environ['cocktail_api_key']


@app.route('/getUser', methods=['GET'])
def get_user():
    """Check if user is already logged in"""

    check_user = session.get('user')
    user = User.query.filter(User.user_id == check_user).first()

    if user:
        return {'response': user.first_name}

    return 'User is not logged in'


@app.route('/register', methods=['POST'])
def register_form():
    """User register form"""
    user_input = request.get_json()
    user = User.query.filter(User.email == user_input['email']).first()    
    
    if user:
        return {'message': 'User account already exists'}

    pw_hash = bcrypt.generate_password_hash(user_input['password']).decode('utf-8')
    new_user = add_user(user_input, pw_hash)

    session['user'] = new_user.user_id

    response = {'userName': new_user.first_name,
                'message': 'Successfully registered!'}

    return jsonify(response)


@app.route('/login', methods=['POST'])
def login():
    """User login"""

    user_login = request.get_json()
    user = User.query.filter(User.email == user_login['email']).first()
    
    if user:
        pw_match = bcrypt.check_password_hash(user.password, user_login['password'])
    
    if not user or not pw_match:
    # if not (user) or (user.password != user_login['password']):
        return {'message': 'The user or password information is incorrect'}

    session['user'] = user.user_id

    response = {'userName': user.first_name,
                'message': 'Successfully logged in!'}

    return jsonify(response)


@app.route('/logout', methods=['POST'])
def logout():
    """User logout"""

    del session['user']

    return ('', 204)


@app.route('/save', methods=["POST"])
def user_saved_recipes():
    """save user's favorite recipes in database"""

    get_save = request.get_json()
    drink_img = get_save['drink_image']
    drink_ingr = get_save['drink_ingr']
    drink_name = get_save['drink_name']

    user_id = session.get("user")
    current_user = User.query.filter_by(user_id=user_id).first()

    if not current_user:
        return {'response': 'User is not logged in'}

    existing_save = Cocktail.query.filter_by(
        user_id=user_id, cocktail_name=drink_name).first()

    if not existing_save:
        save_cocktail = Cocktail(
            user_id=user_id, cocktail_name=drink_name, img_url=drink_img)

        db.session.add(save_cocktail)
        db.session.commit()

        return {'response': 'Saved'}
    else:
        return {'response': 'Already Saved'}

    return "saved!"


@app.route('/displaySavedCocktails')
def display_saved_cocktails():
    """send client user's saved cocktails for display"""

    current_user = session.get("user")
    saved_cocktail = Cocktail.query.filter_by(user_id=current_user).all()

    saved_cocktail_detail = []

    for cocktail in saved_cocktail:
        saved_cocktail_detail.append({'cocktail_name': cocktail.cocktail_name,
                                      'img_url': cocktail.img_url})
    
    return jsonify(saved_cocktail_detail)


def drink_recipe(drink_results):
    """api search for drinks recipes"""

    drink_info = []

    for drink in drink_results:
        drink_name = drink['drink_name']
        drink_dict = {'drink_name': drink_name,
                      'drink_image': drink['drink_thumb']}
        drink_name = drink_name.replace(' ', '_')
        # print('drink names', drink_name)

        recipe_api = requests.get(
            f'https://www.thecocktaildb.com/api/json/v2/{cocktail_api_key}/search.php?s={drink_name}')

        recipe_results = recipe_api.json()
        # print(recipe_results)

        drink_ingredients = []
        num = 1

        while f'strIngredient{num}' in recipe_results['drinks'][0] and recipe_results['drinks'][0][f'strIngredient{num}'] is not None:
            drink_ingredients.append(
                recipe_results['drinks'][0][f'strIngredient{num}'])
            num += 1

        drink_dict['drink_ingr'] = drink_ingredients

        drink_info.append(drink_dict)

    return drink_info


@app.route('/ingredientsresults.json', methods=["POST"])
def search_bar():
    """api results for search bar based on ingredients"""

    # get form variable from search bar
    list_of_ingredients = request.get_json()
    # print('list_of_ingredients', list_of_ingredients['ingredients'])

    # joins each item in list by getting rid of white space between commas
    ingredients = ",".join(list_of_ingredients['ingredients'])
    # print('ingredients', ingredients)

    # #api request using CocktailDB
    ingredients_api = requests.get(
        f'https://www.thecocktaildb.com/api/json/v2/{cocktail_api_key}/filter.php?i={ingredients}')

    # #converting get request into JSON file
    ingredients_results = ingredients_api.json()

    # #assigning drink results to drinks key
    drinks = ingredients_results['drinks']
    # print('drinks', drinks)

    # #create list for search results
    drink_results = []

    if drinks == 'None Found':
        return {'message': 'No results found'}

    # #append drink string into new list
    for i in range(0, 10):
        if i < len(drinks):
            drink_results.append({'drink_name': drinks[i]['strDrink'],
                                  'drink_thumb': drinks[i]['strDrinkThumb']})
        else:
            break

    cocktails_list = drink_recipe(drink_results)

    return jsonify(cocktails_list)


@app.route('/getIngredients.json', methods=["POST"])
def get_ing_from_saved():

    saved_cocktail = request.get_json()
    saved_cocktail = saved_cocktail.replace(' ', '_').lower()

    ingredients = requests.get(
        f'https://www.thecocktaildb.com/api/json/v2/{cocktail_api_key}/search.php?s={saved_cocktail}')

    ing_results = ingredients.json()
    drink_ingredients = []

    num = 1

    while f'strIngredient{num}' in ing_results['drinks'][0] and ing_results['drinks'][0][f'strIngredient{num}'] is not None:
        drink_ingredients.append(ing_results['drinks'][0][f'strIngredient{num}'])
        num += 1
    
    return jsonify(drink_ingredients)


@app.route('/deleteSavedCocktail', methods=['POST'])
def delete_saved_cocktail():

    remove_cocktail = request.get_json()
    user_id = session.get("user")

    current_user = User.query.filter_by(user_id=user_id).first()
    existing_save = Cocktail.query.filter_by(
        user_id=user_id, cocktail_name=remove_cocktail).delete()

    db.session.commit()

    return {'response': f'{remove_cocktail} deleted'}



if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)
    app.run()
