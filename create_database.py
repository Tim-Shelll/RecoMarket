from main import db, site

# Creat database to app
with site.app_context():
    db.create_all()