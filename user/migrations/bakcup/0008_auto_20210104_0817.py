# Generated by Django 3.1.4 on 2021-01-03 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20201231_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='social_login_id',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, null=True),
        ),
    ]