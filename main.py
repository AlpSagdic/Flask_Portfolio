from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_ckeditor import CKEditorField
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOU_CHOSE_A_SECRET_KEY'
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Contact Form
class ContactForm(FlaskForm):
    user_name = StringField("What's Your Name?", validators=[DataRequired()])
    user_email = EmailField("What's Your Email Address?", validators=[Email()])
    message_subject = StringField("What's Your Subject?", validators=[DataRequired()])
    message = CKEditorField("What's Your Message?", validators=[DataRequired()])
    submit = SubmitField("Submit")


#Database
class ContactUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=False, nullable=False)
    user_email = db.Column(db.String(100), unique=False, nullable=False)
    message_subject = db.Column(db.String(100), unique=False, nullable=False)
    message = db.Column(db.String(5000), unique=False, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        user_info = ContactUser(
            user_email=form.user_email.data,
            user_name=form.user_name.data,
            message_subject=form.message_subject.data,
            message=form.message.data
        )
        db.session.add(user_info)
        db.session.commit()
        return render_template("index.html")
    return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)