"""
ارسال نوتیفیکیشن سفارش جدید به تلگرام ادمین از طریق Bot API تلگرام.

نحوه راه‌اندازی:
1) با @BotFather یک بات بسازید و توکن آن را در TELEGRAM_BOT_TOKEN بگذارید.
2) به بات خود پیام /start بدهید (یا آن را به گروه/کانال اضافه کنید).
3) chat_id خودتان یا گروه را با فراخوانی
   https://api.telegram.org/bot<TOKEN>/getUpdates
   پیدا کنید و در TELEGRAM_ADMIN_CHAT_ID قرار دهید.
"""

import logging
import requests

logger = logging.getLogger(__name__)

TELEGRAM_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def _escape_html(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_order_message(order, package) -> str:
    phone_line = f"📱 شماره تماس: {_escape_html(order.phone)}\n" if order.phone else ""
    note_line = f"📝 توضیحات: {_escape_html(order.note)}\n" if order.note else ""

    return (
        "🛒 <b>سفارش جدید ثبت شد!</b>\n\n"
        f"👤 نام مشتری: {_escape_html(order.customer_name)}\n"
        f"💬 آیدی تلگرام: {_escape_html(order.telegram_username)}\n"
        f"{phone_line}"
        f"📦 بسته: {_escape_html(package.name)} ({package.duration_days} روزه - {package.volume_label})\n"
        f"💰 مبلغ: {order.price_at_order:,} تومان\n"
        f"{note_line}"
        f"🆔 شماره سفارش: #{order.id}\n"
        f"🕐 تاریخ: {order.created_at.strftime('%Y-%m-%d %H:%M')}"
    )


def send_order_notification(order, package, bot_token: str, chat_id: str) -> bool:
    """پیام سفارش را به تلگرام ادمین ارسال می‌کند. در صورت موفقیت True برمی‌گرداند."""
    if not bot_token or not chat_id:
        logger.warning("Telegram bot token or chat id is not configured. Skipping notification.")
        return False

    message = build_order_message(order, package)
    url = TELEGRAM_API_URL.format(token=bot_token)

    try:
        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return bool(data.get("ok"))
    except requests.RequestException as exc:
        logger.error("Failed to send Telegram notification: %s", exc)
        return False
