from django.db import models
from django.conf import settings


#--------------------------------------------------------------
# Alerts are for store owners only hence the model here.     ||
# Integrations are store dependant, so each vendor will have ||
# a set of integrations. i.e [Social, Store Management]      ||
# created when a social media, robot, payment method is      ||
# added to a store.                                          ||
#--------------------------------------------------------------
#                                                            ||
#                                                            ||
#           __________________________________________       ||
#          |___________FOR_JOEL_OGOFE_TANKO___________|      ||
#          | |\\                                  //| |      ||
#          | | \\                                // | |      ||
#          | |  \\        MAIL IS HERE !        //  | |      ||
#          | |   \\                            //   | |      ||
#          |||    \\                          //    |||      ||
#          |||     \\________________________//     |||      ||
#          |||      --------------------------      |||      ||
#          |||                                      |||      ||
#          |||                                      |||      ||
#          |||                                      |||      ||
#          |||                                      |||      ||
#          |||                                      |||      ||
#          ############################################      ||
#                                                            ||
#                                                            ||
#                                                            ||
#--------------------------------------------------------------

PRIORITIES = (
    (1, 'High'),
    (2, 'Normal'),
    (3, 'Low'),
)

INTEGRATIONS = (
    ('default', 'Default'),
    ('social', 'Social'),
    ('management', 'Store Management'),
)

class Alert(models.Model):
    priority = models.IntegerField(choices=PRIORITIES)
    message = models.TextField()
    subject = models.CharField(max_length=300)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    sender = models.CharField(max_length=150, default='Vendor Bot')
    date = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=30, blank=True)
    cta_link = models.URLField(max_length=30, blank=True)
    unread = models.BooleanField(default=True)

    def mark_as_read(self):
        self.unread = False
        self.save()

    def __str__(self):
        return self.subject


# class Integration(models.Model):
#     type = models.CharField(max_length=20, choices=INTEGRATIONS)
#     social_link = models.ForeignObject('store.Social', blank=True, null=True, on_delete=models.CASCADE,
#     to_fields=['link'], from_fields=['social_link'] )
#     payment_link = models.ForeignObject('store.PaymentMethod', blank=True, null=True, on_delete=models.CASCADE,
#     to_fields=['gateway_link'], from_fields=['payment_link'] )
#     bots = models.ManyToManyField('Bot', blank=True)

class Bot(models.Model):
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=150)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)