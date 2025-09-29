from apps.web.flask_app import create_app

app = create_app()

if __name__ == "__main__":
    # host 0.0.0.0 para que Codespaces pueda exponer el puerto
    app.run(host="0.0.0.0", port=5000, debug=True)
