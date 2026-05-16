# from django.urls import path
# from .views import register_user, login_user, b2b_request

# urlpatterns = [
#     path('register/', register_user),
#     path('login/', login_user),
#      path('b2b/', b2b_request), 
   
# ]

from django.urls import path
from .views import register_user, login_user, b2b_request, get_b2b_status,add_to_cart,get_cart,update_cart,delete_cart,clear_cart

urlpatterns = [
    path('register/', register_user),
    path('login/', login_user),
    path('b2b/', b2b_request),
    path('b2b-status/', get_b2b_status),  # ✅ ADD THIS
    path('cart/', add_to_cart),
    
    path('cart-items/', get_cart), # get all product
    path('update-cart/<int:id>/', update_cart), #update card
    path('delete-cart/<int:id>/', delete_cart), #delete card
    path('clear-cart/', clear_cart), #clear the card item from the backend also 
]