from django.http        import JsonResponse
from django.views       import View

from product.models import Product
from board.models   import Review
from user.models    import HostWishList


class ProductDetailView(View):
    def get(self, request, product_id):
        try:

            product = Product.objects.select_related('discount', 'host').prefetch_related('productimage_set').get(id = product_id)

            product.hit_count += 1
            product.save()

            review_count = Review.objects.filter(product__host_id = product.host.id).count()

            product_detail = {
                'id'                  : product.id,
                'title'               : product.name,
                'subtitle'            : product.subtitle,
                'price'               : product.price,
                'discount_percentage' : product.discount.percentage,
                'image_urls'          : [{
                    'id' : image.id,
                    'image_url' : image.image_url
                    }for image in product.productimage_set.all()],
                'hit_count'           : product.hit_count,
                'star_rating'         : product.star_rating,
                'five_star_count'     : product.five_star_count,
                'sales_rate'          : product.sales_rate,
                'activity_address'    : product.activity_address,
                'bookmark'            : False,
                'host'                : {
                    'id' : product.host.id,
                    'host_name': product.host.name,
                    'frip_count' : Product.objects.filter(host_id=product.host.id).count(),
                    'review_count' : review_count,
                    'bookmark' : HostWishList.objects.filter(host_id=product.host.id).count(),
                }
            }

            return JsonResponse({'MESSAGE': 'SUCCESS', 'product_detail': product_detail}, status = 200)

        except Product.DoesNotExist as e:
            return JsonResponse({'MESSAGE': 'PRODUCT_NOT_FOUND => ' + e.args[0]}, status=400)
        except ValueError as e:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR => ' + e.args[0]}, status=400)



