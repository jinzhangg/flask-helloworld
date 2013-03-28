import os
from flask import Flask, render_template, flash, redirect, session, url_for, request, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash


#----------------------------------------
# Initialization
#----------------------------------------

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    # Database Setting For Heroku
    # Searches for Heroku's DATABASE_URL setting or default to local settings if unable to find
    #
    # Postgresql - use this if your local database is Postgresql
    #SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "postgresql://postgres:postgres_pw@localhost/database_1"),
    # Sqlite - use this if your local database is Sqlite
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(basedir, "app.db")),
    CSRF_ENABLED=True,
    SECRET_KEY='your_secret_key',
    DEBUG=True,
    )

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
login_manager.init_app(app)


#----------------------------------------
# Models
#----------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    pw_hash = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Name %r>' % self.name


#----------------------------------------
# Controllers
#----------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Check if form field validation checks out
    if form.validate_on_submit():
        # Check username and password against database here
        the_user = User.query.filter_by(email=form.email.data).first()
        if the_user:
            # Email found, next check the password
            pw = the_user.check_password(form.password.data)
            if pw:
                # Password was correct, log the user in
                login_user(the_user)
                return redirect(url_for('index'))
            else:
                # Password was incorrect
                flash("Incorrect password.")
                return render_template('login.html', title='Sign In', form=form)
        # User failed to log in, show login page again
        else:
            # Email was not found in database
            flash("User not found.")
            return render_template('login.html', title='Sign In', form=form)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # Check if form field validation checks out
    if form.validate_on_submit():
        # Check if email already exist in database
        the_user = User.query.filter_by(email=form.email.data).first()
        if the_user:
            # Email already exist, report error to user
            flash("Account with " + form.email.data + " already exist!")
            return redirect(url_for('register'))
        else:
            # Save new user to database
            new_user = User(email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful. Please log in.")
            return redirect(url_for('login'))
    return render_template('register.html', title='Register New User', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out.")
    return redirect(url_for('index'))


#----------------------------------------
# Launch
#----------------------------------------

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
