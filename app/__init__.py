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

    # Crear admin si no existe
    if not User.query.filter_by(email="admin@tienda.com").first():
        from . import bcrypt
        admin = User(
            name="Admin",
            email="admin@tienda.com",
            password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="admin"
        )
        db.session.add(admin)

    # Crear categorías si no existen
    if Category.query.count() == 0:
        cats = [
            "Botas de fútbol para césped artificial",
            "Botas de fútbol para césped natural.",
            "Botas de fútbol multitacos.",
            "Botas de fútbol AG (AG – Artificial Grass)",
            "Botas de fútbol Turf (TF – Turf)",
            "Botas de fútbol de aluminio (SG – Soft Ground)"
        ]
        categories = [Category(name=c) for c in cats]
        db.session.add_all(categories)
        db.session.flush()
    else:
        categories = Category.query.order_by(Category.id).all()

    # Borrar productos existentes antes de insertar nuevos
    Product.query.delete()
    db.session.commit()

    # Productos de ejemplo
    sample_products = [
        Product(
            name="New Balance Furon 4.0 Pro FG",
            description="Presenta una horma rediseñada para un ajuste superior y comodidad, con una puntera más baja. Incorpora la tecnología FantomFit para un ajuste ligero y seguro.",
            price=489000,
            stock=20,
            category_id=categories[0].id,
            image_url="https://www.futbolemotion.com/imagesarticulos/236637/750/bota-adidas-f50-elite-fg-turbo-aurora-black-platin-met-0.webp"
        ),
        Product(
            name="Adidas F50 League SG.",
            description="Cuentan con una parte superior de material sintético que busca un ajuste cómodo y una buena sensación con el balón",
            price=340000,
            stock=35,
            category_id=categories[1].id,
            image_url="https://media.foot-store.es/catalog/product/cache/image/1800x/9df78eab33525d08d6e5fb8d27136e95/a/d/adidas_if8819_9_footwear_photography_mirrored_pair_view_white-nw052424.jpg"
        ),
        Product(
            name="Nike Phantom GX 2 Academy",
            description="La parte superior suave y el diseño general buscan proporcionar un ajuste cómodo durante todo el partido",
            price=450000,
            stock=15,
            category_id=categories[2].id,
            image_url="https://images.prodirectsport.com/ProductImages/Main/1019031_Main_1832897.jpg"
        ),
        Product(
            name="Adidas Predator Club Turf",
            description="Cuentan con un ajuste clásico, sistema de amarre de cordones y forro interno textil para mayor comodidad.",
            price=220000,
            stock=10,
            category_id=categories[3].id,
            image_url="https://www.futbolemotion.com/imagesarticulos/248158/540/bota-adidas-predator-league-turf-nino-core-black-grey-four-lucid-red-0.jpg"
        ),
        Product(
            name="Nike Phantom 6 High Academy FG/MG.",
            description="Incorpora una textura adherente, especialmente en la zona de golpeo, para mejorar el contacto y la precisión al golpear el balón.",
            price=350000,
            stock=8,
            category_id=categories[4].id,
            image_url="https://www.futbolemotion.com/imagesarticulos/268899/750/bota-nike-phantom-6-high-akademie-fg-mg-azul-electrico-0.webp"
        ),
        Product(
            name="Nike Phantom 6 High Academy FG/MG.",
            description="Incorpora una textura adherente, especialmente en la zona de golpeo, para mejorar el contacto y la precisión al golpear el balón.",
            price=350000,
            stock=8,
            category_id=categories[4].id,
            image_url="https://www.futbolemotion.com/imagesarticulos/268899/750/bota-nike-phantom-6-high-akademie-fg-mg-azul-electrico-0.webp"
        ),
        Product(
            name="Nike Phantom 6 High Academy FG/MG.",
            description="Incorpora una textura adherente, especialmente en la zona de golpeo, para mejorar el contacto y la precisión al golpear el balón.",
            price=350000,
            stock=8,
            category_id=categories[4].id,
            image_url="https://www.futbolemotion.com/imagesarticulos/268899/750/bota-nike-phantom-6-high-akademie-fg-mg-azul-electrico-0.webp"
        ),
        Product(
            name="Nike Phantom 6 High Academy FG/MG.",
            description="Incorpora una textura adherente, especialmente en la zona de golpeo, para mejorar el contacto y la precisión al golpear el balón.",
            price=350000,
            stock=8,
            category_id=categories[4].id,
            image_url="https://www.futbolemotion.com/imagesarticulos/268899/750/bota-nike-phantom-6-high-akademie-fg-mg-azul-electrico-0.webp"
        ),
    ]

    db.session.add_all(sample_products)
    db.session.commit()
