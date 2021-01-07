from django.test      import Client
from django.test      import TestCase

from product.models import Product, Category, CategoryGroupTop, CategoryGroupMedium, CategoryGroupBottom, Discount, ProductImage
from user.models import Host, HostGrade


class ProductListTest(TestCase):
    def tearDown(self):
        Product.objects.all().delete()
        ProductImage.objects.all().delete()
        Category.objects.all().delete()
        CategoryGroupBottom.objects.all().delete()
        CategoryGroupMedium.objects.all().delete()
        CategoryGroupTop.objects.all().delete()
        Host.objects.all().delete()
        Discount.objects.all().delete()


    def setUp(self):
        self.client = Client()

        category_group_top    = CategoryGroupTop.objects.create(name = '일상')
        category_group_medium = CategoryGroupMedium.objects.create(name = '액티비티' , category_group_top = category_group_top)
        category_group_bottom = CategoryGroupBottom.objects.create(name = '아웃도어', category_group_medium = category_group_medium)
        self.category         = Category.objects.create(name = '서핑', category_group_bottom = category_group_bottom)

        host_grade = HostGrade.objects.create(name="일반 판매자")

        Host(name = 'homer', host_grade = host_grade).save()
        Host(name = 'bart' , host_grade = host_grade).save()

        discount = Discount.objects.create(name = 10, percentage = 0.1)

        self.homer_surfing = Product.objects.create(
                                               name             = "homer surfing",
                                               subtitle         = "D'oh!",
                                               price            = 50000,
                                               activity_address = '스프링필드 에버그린 테라스 742',
                                               stock            = 100,
                                               discount         = discount,
                                               category         = Category.objects.get(name = '서핑'),
                                               host             = Host.objects.get(name     = 'homer'),
                                               )

        self.bart_surfing = Product.objects.create(
                                              name             = "bart surfing",
                                              subtitle         = "(Ay Caramba",
                                              price            = 100000,
                                              activity_address = '스프링필드 에버그린 테라스 742',
                                              stock            = 100,
                                              discount         = discount,
                                              category         = Category.objects.get(name = '서핑'),
                                              host             = Host.objects.get(name     = 'bart')
                                              )

        ProductImage(product = self.homer_surfing, image_url='homer_surfing_image_url').save()
        ProductImage(product = self.bart_surfing, image_url='bart_surfing_image_url').save()


    def test_product_list_get_success(self):
        print("test_product_list_get_success - starts")
        product_list_request = {
            'order'   : 'created_at',
            'category': self.category.id,
            'offset'  : '0',
            'limit'   : '2',
        }
        response = self.client.get('/product/list', product_list_request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE' : 'SUCCESS',
                             'product_list' : [
                                 {
                                     'id'                 : 1,
                                     'title'              : 'homer surfing',
                                     'subtitle'           : "D'oh!",
                                     'price'              : '50000.00',
                                     'discount_percentage': 0.1,
                                     'image_url'          : 'homer_surfing_image_url',
                                     'hit_count'          : 0,
                                     'star_rating'        : '0.0',
                                     'five_star_count'    : 0,
                                     'sales_rate'         : 0,
                                     'activity_address'   : '스프링필드 에버그린 테라스 742',
                                     'bookmark'           : False
                                 },
                                 {
                                     'id'                 : 2,
                                     'title'              : 'bart surfing',
                                     'subtitle'           : '(Ay Caramba',
                                     'price'              : '100000.00',
                                     'discount_percentage': 0.1,
                                     'image_url'          : 'bart_surfing_image_url',
                                     'hit_count'          : 0,
                                     'star_rating'        : '0.0',
                                     'five_star_count'    : 0,
                                     'sales_rate'         : 0,
                                     'activity_address'   : '스프링필드 에버그린 테라스 742',
                                     'bookmark'           : False
                                 }
                             ]
                         }
                         )

