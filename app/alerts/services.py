
from .selectors import get_alert_status
from .models import Alert


def create_alert(product_id, days_before_expiration_to_trigger):

    Alert.objects.create(product_id=product_id, days_before_expiration_to_trigger=days_before_expiration_to_trigger)

def display_alerts(products):

    for product in products:
    
        print(
            f"Product: {product.name}.\n"
            f"Description: {product.description}.\n"
            f"Total alerts set up for this product: {product.alerts.all().count()}.\n"
        )
    
        for alert in product.alerts.all():
    
            print(
                f"Alert creted at {alert.created_at}\n"
                f"Set to be triggered {alert.days_before_expiration_to_trigger} days before expiration.\n"
                f"Status: {get_alert_status(product.expiration_date, alert.days_before_expiration_to_trigger)}\n"
            )

def notify_alerts(products):

    for product in products:

        print(
            f"There is an alert set for today by {product.user.first_name} {product.user.last_name} for the product {product.name} with expiration date {product.expiration_date}. \n"
            f"An email has been sent to {product.user.email}.\n"
            f"Total alerts set up for this product: {product.alerts.all().count()}.\n"
        )

        for alert in product.alerts.all():

            print(f"Alert creted at {alert.created_at}, set to be triggered {alert.days_before_expiration_to_trigger} days before expiration.")
