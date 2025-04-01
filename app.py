import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# configure the database with SQLite fallback
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///bot.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

@app.route('/health')
def health_check():
    """Health check endpoint for Uptime Robot."""
    from bot import _last_health_check
    import time

    # Check if the bot's last health check was within the last 10 minutes
    current_time = time.time()
    bot_healthy = (current_time - _last_health_check) < 600  # 10 minutes

    status = {
        'status': 'healthy' if bot_healthy else 'unhealthy',
        'timestamp': current_time,
        'last_health_check': _last_health_check
    }

    return jsonify(status), 200 if bot_healthy else 503

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    db.create_all()