import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "please-change-this-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'yazarvpn.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_ADMIN_CHAT_ID = os.environ.get("TELEGRAM_ADMIN_CHAT_ID", "")
    TELEGRAM_CHANNEL_USERNAME = os.environ.get("TELEGRAM_CHANNEL_USERNAME", "Yazarvpn")

    # --- Admin panel login ---
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    # از دستور توضیح داده‌شده در README برای ساخت هش پسورد استفاده کنید
    ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", "")

    # --- Site ---
    SITE_NAME = os.environ.get("SITE_NAME", "YazarVPN")
    SITE_CURRENCY = os.environ.get("SITE_CURRENCY", "تومان")
