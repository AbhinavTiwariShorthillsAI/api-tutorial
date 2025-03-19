from api_tutorial import app, db

with app.app_context():
    db.create_all()