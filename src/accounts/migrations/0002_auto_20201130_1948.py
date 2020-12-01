# Generated by Django 2.2.14 on 2020-11-30 19:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='stores',
            field=models.ManyToManyField(blank=True, to='store.Store'),
        ),
        migrations.AddField(
            model_name='merchant',
            name='tokens',
            field=models.ManyToManyField(blank=True, related_name='tokens', to='accounts.Token'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]