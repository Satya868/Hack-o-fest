from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_wtf import FlaskForm
from text_summary import summarizer
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
import pdfkit


db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secrets"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///video-meeting.db"
db.init_app(app)



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


class RegistrationForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8, max=20)])


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])




@app.route("/")
def home():
    # return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Register.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully!", "info")
    return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user = Register(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created Successfully! <br>You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", first_name=current_user.first_name, last_name=current_user.last_name)


@app.route("/meeting")
@login_required
def meeting():
    return render_template("meeting.html", username=current_user.username)

@app.route("/summ_input")
@login_required
def sum_input():
    return render_template("summ_input.html")


# @app.route("/analysis")

@app.route('/analyze', methods = ['GET', 'POST'])
@login_required
def analyze():
    # it is good that i should initialize the text here else it will crash if no value is passed 
    summary = "Enter Correct value to be initialised"
    org_txt = "Enter Valid length of text"
    line_of_summary = 0

    if request.method == 'POST':
        rawtext = request.form['rawtext']
        summary, org_txt, line_of_summary = summarizer(rawtext)

    return render_template('summary.html',  summary = summary, original_txt = org_txt, total_line_in_summary = line_of_summary)



@app.route("/download_pdf", methods=['GET', 'POST'])
@login_required
def download_pdf():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        summary, org_txt, line_of_summary = summarizer(rawtext)
        rendered_html = render_template("summary_template.html", summary=summary)

        pdf = pdfkit.from_string(rendered_html, False)

        response = Response(pdf, content_type='application/pdf')
        response.headers['Content-Disposition'] = 'attachment; filename="summary.pdf"'

        return response

    return render_template("download_pdf.html")

@app.route("/join", methods=["GET", "POST"])
@login_required
def join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/meeting?roomID={room_id}")

    return render_template("join.html")


if __name__ == "__main__":
    app.run(debug=True)