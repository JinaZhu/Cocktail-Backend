from sqlalchemy import func
from model import connect_to_db, db, User, Ingredient, Cocktail

def add_user(user_input, pw_hash):
    """Save user information into database"""

    new_user = User(
                email=user_input['email'],
                first_name=user_input['fname'],
                last_name=user_input['lname'],
                password=pw_hash
                )
    
    db.session.add(new_user)
    db.session.commit()

    return new_user