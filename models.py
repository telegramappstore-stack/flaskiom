from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from extensions import db


class Package(db.Model):
    __tablename__ = "packages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False, default=30)
    volume_gb = db.Column(db.Integer, nullable=True)  # None = نامحدود
    price = db.Column(db.Integer, nullable=False)  # به تومان
    description = db.Column(db.Text, nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship("Order", backref="package", lazy=True)

    @property
    def volume_label(self):
        return "نامحدود" if self.volume_gb is None else f"{self.volume_gb} گیگابایت"

    def __repr__(self):
        return f"<Package {self.name}>"


class Order(db.Model):
    __tablename__ = "orders"

    STATUS_CHOICES = ("pending", "paid", "delivered", "cancelled")
    STATUS_LABELS_FA = {
        "pending": "در انتظار پرداخت",
        "paid": "پرداخت شده",
        "delivered": "تحویل داده شده",
        "cancelled": "لغو شده",
    }

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120), nullable=False)
    telegram_username = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    note = db.Column(db.Text, nullable=True)

    package_id = db.Column(db.Integer, db.ForeignKey("packages.id"), nullable=False)
    price_at_order = db.Column(db.Integer, nullable=False)

    status = db.Column(db.String(20), default="pending")
    telegram_notified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def status_label(self):
        return self.STATUS_LABELS_FA.get(self.status, self.status)

    def __repr__(self):
        return f"<Order #{self.id} - {self.customer_name}>"


class AdminUser(UserMixin):
    """کاربر ادمین ساده که از تنظیمات .env خوانده می‌شود (نیازی به جدول جدا نیست)."""

    def __init__(self, username):
        self.id = username
        self.username = username

    @staticmethod
    def validate(username, password, config):
        if username != config.ADMIN_USERNAME:
            return False
        if not config.ADMIN_PASSWORD_HASH:
            return False
        return check_password_hash(config.ADMIN_PASSWORD_HASH, password)
