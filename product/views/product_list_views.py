from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from product.models import Product


class ProductListView(View):
    def get(self, request):
        try:
            offset             = int(request.GET.get('offset', 0))
            limit              = int(request.GET.get('limit' , 4))
            order              = request.GET.get('order')
            category_id        = request.GET.get('category', None)
            medium_category_id = request.GET.get('medium_category', None)
            search_keyword     = request.GET.get('search_keyword', None)

            if category_id:
                products = Product.objects.filter(category = category_id).select_related('discount').prefetch_related('productimage_set').order_by(order)
            elif medium_category_id:
                products = Product.objects.filter(category__category_group_bottom__category_group_medium_id = medium_category_id).select_related('discount').prefetch_related('productimage_set').order_by(order)
            elif search_keyword:
                products = Product.objects.all().select_related('discount').prefetch_related('productimage_set').order_by(order)
                products = products.filter(
                    Q(name__icontains    = search_keyword) |
                    Q(subtitle__icontains = search_keyword)
                ).distinct()
            else:
                products = Product.objects.all().select_related('discount').prefetch_related('productimage_set').order_by(order)

            product_list = [{
                'id'                  : product.id,
                'title'               : product.name,
                'subtitle'            : product.subtitle,
                'price'               : product.price,
                'discount_percentage' : product.discount.percentage,
                'image_url'           : product.productimage_set.all()[0].image_url,
                'hit_count'           : product.hit_count,
                'star_rating'         : product.star_rating,
                'five_star_count'     : product.five_star_count,
                'sales_rate'          : product.sales_rate,
                'activity_address'    : product.activity_address,
                'bookmark'            : False,
            } for product in products[offset:limit]]

            return JsonResponse({'MESSAGE': 'SUCCESS', 'product_list': product_list}, status = 200)

        except Product.DoesNotExist as e:
            return JsonResponse({'MESSAGE': 'PRODUCT_NOT_FOUND => ' + e.args[0]}, status=400)
        except ValueError as e:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR => ' + e.args[0]}, status=400)
        except Exception as e:
            return JsonResponse({'MESSAGE': 'Exception => ' + e.args[0]}, status=400)
