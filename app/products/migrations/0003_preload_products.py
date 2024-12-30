from django.db import migrations
from django.utils.timezone import now
from datetime import timedelta
import random


def preload_products_and_alerts(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    Alert = apps.get_model('alerts', 'Alert')
    User = apps.get_model('auth', 'User')

    users = list(User.objects.all())

    if not users:
        raise Exception("No users available to assign to products.")

    product_names = [f"Product {i}" for i in range(1, 11)]

    products = []
    alerts = []
    today = now().date()

    for name in product_names:
        user = random.choice(users)
        expiration_date = today + timedelta(days=random.randint(10, 365))

        product = Product(
            name=name,
            description=f"Description for {name}",
            stock_quantity=random.randint(1, 100),
            expiration_date=expiration_date,
            user=user,
        )
        products.append(product)

    Product.objects.bulk_create(products)

    for product in Product.objects.all():
        alerts.append(Alert(product=product, days_before_expiration_to_trigger=5))
        alerts.append(Alert(product=product, days_before_expiration_to_trigger=10))

    Alert.objects.bulk_create(alerts)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_preload_users'),
        ('products', '0002_product_user'),
    ]

    operations = [
        migrations.RunPython(preload_products_and_alerts),
    ]
