
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import db, User
from .. import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Bienvenido, {}!".format(user.name), "success")
            return redirect(url_for("public.index"))
        flash("Correo o contraseña incorrectos", "danger")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        if not name or not email or not password:
            flash("Completa todos los campos", "warning")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("Este correo ya está registrado", "warning")
            return render_template("register.html")
        pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(name=name, email=email, password_hash=pw_hash, role="customer")
        db.session.add(user)
        db.session.commit()
        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("public.index"))

@auth_bp.route("/profile", methods=["GET","POST"])
@login_required
def profile():
    if request.method == "POST":
        current_user.name = request.form.get("name", current_user.name)
        db.session.commit()
        flash("Perfil actualizado", "success")
    return render_template("profile.html")
