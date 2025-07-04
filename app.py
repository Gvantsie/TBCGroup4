from ext import app


if __name__ == "__main__":
    from routes import home, register, login, product, create_product, edit_product, delete_product
    app.run(debug=True)
