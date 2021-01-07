from django.urls import path

from product.views.product_list_views   import ProductListView
from product.views.product_detail_views import ProductDetailView


urlpatterns = [
    path('/list', ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]

