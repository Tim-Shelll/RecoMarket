from main import db, site
site.app_context().push()
db.create_all()