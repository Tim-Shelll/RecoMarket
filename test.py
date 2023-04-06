from main import site, db

with site.app_context():
    db.create_all()