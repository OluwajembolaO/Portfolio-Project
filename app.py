from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # Required for form security
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True) 
    password = db.Column(db.String(200), nullable=False)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Debugging statements
        print(f"Username: {username}")
        print(f"Password: {password}")

        if username is None or password is None:
            error_message = 'Both username and password are required!'
            return render_template('signUp.html', error=error_message)
        
        usernameExists = User.query.filter_by(username=username).first()
        if usernameExists:
            error_message = f'This username ({username}) already exists!'
            return render_template('signUp.html', error=error_message)
        elif len(password) < 8:
            error_message = "Your password is too short. It must be at least 8 characters long."
            return render_template('signUp.html', error=error_message)
        else:
            newUser = User(username=username, password=password)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('signUp.html')

@app.route('/', methods=['GET', 'POST'])
def signIn():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Replace with your database query logic
        # Example assumes User model has 'name' and 'password' fields
        user = User.query.filter_by(username=username).first()

        if user is None:
            error_message = f"This username ({username}) doesn't exist. Please try again."
            return render_template('signIn.html', error=error_message)
        else:
            if user.password == password:
                session['username'] = user.username  # Store the username in the session
                return redirect(url_for('index'))
            else:
                error_message = "Incorrect password. Please try again."
                return render_template('signIn.html', error=error_message)

    return render_template('signIn.html')   


if __name__ == '__main__':
    app.run(debug=True)
