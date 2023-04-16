from app import db, app

# Creat database to app
with app.app_context():
    db.create_all()