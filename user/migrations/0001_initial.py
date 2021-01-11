
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'account_types',
            },
        ),
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(max_length=11)),
                ('sms_number', models.IntegerField(null=True)),
                ('sms_request_count', models.IntegerField(default=0)),
                ('try_count', models.IntegerField(default=0)),
                ('is_authenticated', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'authentications',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expired_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'coupons',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('introduce', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'hosts',
            },
        ),
        migrations.CreateModel(
            name='HostGrade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'host_grades',
            },
        ),
        migrations.CreateModel(
            name='HostWishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.host')),
            ],
            options={
                'db_table': 'host_wish_lists',
            },
        ),
        migrations.CreateModel(
            name='ProductWishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
            ],
            options={
                'db_table': 'product_wish_lists',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('social_login_id', models.CharField(max_length=20, null=True)),
                ('nickname', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=2000, null=True)),
                ('phone_number', models.CharField(max_length=11, null=True)),
                ('profile_image', models.URLField(max_length=2000, null=True)),
                ('mileage', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.accounttype')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'user_coupons',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='coupon',
            field=models.ManyToManyField(related_name='user_coupon_set', through='user.UserCoupon', to='user.Coupon'),
        ),
        migrations.AddField(
            model_name='user',
            name='host_wish_list',
            field=models.ManyToManyField(related_name='host_wish_list_set', through='user.HostWishList', to='user.Host'),
        ),
        migrations.AddField(
            model_name='user',
            name='product_wish_list',
            field=models.ManyToManyField(related_name='product_wish_list_set', through='user.ProductWishList', to='product.Product'),
        ),
        migrations.AddField(
            model_name='productwishlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.user'),
        ),
        migrations.AddField(
            model_name='hostwishlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.user'),
        ),
        migrations.AddField(
            model_name='host',
            name='host_grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.hostgrade'),
        ),
    ]
