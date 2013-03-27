import os
from flask import Flask, render_template


#----------------------------------------
# Initialization
#----------------------------------------

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    )


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
