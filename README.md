# YazarVPN — فروشگاه بسته‌های VPN با Flask

فروشگاه مدرن و راست‌چین برای فروش بسته‌های VPN. سفارش‌ها در دیتابیس ذخیره می‌شوند و به‌صورت خودکار یک پیام به تلگرام ادمین ارسال می‌شود (شامل نام مشتری، آیدی تلگرام، بسته انتخابی و مبلغ). پرداخت و تحویل نهایی طبق درخواست شما، خارج از سایت و در تلگرام انجام می‌شود.

## امکانات

- طراحی مدرن، تیره، راست‌چین با Tailwind CSS و فونت وزیرمتن
- نمایش بسته‌ها با کارت‌های زیبا و بسته‌ی "ویژه"
- فرم ثبت سفارش (مودال) بدون رفرش صفحه
- ارسال خودکار نوتیفیکیشن سفارش به تلگرام (Bot API)
- پنل مدیریت با ورود امن (هش پسورد):
  - داشبورد سفارش‌ها با فیلتر وضعیت و آمار درآمد
  - تغییر وضعیت سفارش (در انتظار / پرداخت‌شده / تحویل‌شده / لغو)
  - افزودن، ویرایش، فعال/غیرفعال و حذف بسته‌ها
- پایگاه داده SQLite (قابل تغییر به Postgres/MySQL با تغییر `DATABASE_URL`)

## پیش‌نیاز

- Python 3.11
- یک بات تلگرام (رایگان، از طریق [@BotFather](https://t.me/BotFather))

## نصب و راه‌اندازی

### ۱) ساخت محیط مجازی و نصب پکیج‌ها

```bash
python3.11 -m venv venv
source venv/bin/activate   # ویندوز: venv\Scripts\activate
pip install -r requirements.txt
```

### ۲) ساخت فایل `.env`

```bash
cp .env.example .env
```

سپس فایل `.env` را باز کرده و مقادیر زیر را تنظیم کنید.

### ۳) ساخت بات تلگرام و گرفتن Chat ID

1. در تلگرام به [@BotFather](https://t.me/BotFather) پیام دهید و با دستور `/newbot` یک بات جدید بسازید. توکنی که می‌دهد را در `TELEGRAM_BOT_TOKEN` بگذارید.
2. به بات خودتان یک پیام (مثلاً `/start`) بدهید تا در تاریخچه چت ثبت شود.
3. آدرس زیر را در مرورگر باز کنید (به‌جای `<TOKEN>` توکن بات را بگذارید):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. در خروجی JSON دنبال مقدار `"chat":{"id": ...}` بگردید؛ همان عدد را در `TELEGRAM_ADMIN_CHAT_ID` قرار دهید.
   > اگر می‌خواهید سفارش‌ها به یک گروه ارسال شوند، بات را به گروه اضافه کنید و همین مراحل را برای گروه تکرار کنید (chat_id گروه‌ها معمولاً منفی است).

### ۴) ساخت رمز عبور پنل ادمین

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourStrongPassword'))"
```

خروجی را در `ADMIN_PASSWORD_HASH` داخل `.env` قرار دهید و `ADMIN_USERNAME` دلخواه خود را هم تنظیم کنید.

### ۵) ساخت دیتابیس و بسته‌های نمونه

```bash
python seed.py
```

### ۶) اجرای پروژه

```bash
python app.py
```

سپس به آدرس زیر بروید:

- فروشگاه: http://127.0.0.1:5000/
- پنل ادمین: http://127.0.0.1:5000/admin/login

## ساختار پروژه

```
yazarvpn/
├── app.py                  # اجرای اصلی برنامه (Application Factory)
├── config.py                # تنظیمات از فایل .env
├── extensions.py             # db, login_manager
├── models.py                 # مدل‌های Package, Order, AdminUser
├── telegram_service.py       # ارسال پیام سفارش به تلگرام
├── seed.py                   # ساخت دیتابیس و بسته‌های نمونه
├── blueprints/
│   ├── main/                 # صفحات عمومی فروشگاه
│   └── admin/                 # پنل مدیریت
├── templates/
│   ├── base.html, index.html, order_success.html
│   └── admin/ (login, dashboard, packages)
├── static/
│   ├── css/style.css
│   └── js/main.js
├── requirements.txt
└── .env.example
```

## اجرا در حالت Production

برای اجرای واقعی، به‌جای `python app.py` از یک WSGI server مثل gunicorn استفاده کنید:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

پیشنهاد می‌شود پشت یک ریورس‌پروکسی مثل Nginx با HTTPS (Let's Encrypt) قرار بگیرد، `SECRET_KEY` را با یک مقدار تصادفی و طولانی جایگزین کنید و از دیتابیس PostgreSQL برای پروداکشن استفاده کنید.

## نکات امنیتی

- هرگز `.env` را در گیت commit نکنید (در `.gitignore` قرار دارد).
- توکن بات تلگرام را مخفی نگه دارید؛ اگر لو رفت، از BotFather دستور `/revoke` را بزنید و توکن جدید بگیرید.
- رمز پنل ادمین را قوی انتخاب کنید؛ رمز به‌صورت هش‌شده نگه‌داری می‌شود.
