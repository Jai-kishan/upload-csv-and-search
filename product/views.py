from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.

from product.operation_helper import OperationHelper
from product.response_helper import ResponseHelper

OperationHelper = OperationHelper()
Response = ResponseHelper()


class UploadCSV(APIView):
    def post(self,request):
        data = request.data
        
        mandatory_request_data = [
            "file_url"
        ]
        
        request_data_validation = OperationHelper.validate_request_body(data, mandatory_request_data)

        if request_data_validation:
            return Response.get_status_422(request_data_validation)

        upload_csv_res = OperationHelper.upload_csv_data(request)
        return upload_csv_res
    
class SearchData(APIView):
    def get(self,request):
        data = request.GET

        mandatory_request_data = [
            "search_data"
        ]
        
        request_data_validation = OperationHelper.validate_request_body(data, mandatory_request_data)

        if request_data_validation:
            return Response.get_status_422(request_data_validation)
        
        skip = data.get("skip") if data.get('skip') else 0
        limit = data.get("limit") if data.get('limit') else 10
        
        final_res = OperationHelper.get_search_data(data,skip, limit) 
        return final_res