from flask import Flask, session, jsonify, request
from model import connect_to_db, db, User, Ingredient, Cocktail
from model_helper import add_user


app = Flask(__name__)
app.secret_key = 'TEMP'

@app.route('/register', methods=['POST'])
def register_form():
    """User register form"""

    user_input = request.get_json()

    user = User.query.filter(User.email == user_input['email']).first()

    if user:
        return
    
    new_user = add_user(user_input)

    session['user'] = new_user.user_id

    return (new_user.first_name)


@app.route('/login', methods=['POST'])
def login():
    """User login"""

    user_login = request.get_json()

    user = User.query.filter(User.email == user_login['email']).first()

    if not (user) or (user.password != user_login['password']):
        return
    
    session['user'] = user.user_id

    return (user.first_name)


@app.route('/logout', methods=['POST'])
def logout():
    """User logout"""

    del session['user']

    return ('', 204)


if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)
    app.run()