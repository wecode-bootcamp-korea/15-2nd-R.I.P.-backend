
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_name', models.CharField(max_length=45)),
                ('address', models.CharField(max_length=300)),
                ('phone_number', models.CharField(max_length=11)),
                ('delivery_message', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'order_details',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'order_status',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'payment_method',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.orderdetail')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.paymentmethod')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.orderstatus')),
            ],
            options={
                'db_table': 'orders',
            },
        ),
    ]
