from alerts.services import display_alerts, notify_alerts
from celery import shared_task
from products.models import Product

@shared_task
def alerts_information():

    products_with_active_alerts = Product.get_products_with_active_alerts()

    display_alerts(products_with_active_alerts)
   
    return "Alerts information triggered successfully."


@shared_task
def alerts_notifications():

    products_with_alerts_to_be_triggered_today = Product.get_products_with_alerts_to_be_triggered_today()

    notify_alerts(products_with_alerts_to_be_triggered_today)

    return "Alerts notification triggered successfully."
