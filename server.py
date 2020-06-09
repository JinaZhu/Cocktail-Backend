from flask import Flask, session, jsonify, request
from model import connect_to_db, db, User, Ingredient, Cocktail
from model_helper import add_user
import os
import requests

cocktail_api_key = os.environ['cocktail_api_key']


@app.route('/register', methods=['POST'])
def register_form():
    """User register form"""
    user_input = request.get_json()
    user = User.query.filter(User.email == user_input['email']).first()

    if user:
        return {'message': 'User account already exists'}

    new_user = add_user(user_input)

    session['user'] = new_user.user_id

    response = {'userName': new_user.first_name,
                'message': 'Successfully registered!'}

    return jsonify(response)


@app.route('/login', methods=['POST'])
def login():
    """User login"""

    user_login = request.get_json()
    user = User.query.filter(User.email == user_login['email']).first()

    if not (user) or (user.password != user_login['password']):
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

    cocktail_name = request.form["cocktailName"]
    img_url = request.form["imgUrl"]
    ingredients = request.form["ingredients"]
    user_id = session.get("user_id")

    current_user = User.query.filter_by(user_id=user_id).first()

    if not current_user:
        return ("Please login or register!")

    check_duplicates = Cocktail.query.filter_by(
        user_id=user_id, cocktail_name=cocktail_name).first()

    if not check_duplicates:
        save_cocktail = Cocktail(cocktail_name=cocktail_name,
                                 img_url=img_url, ing_name=ingredients, user_id=user_id)

        db.session.add(save_cocktail)
        db.session.commit()

    return "saved!"


@app.route('/displaySavedCocktails')
def display_saved_cocktails():
    """send client user's saved cocktails for display"""

    current_user = session.get("user_id")
    saved_cocktail = Cocktail.query.filter_by(user_id=current_user).all()

    saved_cocktail_detail = []

    for cocktail in saved_cocktail:
        saved_cocktail_detail.append({'cocktail_name': cocktail.cocktail_name,
                                      'img_url': cocktail.img_url, 'ingredients': cocktail.ing_name})

    return jsonify(saved_cocktail_detail)

@app.route('/ingredientsresults.json')
def search_bar():
    """api results for search bar based on ingredients"""

    #get form variable from search bar
    list_of_ingredients = request.args["ingredients"]

    #joins each item in list by getting rid of white space between commas
    ingredients = ",".join(list_of_ingredients)

    #api request using CocktailDB 
    ingredients_api = requests.get(f'https://www.thecocktaildb.com/api/json/v2/{cocktail_api_key}/filter.php?i={ingredients}')
    
    #converting get request into JSON file
    ingredients_results = ingredients_api.json()

    #assigning drink results to drinks key
    drinks = ingredients_results['drinks']
    
    #create list for search results
    drink_results = []

    #append drink string into new list
    for i, drink in enumerate(drinks):
        drink_results.append({'drink_name': drinks[i]['strDrink'], 
                            'drink_thumb': drinks[i]['strDrinkThumb']})
    
    return jsonify(drink_results)

if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)
    app.run()
