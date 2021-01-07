from django.urls import path

from product.views.product_list_views import ProductListView


urlpatterns = [
    path('/list', ProductListView.as_view()),
]
