from flask import Flask, session, jsonify, request
import requests
from model import connect_to_db, db, User, Ingredient, Cocktail

res = requests.get('https://www.thecocktaildb.com/api/json/v1/9973533/search.php?s=moscow_mule')

cocktail_results = res.json()

print(cocktail_results)

app = Flask(__name__)
app.secret_key = 'TEMP'

if __name__ == '__main__':

    app.debug = True

    connect_to_db(app)
    app.run()