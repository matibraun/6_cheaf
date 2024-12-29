from datetime import date, timedelta

def get_alert_status(product_expiration_date, days_before_expiration_to_trigger):
    today = date.today()
    trigger_date = product_expiration_date - timedelta(days=days_before_expiration_to_trigger)
    if today >= trigger_date:
        return "expired"
    return "active"