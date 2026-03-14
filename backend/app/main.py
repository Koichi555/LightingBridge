from flask import Flask
from app.api.config_routes import bp as config_bp
from app.api.status_routes import bp as status_bp
from app.api.command_routes import bp as command_bp
from app.api.log_routes import bp as log_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(config_bp)
    app.register_blueprint(status_bp)
    app.register_blueprint(command_bp)
    app.register_blueprint(log_bp)

    @app.get("/")
    def index():
        return {"code": 200, "data": {"service": "LightingBridge Backend"}, "msg": "success"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
