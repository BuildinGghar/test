# Generated by Django 4.2.3 on 2023-08-05 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='payment_status',
            field=models.CharField(default='Paid', max_length=200),
        ),
    ]
