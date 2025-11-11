from app_config import app  # Import `app` from the new configuration file
from routes.auth_routes import auth_bp  # Import the auth blueprint

app.register_blueprint(auth_bp)  # Register the blueprint

if __name__ == '__main__':
    app.run(debug=True)