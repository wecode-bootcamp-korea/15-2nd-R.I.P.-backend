from django.test      import Client
from django.test      import TestCase

from product.models import Product, Category, CategoryGroupTop, CategoryGroupMedium, CategoryGroupBottom, Discount, ProductImage
from user.models import Host, HostGrade

class ProductDetailTest(TestCase):
    def setUp(self):
        self.client = Client()

        category_group_top    = CategoryGroupTop.objects.create(name = '일상')
        category_group_medium = CategoryGroupMedium.objects.create(name = '액티비티' , category_group_top = category_group_top)
        category_group_bottom = CategoryGroupBottom.objects.create(name = '아웃도어', category_group_medium = category_group_medium)
        category              = Category.objects.create(name = '서핑', category_group_bottom = category_group_bottom)

        host_grade = HostGrade.objects.create(name="일반 판매자")

        Host(name = 'homer', host_grade = host_grade).save()
        Host(name = 'bart' , host_grade = host_grade).save()

        discount = Discount.objects.create(name = 10, percentage = 0.1)

        homer_surfing = Product.objects.create(name = "homer surfing",
                subtitle         = "D'oh!",
                price            = 50000,
                activity_address = '스프링필드 에버그린 테라스 742',
                stock            = 100,
                discount         = discount,
                category         = Category.objects.get(name = '서핑'),
                host             = Host.objects.get(name     = 'homer'),
                )

        bart_surfing = Product.objects.create(name = "bart surfing",
                subtitle         = "(Ay Caramba",
                price            = 100000,
                activity_address = '스프링필드 에버그린 테라스 742',
                stock            = 100,
                discount         = discount,
                category         = Category.objects.get(name = '서핑'),
                host             = Host.objects.get(name     = 'bart')
                )

        ProductImage(product = homer_surfing, image_url='homer_surfing_image_url').save()
        ProductImage(product = bart_surfing, image_url='bart_surfing_image_url').save()

    def test_product_detail_get_success(self):
        response = self.client.get('/product/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE'       : 'SUCCESS',
                             'product_detail': {
                                 'id'                 : 1,
                                 'title'              : 'homer surfing',
                                 'subtitle'           : "D'oh!",
                                 'price'              : '50000.00',
                                 'discount_percentage': 0.1,
                                 'image_urls'         : [
                                     {
                                         'id'       : 1,
                                         'image_url': 'homer_surfing_image_url'
                                     }
                                 ],
                                 'hit_count'          : 1,
                                 'star_rating'        : '0.0',
                                 'five_star_count'    : 0,
                                 'sales_rate'         : 0,
                                 'activity_address'   : '스프링필드 에버그린 테라스 742',
                                 'bookmark'           : False,
                                 'host'               : {
                                     'id'          : 1,
                                     'host_name'   : 'homer',
                                     'frip_count'  : 1,
                                     'review_count': 0,
                                     'bookmark'    : 0
                                 }
                             }
                         }
        )
