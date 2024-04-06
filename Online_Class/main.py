from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from text_summary import summarizer
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, current_user, logout_user


db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secrets"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///video-meeting.db"
db.init_app(app)



db = SQLAlchemy()


login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Register.query.get(int(user_id))


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True


with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/analyze', methods = ['GET', 'POST'])
def analyze():
    # it is good that i should initialize the text here else it will crash if no value is passed 
    summary = "Enter Correct value to be initialised"
    org_txt = "Enter Valid length of text"
    line_of_summary = 0

    if request.method == 'POST':
        rawtext = request.form['rawtext']
        summary, org_txt, line_of_summary = summarizer(summary)

    return render_template('summary.html',  summary = summary, original_txt = org_txt, total_line_in_summary = line_of_summary)


if __name__ == '__main__':
    app.run()

