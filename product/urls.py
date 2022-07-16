from django.urls import path
from .views import *

urlpatterns = [
    path("upload_csv", UploadCSV.as_view(), name="upload csv file"),
    path("search_data", SearchData.as_view(), name="seach_product_deatils")
]
