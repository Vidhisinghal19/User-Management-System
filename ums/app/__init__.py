#ums/app/__init__.py

from flask import Flask
from admin_routes import admin_bp
from manager_routes import manager_bp


# Initialize Flask app
app = Flask(__name__)

# Import and register routes
from app import routes  # Import the routes Blueprint
app.register_blueprint(routes)

app.register_blueprint(admin_bp)
app.register_blueprint(manager_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
