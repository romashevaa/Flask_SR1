from app import app, Feedback

with app.app_context():
    feedbacks = Feedback.query.all()

for feedback in feedbacks:
    print(feedback.text)
