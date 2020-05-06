from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User searching for cocktails"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):

        return f'<User user_id={self.user_id} email={self.email}>'


class Ingredient(db.Model):
    """Common ingredients for cocktail recipes"""

    __tablename__ = 'ingredients'

    ing_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ing_name = db.Column(db.String(35), nullable=False)

    def __repr__(self):
        
        return f'<Ingredient ing_id={self.ing_id} name={self.ing_name}>'


class Cocktail(db.Model):
    """Cocktail that user saved"""

    __tablename__ = 'cocktails'

    cocktail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    cocktail_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), index=True)
    ing_id = db.Column(db.Integer,
                              db.ForeignKey('ingredients.ing_id'), index=True)
    
    # Define relationship to user
    user = db.relationship('User',
                           backref=db.backref('cocktails', order_by=cocktail_id))

    # Define relationship to ingredient
    ing = db.relationship('Ingredient',
                          backref=db.backref('cocktails', order_by=cocktail_id))
                        

def connect_to_db(app, db_uri='postgresql:///cocktail'):
    
    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # Work directly with database when running module interactively
     
    from server import app
    connect_to_db(app)
    db.create_all()
    print("Connected to DB.")
    