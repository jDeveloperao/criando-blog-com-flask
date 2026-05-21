from flask import Flask ,  render_template
from extensios import db
from models.post import Post
from models.user import User
from routes.auth import auth_bp
from routes.users import user_bp
from extensios import lm
from flask_login import login_required
import os
from dotenv import load_dotenv


app = Flask(__name__)


load_dotenv()
app.secret_key = os.getenv("secret_key")
app.config["SESSION_COOKIE_HTTPONLY"] = True
#app.config["SESSION_COOKIE_SAMESITE"] = "Last"
app.config["REMENBER_COOKIE_SECURE"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_uri")


db.init_app(app)
lm.init_app(app)
lm.login_message = "Faça login primeiro!"
lm.login_view = "auth.login"


@lm.user_loader
def get_user(id):
    return User.query.filter_by(id = id).first()

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
@login_required
def root():

    return render_template("index.html")


app.register_blueprint(auth_bp , url_prefix ="/auth")
app.register_blueprint(user_bp , url_prefix = "/user")

with app.app_context():
    db.create_all()

app.run(debug = True , host= "localhost" , port= 5000)