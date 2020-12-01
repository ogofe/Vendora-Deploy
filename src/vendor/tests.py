from django.test import TestCase
from datetime import datetime
from .models import Alert


class AlertsTest(TestCase):
    " test class for alerts"

    def test_is_welcome_alert(self):
        "Compares Alerts to see if it is a welcome message."
        objs = Alert.objects.get(id=1)
        today = datetime.now().date()
        self.assertEqual(today, objs.date, "Yes It Is!")