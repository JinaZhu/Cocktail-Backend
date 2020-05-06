from flask import Flask, session, jsonify, request
from model import connect_to_db, db, User, Ingredient, Cocktail


app = Flask(__name__)
app.secret_key = 'TEMP'

if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)
    app.run()