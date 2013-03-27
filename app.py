import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models import User

#----------------------------------------
# Initialization
#----------------------------------------

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config.update(
    DEBUG = True,
    # Heroku Setting
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'],
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    )

db = SQLAlchemy(app)


#----------------------------------------
# Controllers
#----------------------------------------

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    return render_template('index.html')


#----------------------------------------
# Launch
#----------------------------------------

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
