import sys
from model import User, Ingredient, Cocktail, connect_to_db, db


def open_and_read_file(filepath):
    """Open file and convert into string"""

    file = open(filepath)
    str_data = file.read()
    file.close()

    return str_data

def seed_data(str_data):
    """Seed all ingredients into database"""

    str_data = str_data.split('\n')
    for ingredient in str_data:

        new_ingredient = Ingredient(ing_name=ingredient)
        db.session.add(new_ingredient)

        db.session.commit()



if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    db.create_all()

    print("Connected to DB.")

    str_data = open_and_read_file('ingredients.txt')
    seed_data(str_data)

    print('Successfully seeded into db')