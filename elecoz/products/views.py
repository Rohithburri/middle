# from django.http import JsonResponse
# from .models import Product
# from django.core.paginator import Paginator
# from django.http import JsonResponse
# from .models import Product
# from django.http import JsonResponse
# from django.core.paginator import Paginator
# from .models import Product

# def get_products(request):
#     page = request.GET.get('page', 1)
#     category = request.GET.get('category')

#     products = Product.objects.all()

#     if category:
#         products = products.filter(category__name__icontains=category)

#     paginator = Paginator(products, 10)
#     page_obj = paginator.get_page(page)

#     data = []
#     for p in page_obj:
#         data.append({
#     "id": p.id,
#     "name": p.name,
#     "code": p.code or "",

#     "price": p.price,
#     "old_price": p.old_price,
#     "discount": p.discount,

#     "category": p.category.name,
#     "category_slug": p.category.name.lower().replace(" ", "-"),  # ✅ FIX

#     "image": p.image.url if p.image else "/media/products/mccb.webp",  # ✅ FIX

#     "ampere": p.ampere,
#     "poles": p.poles,
#     "breaking_capacity": p.breaking_capacity,
#     "setting_type": p.setting_type,

#     "selectors": [
#         p.ampere,
#         p.poles,
#         p.breaking_capacity,
#         p.setting_type
#     ]
# })

#     return JsonResponse({
#         "count": paginator.count,
#         "results": data
#     })
# from .models import Category


# def get_categories(request):
#     categories = Category.objects.all()

#     data = []
#     for c in categories:
#         data.append({
#             "id": c.id,
#             "name": c.name,
#             "slug": c.name.lower().replace(" ", "-"),
#             "image": c.image.url if c.image else None,   # ✅ ADD THIS
#         })

#     return JsonResponse(data, safe=False)


# import pandas as pd
# import os
# from django.core.files import File
# from django.http import JsonResponse
# from .models import Product, Category, Brand

# from django.conf import settings
# def import_products(request):
    
#     file_path = os.path.join(settings.BASE_DIR, "products.xlsx")
#     df = pd.read_excel(file_path)

#     for _, row in df.iterrows():

#         code = str(row.get("code", "")).strip()
#          # 🔴 skip invalid
#         if not code:
#             continue

#         # ✅ CATEGORY
#         category_name = str(row.get("category", "")).strip()
#         category = Category.objects.filter(name=category_name).first()
#         if not category:
#             category = Category.objects.create(name=category_name)

#         # ✅ BRAND
#         brand_name = str(row.get("brand", "")).strip()
#         brand = Brand.objects.filter(name=brand_name).first()
#         if not brand:
#             brand = Brand.objects.create(name=brand_name)

#         # 🔥 UPDATE OR CREATE
#         product, created = Product.objects.update_or_create(
#             code=code,   # 🔑 unique field
#             defaults={
#                 "name": row.get("name"),
#                 "price": row.get("price"),
#                 "old_price": row.get("old_price"),
#                 "discount": row.get("discount"),
#                 "ampere": row.get("ampere"),
#                 "poles": row.get("poles"),
#                 "breaking_capacity": row.get("breaking_capacity"),
#                 "setting_type": row.get("setting_type"),
#                 "category": category,
#                 "brand": brand
#             }
#         )

#         # ✅ IMAGE UPDATE
#         img1 = row.get("image1")
#         if img1:
#             product.image = f"products/{img1}"
#             product.save(update_fields=["image"])

#     return JsonResponse({"message": "Products Imported (Updated + Created) Successfully"})


# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Product
# from .serializers import ProductSerializer

# @api_view(['GET'])
# def get_single_product(request, id):
#     try:
#         product = Product.objects.get(id=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         return Response({"error": "Product not found"})


# from rest_framework.views import APIView
# from .models import Brand
# from .serializers import BrandSerializer


# class BrandAPIView(APIView):
#     def get(self, request):
#         brands = Brand.objects.all()
#         serializer = BrandSerializer(brands, many=True)
#         return Response(serializer.data)

# @api_view(['GET'])
# def top_deals(request):
#     products = Product.objects.all().order_by('-id')[:10]  # latest 10

#     data = []
#     for p in products:
#         data.append({
#             "id": p.id,
#             "title": p.name,
#             "price": p.price,
#             "image": p.image.url if p.image else "/media/products/mccb.webp",
#             "brand": p.brand.name if p.brand else "",
#         })

#     return Response(data)




from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.text import slugify
from .models import Product, Category, Brand

import pandas as pd
import os


# =========================
# ✅ GET PRODUCTS API
# =========================
def get_products(request):
    page = request.GET.get('page', 1)
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    search = request.GET.get('search')
    print("CATEGORY:", category)

    # products = Product.objects.all()
    products = Product.objects.all().order_by('-id')
    # CATEGORY FILTER
    if category and category != "all":
        products = products.filter(category__name__iexact=category)

