from django.urls import path
from .views import add_enquiry, get_enquiries, delete_enquiry, clear_enquiries,submit_enquiry

urlpatterns = [
    path('enquiry/', add_enquiry),                    # POST
    path('enquiries/', get_enquiries),                # GET
    path('enquiry/<int:id>/', delete_enquiry),        # DELETE single
    path('enquiries/clear/', clear_enquiries),        # DELETE all
     path('submit-enquiry/', submit_enquiry), #enqury submitting
]