from __future__ import annotations
from flask import Flask
from .config import SETTINGS
from .blueprints import home, companies, sfdr, documents

def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(home.bp)
    app.register_blueprint(companies.bp)
    app.register_blueprint(sfdr.bp)
    app.register_blueprint(documents.bp)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app

def main():
    app = create_app()
    print(f"Dataland GUI läuft auf http://127.0.0.1:{SETTINGS.port}")
    app.run(host="127.0.0.1", port=SETTINGS.port, debug=True)
