from django.http        import JsonResponse
from django.views       import View

from product.models import Product, Option


class ProductOptionView(View):
    def get(self, request, product_id):
        try:
            options = Option.objects.filter(product_id=product_id)

            product_option = [{
                'id'         : option.id,
                'start_date' : option.start_date,
                'end_date'   : option.end_date,
                'due_date'   : option.due_date,
                'headcount'  : option.headcount,
                'capacity'   : option.capacity,
            } for option in options]

            return JsonResponse({'MESSAGE': 'SUCCESS', 'product_option': product_option}, status = 200)

        except Product.DoesNotExist as e:
            return JsonResponse({'MESSAGE': 'PRODUCT_NOT_FOUND => ' + e.args[0]}, status=400)
        except ValueError as e:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR => ' + e.args[0]}, status=400)



