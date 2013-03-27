import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

#----------------------------------------
# Initialization
#----------------------------------------

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    )

db = SQLAlchemy(app)


#----------------------------------------
# Models
#----------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

# Create a test user
'''
user = User('John Doe', 'john@example.com')
db.session.add(user)
db.session.commit()
'''


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
