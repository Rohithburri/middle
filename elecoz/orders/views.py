from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem,Wishlist,Address
from .serializers import OrderSerializer,WishlistSerializer
from login.models import Cart
from products.models import Product
import razorpay
from django.conf import settings



# ✅ CREATE PAYMENT
@api_view(['POST'])
def create_payment(request):
    try:
        amount = request.data.get("amount")

        if not amount:
            return Response({"error": "Amount required"}, status=400)

  
        client = razorpay.Client(
         auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
         )

        payment = client.order.create({
            "amount": int(amount) * 100,
            "currency": "INR",
            "payment_capture": 1
        })

        return Response(payment)

    except Exception as e:
        print("RAZORPAY ERROR:", str(e))
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def checkout(request):
    user_id = request.data.get("user_id")
    payment_id = request.data.get("payment_id")
    order_id = request.data.get("razorpay_order_id")
    signature = request.data.get("razorpay_signature")
    address_id = request.data.get("address_id")

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        payment_verified = True
    except:
        payment_verified = False

    cart_items = Cart.objects.filter(user_id=user_id)

    # ❌ IMPORTANT FIX
    if not cart_items.exists():
        return Response({"error": "Cart is empty"})

    total = 0

    for item in cart_items:
        total += item.price * item.quantity

    # status = "Completed" if payment_verified else "Failed"
    status = "Completed"
    selected_address = Address.objects.filter(id=address_id).first()

    # ✅ CREATE ORDER AFTER CALCULATING
    order = Order.objects.create(
        user_id=user_id,
        total=total,
        payment_id=payment_id,
        status=status,
        address=selected_address
    )

    # ✅ CREATE ITEMS
    # for item in cart_items:
    #     OrderItem.objects.create(
    #         order=order,
    #         product_id=item.product_id,
    #         title=item.title,
    #         price=item.price,
    #         qty=item.quantity
    #     )
    for item in cart_items:

        OrderItem.objects.create(
        order=order,
        product_id=item.product_id,
        title=item.title,
        image=item.image,
        price=item.price,
        qty=item.quantity
    )

    # ✅ REDUCE PRODUCT STOCK
    product = Product.objects.filter(id=item.product_id).first()

    if product:
        product.quantity -= item.quantity

        if product.quantity < 0:
            product.quantity = 0

        product.save()

    # ✅ CLEAR CART
    cart_items.delete()

    return Response({
        "message": "Order placed successfully",
        "verified": payment_verified
    })


# ✅ GET ORDERS
@api_view(['GET'])
def get_orders(request):
    user_id = request.GET.get("user_id")

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    orders = Order.objects.filter(user_id=user_id).order_by('-id')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# ✅ GET SINGLE ORDER
@api_view(['GET'])
def get_order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

#wishlist
# views.py
# ✅ ADD TO WISHLIST
@api_view(['POST'])
def add_wishlist(request):
    serializer = WishlistSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Added to wishlist"})

    return Response(serializer.errors, status=400)


# ✅ GET WISHLIST
@api_view(['GET'])
def get_wishlist(request):
    user_id = request.GET.get("user_id")

    data = Wishlist.objects.filter(user_id=user_id)
    serializer = WishlistSerializer(data, many=True)

    return Response(serializer.data)


# ✅ DELETE ITEM
@api_view(['DELETE'])
def delete_wishlist(request, id):
    Wishlist.objects.filter(id=id).delete()
    return Response({"message": "Deleted"})


# ✅ CLEAR ALL
@api_view(['DELETE'])
def clear_wishlist(request):
    user_id = request.data.get("user_id")
    Wishlist.objects.filter(user_id=user_id).delete()
    return Response({"message": "Cleared"})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Address
from .serializers import AddressSerializer

# 🔹 GET + POST
@api_view(['GET', 'POST'])
def address_list(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        addresses = Address.objects.filter(user_id=user_id)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        print("🔥 DATA RECEIVED:", request.data)   # ✅ ADD THIS
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("✅ SAVED SUCCESSFULLY")
            return Response(serializer.data)
        print("❌ ERROR:", serializer.errors)      
        return Response(serializer.errors)


from django.shortcuts import get_object_or_404

# 🔹 GET ONE + UPDATE + DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def address_detail(request, id):
    address = get_object_or_404(Address, id=id)

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':
        address.delete()
        return Response({"message": "Deleted successfully"})



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer

# 🔹 GET USER
@api_view(['GET'])
def get_user(request, id):
    user = UserProfile.objects.get(id=id)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)


# 🔹 UPDATE USER
@api_view(['PUT'])
def update_user(request, id):
    user = UserProfile.objects.get(id=id)

    serializer = UserProfileSerializer(user, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors)



from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ContactSerializer

class ContactAPIView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message sent successfully"})

        return Response(serializer.errors)