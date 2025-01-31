from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = b'\xeb\xa2\xc9\x1b#\x84\xb8\x1cjq\xc0\x1e3\x11+\xc9'
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app