from ext import app, db
from models import Product, User, Comment

with app.app_context():
    db.drop_all()
    db.create_all()

    # ადმინის იუზერის შექმნა
    admin = User(username="Admin", password="Adminpass", role="Admin")
    db.session.add(admin)
    db.session.commit()