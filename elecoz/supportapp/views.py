from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SupportTicket
from .serializers import SupportSerializer

@api_view(['POST'])
def create_support(request):
    serializer = SupportSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Ticket created successfully"})
    return Response(serializer.errors)