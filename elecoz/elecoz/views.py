import requests
import urllib3
from django.http import JsonResponse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_pincode(request, pincode):
    try:
        url = f"https://api.postalpincode.in/pincode/{pincode}"

        response = requests.get(
            url,
            timeout=15,
            verify=False,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )

        return JsonResponse(response.json(), safe=False)

    except requests.exceptions.SSLError as e:
        return JsonResponse({
            "Status": "Error",
            "Message": "SSL error",
            "Details": str(e)
        }, status=500)

    except requests.exceptions.Timeout:
        return JsonResponse({
            "Status": "Error",
            "Message": "Postal API timeout"
        }, status=500)

    except Exception as e:
        return JsonResponse({
            "Status": "Error",
            "Message": str(e)
        }, status=500)