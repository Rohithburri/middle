from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Enquiry
from .serializers import EnquirySerializer


# ✅ ADD ENQUIRY
@api_view(['POST'])
def add_enquiry(request):
    serializer = EnquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Enquiry added successfully"})
    return Response(serializer.errors, status=400)


# ✅ GET ALL ENQUIRIES
@api_view(['GET'])
def get_enquiries(request):
    user_id = request.GET.get("user_id")

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    enquiries = Enquiry.objects.filter(user_id=user_id).order_by('-id')
    serializer = EnquirySerializer(enquiries, many=True)

    return Response(serializer.data)


# ✅ DELETE SINGLE ENQUIRY
@api_view(['DELETE'])
def delete_enquiry(request, id):
    try:
        enquiry = Enquiry.objects.get(id=id)
        enquiry.delete()
        return Response({"message": "Deleted successfully"})
    except Enquiry.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


# ✅ CLEAR ALL ENQUIRIES
@api_view(['DELETE'])
def clear_enquiries(request):
    user_id = request.data.get("user_id")

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    Enquiry.objects.filter(user_id=user_id).delete()
    return Response({"message": "All enquiries cleared"})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Enquiry

# @api_view(['POST'])
# def submit_enquiry(request):
#     user_id = request.data.get("user_id")

#     if not user_id:
#         return Response({"error": "user_id required"}, status=400)

#     enquiries = Enquiry.objects.filter(user_id=user_id)

#     # ✅ update status
#     enquiries.update(status="Submitted")

#     return Response({"message": "Enquiry submitted successfully"})
import json

@api_view(['POST'])
def submit_enquiry(request):
    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
    except:
        user_id = None

    print("USER ID RECEIVED:", user_id)

    if not user_id:
        return Response({"error": "user_id required"}, status=400)

    Enquiry.objects.filter(user_id=user_id).update(status="Submitted")

    return Response({"message": "Submitted"})