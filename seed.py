"""
اجرای این فایل، دیتابیس را می‌سازد و چند بسته نمونه در آن قرار می‌دهد.
استفاده:
    python seed.py
"""

from app import create_app
from extensions import db
from models import Package

SAMPLE_PACKAGES = [
    dict(name="بسته یک ماهه اقتصادی", duration_days=30, volume_gb=30, price=79000, sort_order=1,
         description="مناسب استفاده روزمره و شبکه‌های اجتماعی."),
    dict(name="بسته یک ماهه پرحجم", duration_days=30, volume_gb=100, price=139000, sort_order=2,
         is_featured=True, description="مناسب استریم و دانلود سنگین."),
    dict(name="بسته سه ماهه", duration_days=90, volume_gb=200, price=349000, sort_order=3,
         description="صرفه اقتصادی برای استفاده سه ماهه."),
    dict(name="بسته یک ماهه نامحدود", duration_days=30, volume_gb=None, price=249000, sort_order=4,
         is_featured=True, description="بدون محدودیت حجم، برای کاربران حرفه‌ای."),
    dict(name="بسته شش ماهه", duration_days=180, volume_gb=500, price=649000, sort_order=5,
         description="بهترین گزینه برای استفاده طولانی‌مدت."),
]


def run():
    app = create_app()
    with app.app_context():
        db.create_all()
        if Package.query.count() > 0:
            print("بسته‌ها از قبل وجود دارند؛ چیزی اضافه نشد.")
            return

        for data in SAMPLE_PACKAGES:
            db.session.add(Package(**data))
        db.session.commit()
        print(f"{len(SAMPLE_PACKAGES)} بسته نمونه با موفقیت اضافه شد.")


if __name__ == "__main__":
    run()
