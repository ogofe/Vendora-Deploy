# Generated by Django 2.2.14 on 2020-11-09 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20201107_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
