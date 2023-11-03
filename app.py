from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///d:/flask/SR1/instance/feedback.db'
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(200), nullable=False)

class FeedbackForm(FlaskForm):
    username = StringField('Нікнейм', validators=[DataRequired()])
    text = TextAreaField('Ваш відгук', validators=[DataRequired()])
    submit = SubmitField('Надіслати')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FeedbackForm()

    if form.validate_on_submit():
        username = form.username.data
        text = form.text.data
        feedback = Feedback(username=username, text=text)

    try:
        db.session.add(feedback)
        db.session.commit()
        flash('Ваш відгук був збережений', 'success')
        form.username.data = ''
        form.text.data = ''
    except:
        db.session.rollback()
        flash('Помилка при збереженні відгука', 'danger')


    feedbacks = Feedback.query.all()
    return render_template('index.html', form=form, feedbacks=feedbacks)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

