from django.urls import path
from .views import get_products, get_categories ,import_products,get_single_product,BrandAPIView ,top_deals ,featured_products # ✅ ADD THIS

urlpatterns = [
    path('products/', get_products),
    path('categories/', get_categories),
    path('products/<int:id>/', get_single_product),   # ✅ ADD THIS LINE
    path('import/', import_products),   # ✅ ADD THIS
        # ✅ ADD THIS
    path('brands/', BrandAPIView.as_view()),
    path("top-deals/", top_deals),
    path("featured-products/", featured_products),
    


]