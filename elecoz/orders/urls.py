from django.urls import path
from .views import checkout, get_orders, get_order_detail, create_payment,add_wishlist, get_wishlist, delete_wishlist, clear_wishlist,address_list,address_detail,get_user,update_user, ContactAPIView


urlpatterns = [
    path('checkout/', checkout),
    path('orders/', get_orders),
    path('order/<int:order_id>/', get_order_detail),
    path('create-payment/', create_payment),
    path('wishlist/', get_wishlist),
    path('wishlist/add/', add_wishlist),
    path('wishlist/<int:id>/', delete_wishlist),
    path('wishlist/clear/', clear_wishlist),
     path('addresses/', address_list),
     path('addresses/<int:id>/', address_detail),
     path('user/<int:id>/', get_user),
    path('update-user/<int:id>/', update_user),
      path("contact/", ContactAPIView.as_view()),
]    