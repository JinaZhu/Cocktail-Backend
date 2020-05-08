from flask import Flask, session, jsonify, request
from model import connect_to_db, db, User, Ingredient, Cocktail


@app.route('/save', method=["POST"])
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


app = Flask(__name__)
app.secret_key = 'TEMP'

if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)
    app.run()
