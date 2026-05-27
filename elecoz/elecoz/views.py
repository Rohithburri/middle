import requests
from django.http import JsonResponse

def get_pincode(request, pincode):
    try:
        url = f"https://api.postalpincode.in/pincode/{pincode}"

        response = requests.get(url)
        data = response.json()

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({
            "Status": "Error",
            "Message": str(e)
        }, status=500)