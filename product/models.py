from django.db import models

from rip.core import TimeStampModel


class CategoryTop(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'category_tops'


class CategoryMedium(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'category_mediums'


class CategoryBottom(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'category_bottoms'


class ProductType(models.Model):
    name = models.CharField(max_length = 45)

    class Meta:
        db_table = 'product_types'


class Discount(models.Model):
    name       = models.CharField(max_length = 200)
    percentage = models.FloatField()

    class Meta:
        db_table = 'discounts'


class Product(TimeStampModel):
    name              = models.CharField(max_length = 200)
    subtitle          = models.CharField(max_length = 500)
    price             = models.DecimalField(max_digits = 10, decimal_places = 2)
    discount          = models.ForeignKey(Discount, on_delete = models.PROTECT, null = True)
    host              = models.ForeignKey('user.Host', on_delete = models.PROTECT)
    star_rating       = models.DecimalField(max_digits = 2, decimal_places = 1)
    five_star_count   = models.IntegerField()
    sales_rate        = models.IntegerField()
    activity_address  = models.CharField(max_length = 300)
    gathering_address = models.CharField(max_length = 300)
    stock             = models.IntegerField()
    category_top      = models.ForeignKey(CategoryTop   , on_delete = models.PROTECT)
    category_medium   = models.ForeignKey(CategoryMedium, on_delete = models.PROTECT)
    category_bottom   = models.ForeignKey(CategoryBottom, on_delete = models.PROTECT)
    hit_count         = models.IntegerField(default = 0)

    class Meta :
        db_table = 'products'


class ProductImage(models.Model):
    product   = models.ForeignKey(Product, on_delete = models.CASCADE)
    image_url = models.URLField(max_length = 2000)

    class Meta :
        db_table = 'product_images'


class Option(models.Model):
    product    = models.ForeignKey(Product, on_delete = models.CASCADE)
    name       = models.CharField(max_length = 200)
    start_date = models.DateField()
    end_date   = models.DateField()
    due_date   = models.DateField()
    headcount  = models.IntegerField(default = 1)
    capacity   = models.IntegerField(default = 1)
    quantity   = models.IntegerField(default = 1)

    class Meta :
        db_table = 'options'
