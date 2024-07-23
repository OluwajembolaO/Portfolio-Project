from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy






app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(200),nullable = False) 
    password = db.Column(db.String(200),nullable = False)


@app.route('/')
def index():
    food = 'tomatoes'


    return render_template('index.html',food = food)




if __name__ == '__main__': 
    app.run(debug = True)


