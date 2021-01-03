from django.db import models

from rip.core import TimeStampModel


class Authentication(TimeStampModel):
    phone_number      = models.CharField(max_length = 11)
    sms_number        = models.IntegerField(null = True)
    sms_request_count = models.IntegerField(default = 0)
    try_count         = models.IntegerField(default = 0)
    is_authenticated  = models.BooleanField(default = False)

    class Meta:
        db_table = 'authentications'


class HostGrade(models.Model):
    name = models.CharField(max_length = 45)

    class Meta :
        db_table = 'host_grades'


class Host(models.Model):
    name       = models.CharField(max_length = 45)
    host_grade = models.ForeignKey(HostGrade, on_delete = models.PROTECT)
    introduce  = models.CharField(max_length= 300)

    class Meta :
        db_table = 'hosts'


class AccountType(models.Model):
    name = models.CharField(max_length = 45)

    class Meta :
        db_table = 'account_types'


class Coupon(models.Model):
    name           = models.CharField(max_length = 100)
    discount_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    expired_date   = models.DateField(null = True)

    class Meta:
        db_table = 'coupons'


class UserCoupon(models.Model):
    user   = models.ForeignKey('User', on_delete = models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'user_coupons'


class ProductWishList(models.Model):
    user    = models.ForeignKey('User', on_delete = models.PROTECT)
    product = models.ForeignKey('product.Product', on_delete = models.PROTECT)

    class Meta:
        db_table = 'product_wish_lists'


class HostWishList(models.Model):
    user = models.ForeignKey('User', on_delete = models.PROTECT)
    host = models.ForeignKey('Host', on_delete = models.PROTECT)

    class Meta:
        db_table = 'host_wish_lists'


class User(TimeStampModel):
    email             = models.EmailField(unique = True)
    social_login_id   = models.CharField(max_length = 20, null = True)
    nickname          = models.CharField(max_length = 20)
    account_type      = models.ForeignKey(AccountType, on_delete = models.PROTECT)
    password          = models.CharField(max_length = 2000, null = True)
    phone_number      = models.CharField(max_length = 11, null = True)
    profile_image     = models.URLField(max_length = 2000, null = True)
    mileage           = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0)
    coupon            = models.ManyToManyField(Coupon, through = UserCoupon, related_name = 'user_coupon_set')
    product_wish_list = models.ManyToManyField('product.Product', through = ProductWishList, related_name='product_wish_list_set')
    host_wish_list    = models.ManyToManyField('Host', through = HostWishList, related_name = 'host_wish_list_set')

    class Meta:
        db_table = 'users'
