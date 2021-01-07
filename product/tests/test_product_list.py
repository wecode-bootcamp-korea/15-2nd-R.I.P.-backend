from django.test      import Client
from django.test      import TestCase

from product.models import Product, Category, CategoryGroupTop, CategoryGroupMedium, CategoryGroupBottom, Discount, ProductImage, Option
from user.models    import Host, HostGrade


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



class ProductListTest(TestCase):
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

        self.homer_surfing = Product.objects.create(name = "homer surfing",
                subtitle         = "D'oh!",
                price            = 50000,
                activity_address = '스프링필드 에버그린 테라스 742',
                stock            = 100,
                discount         = discount,
                category         = Category.objects.get(name = '서핑'),
                host             = Host.objects.get(name     = 'homer'),
                )

        self.bart_surfing = Product.objects.create(name = "bart surfing",
                subtitle         = "(Ay Caramba",
                price            = 100000,
                activity_address = '스프링필드 에버그린 테라스 742',
                stock            = 100,
                discount         = discount,
                category         = Category.objects.get(name = '서핑'),
                host             = Host.objects.get(name     = 'bart')
                )


    def test_product_list_get_success(self):
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

    def test_product_option_get_success(self):
        Option(
            start_date = '2021-01-10',
            end_date   = '2021-01-20',
            due_date   = '2021-01-19',
            headcount  = 10,
            capacity   = 20,
            quantity   = 100,
            product    = self.homer_surfing,
        ).save()

        product_id = self.homer_surfing.id
        response = self.client.get(f'/product/{product_id}/option')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             'MESSAGE'       : 'SUCCESS',
                             'product_option': [
                                 {
                                     'id'        : 1,
                                     'start_date': '2021-01-10',
                                     'end_date'  : '2021-01-20',
                                     'due_date'  : '2021-01-19',
                                     'headcount' : 10,
                                     'capacity'  : 20
                                 }
                             ]
                         }
                        )
