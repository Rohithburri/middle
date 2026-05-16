# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import User
# from .serializers import UserSerializer

# # ✅ REGISTER API
# @api_view(['POST'])
# def register_user(request):
#     email = request.data.get('email')

#     # check user already exists
#     if User.objects.filter(email=email).exists():
#         return Response({"error": "User already exists"}, status=400)

#     serializer = UserSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response({
#             "message": "User registered successfully",
#             "user": serializer.data
#         })

#     return Response(serializer.errors, status=400)


# # ✅ LOGIN API
# @api_view(['POST'])
# def login_user(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     try:
#         user = User.objects.get(email=email, password=password)

#         serializer = UserSerializer(user)

#         return Response({
#             "message": "Login success",
#             "user": serializer.data
#         })

#     except User.DoesNotExist:
#         return Response({"error": "Invalid credentials"}, status=400)




# from django.contrib.auth.models import User
# from .models import B2BRequest
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# @api_view(['POST'])
# def b2b_request(request):

#     user_id = request.data.get("user_id")
#     print("USER ID:", user_id)

#     user = None
#     if user_id:
#         user = User.objects.filter(id=user_id).first()

#     B2BRequest.objects.create(
#         user=user,
#         company_name=request.data.get("companyName"),
#         gst_number=request.data.get("gst"),
#         industry=request.data.get("industry"),
#     )

#     return Response({"message": "B2B request submitted"})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, B2BRequest
from .serializers import UserSerializer

# REGISTER
@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')

    if User.objects.filter(email=email).exists():
        return Response({"error": "User already exists"}, status=400)

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "User registered successfully",
            "user": serializer.data
        })

    return Response(serializer.errors, status=400)


# LOGIN
@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email, password=password)
        serializer = UserSerializer(user)

        return Response({
            "message": "Login success",
            "user": serializer.data
        })

    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=400)


# B2B
@api_view(['POST'])
def b2b_request(request):

    user_id = request.data.get("user_id")
    print("USER ID:", user_id)

    user = None
    if user_id:
        user = User.objects.filter(id=user_id).first()

    B2BRequest.objects.create(
        user=user,
        company_name=request.data.get("companyName"),
        gst_number=request.data.get("gst"),
        industry=request.data.get("industry"),
    )

    return Response({"message": "B2B request submitted"})



@api_view(['GET'])
def get_b2b_status(request):
    user_id = request.GET.get("user_id")

    print("STATUS CHECK USER:", user_id)  # debug

    b2b = B2BRequest.objects.filter(user_id=user_id).first()

    if b2b:
        return Response({
            "status": b2b.status
        })
    else:
        return Response({
            "status": "not_applied"
        })



from .models import Cart, User
from rest_framework.decorators import api_view
from rest_framework.response import Response

# @api_view(['POST'])
# def add_to_cart(request):
#     user_id = request.data.get("user_id")

#     user = User.objects.filter(id=user_id).first()

#     if not user:
#         return Response({"error": "User not found"}, status=400)

#     Cart.objects.create(
#         user=user,
#         product_id=request.data.get("id"),
#         title=request.data.get("title"),
#         price=request.data.get("price"),
#         quantity=request.data.get("qty"),
#     )

#     return Response({"message": "Item added"})




@api_view(['POST'])
def add_to_cart(request):
    user_id = request.data.get("user_id")
    # product_id = request.data.get("id")
    # qty = int(request.data.get("qty", 1))
    product_id = request.data.get("product_id")   # ✅ FIX
    qty = int(request.data.get("quantity", 1))    # ✅ FIX


    user = User.objects.filter(id=user_id).first()

    if not user:
        return Response({"error": "User not found"}, status=400)

    existing = Cart.objects.filter(user=user, product_id=product_id).first()

    if existing:
        existing.quantity += qty
        existing.save()
        return Response({"message": "Quantity updated", "qty": existing.quantity})

    Cart.objects.create(
        user=user,
        product_id=product_id,
        title=request.data.get("title"),
        image=request.data.get("image"),
        price=request.data.get("price"),
        quantity=qty,
    )

    return Response({"message": "Item added"})

@api_view(['GET'])
def get_cart(request):
    user_id = request.GET.get("user_id")

    items = Cart.objects.filter(user_id=user_id)

    data = []
    for item in items:
        data.append({
            "id": item.id,              # ✅ unique
            "product_id": item.product_id,
            "title": item.title,
            "image": item.image,
            "price": item.price,
            "qty": item.quantity,
        })

    return Response(data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart

@api_view(['PUT'])
def update_cart(request, id):
    try:
        item = Cart.objects.get(id=id)
        qty = int(request.data.get("qty", 1))

        item.quantity = qty
        # item.qty = qty
        item.save()

        return Response({"message": "Quantity updated"})
    except Cart.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

@api_view(['DELETE'])
def delete_cart(request, id):
    try:
        item = Cart.objects.get(id=id)
        item.delete()
        return Response({"message": "Deleted"})
    except Cart.DoesNotExist:
        return Response({"error": "Not found"}, status=404)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart

@api_view(['DELETE'])
def clear_cart(request):
    user_id = request.GET.get("user_id")

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    Cart.objects.filter(user_id=user_id).delete()

    return Response({"message": "Cart cleared"})