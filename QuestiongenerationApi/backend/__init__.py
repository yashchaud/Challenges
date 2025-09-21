from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    CORS(app)

    with app.app_context():
        from backend.utils.database import init_db
        init_db()

   
    from backend.routes import auth
    app.register_blueprint(auth.bp)

    return app