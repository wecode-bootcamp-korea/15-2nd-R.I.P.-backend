# Generated by Django 3.1.4 on 2020-12-30 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
