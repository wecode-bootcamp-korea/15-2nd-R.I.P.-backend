# Generated by Django 3.1.4 on 2020-12-30 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20201231_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.URLField(max_length=2000, null=True),
        ),
    ]
