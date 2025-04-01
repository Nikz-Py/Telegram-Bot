from app import db

class BotStatus(db.Model):
    """Model to track bot status and uptime."""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'healthy' or 'unhealthy'
    last_health_check = db.Column(db.DateTime, nullable=False)
