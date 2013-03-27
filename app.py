import os
from flask import Flask, render_template, flash, redirect, session, url_for, request, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.wtf import Form, TextField, Required

#----------------------------------------
# Initialization
#----------------------------------------

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    DEBUG = True,
    # Heroku Setting
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'],
    # Local Development sqlite setting
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    CSRF_ENABLED = True,
    SECRET_KEY = 'my_secret_key',
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
    name = db.Column(db.String(80))
    email = db.Column(db.String(255), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

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


class LoginForm(Form):
    name = TextField('name', validators=[Required()])
    email = TextField('email', validators=[Required()])

class RegisterForm(Form):
    name = TextField('name', validators=[Required()])
    email = TextField('email', validators=[Required()])


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
    if form.validate_on_submit():
        # Check username and password against database here
        the_user = User.query.filter_by(name=form.name.data).first()
        if the_user:
            login_user(the_user)
            return redirect(url_for('index'))
        # User failed to log in, show login page again
        else:
            return render_template('login.html', title='Sign In', form=form)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Save new user to database
        new_user = User(name=form.name.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register New User', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


#----------------------------------------
# Launch
#----------------------------------------

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
