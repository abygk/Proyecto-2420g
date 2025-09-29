from flask import Flask, render_template

def create_app():
    # Flask buscará templates/ y static/ en la carpeta indicada
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
