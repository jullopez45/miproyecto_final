
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import db

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    from .routes.auth import auth_bp
    from .routes.public import public_bp
    from .routes.cart import cart_bp
    from .routes.orders import orders_bp
    from .routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    from .models import User, Category, Product, db
    if not User.query.filter_by(email="admin@tienda.com").first():
        from . import bcrypt
        admin = User(name="Admin", email="admin@tienda.com",
                     password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
                     role="admin")
        db.session.add(admin)
    if Category.query.count() == 0:
        cats = ["Running", "Casual", "Basketball", "Skate", "Outdoor"]
        categories = [Category(name=c) for c in cats]
        db.session.add_all(categories)
        db.session.flush()
        sample_products = [
            Product(name="Zapatilla Runner Pro", description="Ligera y rápida para correr",
                    price=299000, stock=20, category_id=categories[0].id),
            Product(name="Zapatilla Urbana", description="Cómoda para el día a día",
                    price=199000, stock=35, category_id=categories[1].id),
            Product(name="Zapatilla Dunk Shot", description="Estilo basketball clásico",
                    price=259000, stock=15, category_id=categories[2].id),
        ]
        db.session.add_all(sample_products)
    db.session.commit()