# BRAND FILTER
    if brand:
       products = products.filter(brand__name__iexact=brand.strip())
    # SEARCH FILTER
    if search:
        products = products.filter(
        name__icontains=search
        )

    # if category:
    #     products = products.filter(category__name__icontains=category)
   


    #      products = [
    #     p for p in products
    #     if slugify(p.category.name) == category
    #    ]
    # if brand:
    #     products = products.filter(brand__name__icontains=brand)

  

    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page)

    data = []
    for p in page_obj:
        data.append({
            "id": p.id,
            "name": p.name,
            "code": p.code or "",

            "price": p.price,
            "old_price": p.old_price,
            "discount": p.discount,

            "category": p.category.name,
            "category_slug": p.category.name.lower().replace(" ", "-"),
              # ✅ ADD THIS LINE
            "brand": p.brand.name if p.brand else "",

            # ✅ IMAGE FIX
            "image": "/media/" + str(p.image) if p.image else "/media/products/mccb.webp",
            "image2": "/media/" + str(p.image2) if p.image2 else "/media/products/mccb.webp",

            "ampere": p.ampere,
            "poles": p.poles,
            "breaking_capacity": p.breaking_capacity,
            "setting_type": p.setting_type,
            "auxiliary_contact": p.auxiliary_contact,
            "coil_voltage": p.coil_voltage,
            "duty": p.duty,
            "stock_status": p.stock_status,
            "dispatch_date": p.dispatch_date,
            "warehouse": p.warehouse,
          

            "selectors": [
                p.ampere,
                p.poles,
                p.breaking_capacity,
                p.setting_type
            ]
        })

    return JsonResponse({
        "count": paginator.count,
        "results": data
    })


# =========================
# ✅ GET CATEGORIES
# =========================
def get_categories(request):
    categories = Category.objects.all()

    data = []
    for c in categories:
        data.append({
            "id": c.id,
            "name": c.name,
            "slug": c.name.lower().replace(" ", "-"),
            "image": "/media/" + str(c.image) if c.image else None,
        })

    return JsonResponse(data, safe=False)


# =========================
# ✅ IMPORT PRODUCTS (EXCEL)
# =========================
def import_products(request):

    file_path = os.path.join(settings.BASE_DIR, "products.xlsx")
    df = pd.read_excel(file_path)

    for _, row in df.iterrows():

        code = str(row.get("code", "")).strip()
        if not code:
            continue

        # CATEGORY
        category_name = str(row.get("category", "")).strip()
        category, _ = Category.objects.get_or_create(name=category_name)

        # BRAND
        brand_name = str(row.get("brand", "")).strip()
        brand, _ = Brand.objects.get_or_create(name=brand_name)

        # CREATE OR UPDATE PRODUCT
        product, created = Product.objects.update_or_create(
            code=code,
            defaults={
                "name": row.get("name"),
                "price": row.get("price"),
                "old_price": row.get("old_price"),
                "discount": row.get("discount"),
                "ampere": row.get("ampere"),
                "poles": row.get("poles"),
                "breaking_capacity": row.get("breaking_capacity"),
                "setting_type": row.get("setting_type"),

                "auxiliary_contact": row.get("auxiliary_contact"),
                "coil_voltage": row.get("coil_voltage"),
                "duty": row.get("duty"),
                "stock_status": row.get("stock_status"),
                "dispatch_date": row.get("dispatch_date"),
                "warehouse": row.get("warehouse"),
                # "gst_price": None if pd.isna(row.get("gst_price")) else row.get("gst_price"),

                "category": category,
                "brand": brand
            }
        )

        # ✅ IMAGE 1
        img1 = str(row.get("image1") or "").strip()
        if img1:
            product.image = img1

        # ✅ IMAGE 2
        img2 = str(row.get("image2") or "").strip()
        if img2:
            product.image2 = img2

        product.save()

    return JsonResponse({"message": "✅ Products Imported Successfully"})


# =========================
# ✅ SINGLE PRODUCT
# =========================
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer

@api_view(['GET'])
def get_single_product(request, id):
    try:
        product = Product.objects.get(id=id)
        # serializer = ProductSerializer(product)
        serializer = ProductSerializer(
    product,
    context={'request': request}
)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"})


# =========================
# ✅ BRAND API
# =========================
from rest_framework.views import APIView
from .serializers import BrandSerializer

class BrandAPIView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)


# =========================
# ✅ TOP DEALS
# =========================
@api_view(['GET'])
def top_deals(request):
    products = Product.objects.all().order_by('-id')[:10]

    data = []
    for p in products:
        data.append({
            "id": p.id,
            "title": p.name,
            "price": p.price,
            "image": "/media/" + str(p.image) if p.image else "/media/products/mccb.webp",
            "brand": p.brand.name if p.brand else "",
            
        })

    return Response(data)


# ✅ FEATURED PRODUCTS API
@api_view(['GET'])
def featured_products(request):
    products = Product.objects.all().order_by('-id')[:20]

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)