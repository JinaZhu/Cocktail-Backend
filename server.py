from flask import Flask, session, jsonify, request
from model import connect_to_db, db, User, Ingredient, Cocktail


@app.route('/save', method=["POST"])
def user_saved_recipes():
    """save user's favorite recipes in database"""

    cocktail_name = request.form["cocktailName"]
    img_url = request.form["imgUrl"]
    ingredients = request.form["ingredients"]
    current_user = session.get("user_id")
    user_id = User.query.filter_by(user_id=user_id).first()

    if not current_user:
        return ("Please login or register!")

    check_duplicates = Cocktail.query.filter_by(
        user_id=user_id, cocktail_name=cocktail_name).first()

    if not check_duplicates:
        save_cocktail = Save(cocktail_name=cocktail_name,
                             img_url=img_url, ingredients=ingredients, user_id=user_id)


app = Flask(__name__)
app.secret_key = 'TEMP'

if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)
    app.run()
