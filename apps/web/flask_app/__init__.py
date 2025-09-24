from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return "Bienvenido a la Sociedad Científica 🚀"

    return app


