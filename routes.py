from flask import render_template, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required

from forms import RegisterForm, ProductForm, LoginForm, CommentForm
from models import Product, User, Comment
import os
from ext import app, db


@app.route("/")
def home():
    # products = Product.query.filter(Product.price > 100, Product.price < 500, Product.name == "New Product #1").all()
    products = Product.query.all()
    return render_template("index.html", produktebi=products, role="Admin")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, password=form.password.data)

        db.session.add(new_user)
        db.session.commit()
        flash("თქვენ წარმატებით დარეგისტრირდით")
        return redirect("/login")



    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    # თუ ავტორიზაცია გაიარა ადმინის როლის მქონე იუზერმა, მხოლოდ
    # მას ჰქონდეს პროდუქტების შეცვლის/რედაქტირების/შექმნის/წაშლის უფლება.

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(form.username.data == User.username).first()
        if user and user.check_password(form.password.data):
            print(user.check_password(form.password.data))
            login_user(user)
            flash("თქვენ წარმატებით გაიარეთ ავტორიზაცია")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/create_product", methods=["GET", "POST"])
@login_required
def create_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(name=form.name.data, price=form.price.data)

        image = form.img.data
        directory = os.path.join("static", "images", image.filename)
        image.save(directory)

        new_product.img = image.filename

        db.session.add(new_product)
        db.session.commit()

    return render_template("create_product.html", form=form)


@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect("/")


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(name=product.name, price=product.price)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        # შეამოწმეთ ატვირთულია თუ არა პროდუქტის ფოტო, თუ არსებობს
        # რედაქტირებისას აღარ აგვარჩევინოს თავიდან და ათუ არ არსებობს მაშინ გვჭირდებოდეს ატვირთვა

        db.session.commit()
        return redirect("/")

    return render_template("create_product.html", form=form)


@app.route("/product/<int:product_id>", methods=["GET", "POST"])
def product(product_id):
    detailed_product = Product.query.get(product_id)
    comments = Comment.query.filter(Comment.product_id == detailed_product.id).all()
    form = CommentForm()
    print(1)
    if form.validate_on_submit():
        print(2)
        new_comment=Comment(text=form.text.data, product_id=product_id)

        db.session.add(new_comment)
        db.session.commit()
        return redirect(f"/product/{product_id}")

    return render_template("detailed_page.html", form=form, product=detailed_product, comments=comments)
