from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

class ResponseHelper:
    def get_status_200(self, data=None, total_count=None):
        ok_response = {"message": "success", "data": data}
        if total_count:
            ok_response = {"message": "success", "data": data, "total_count": total_count}
        return Response(ok_response, status=status.HTTP_200_OK)

    def get_status_201(self,data=None):
        ok_response = {"message": "success"}
        if data:
            ok_response = {"message": "Accepted", "data": data}
        return Response(ok_response, status=status.HTTP_201_CREATED)

    def get_status_202(self, data=None):
        ok_response = {"message": "Accepted", "data": data}
        return Response(ok_response, status=status.HTTP_202_ACCEPTED)

    def get_status_204(self, data=None):
        ok_response = {"message": "No Content", "data": data}
        return Response(ok_response, status=status.HTTP_204_NO_CONTENT)

    def get_status_404(self, msg="No data found"):
        not_found_response = {"message": msg}
        return JsonResponse(not_found_response, safe=False, status=status.HTTP_404_NOT_FOUND)

    def get_status_500(self, msg="internal server error"):
        error_message = {"message": msg}
        return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_status_400(self, msg="invalid data"):
        error_message = {"message": msg}
        return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)

    def get_status_406(self, msg="not acceptable"):
        error_message = {"message": msg}
        return JsonResponse(error_message, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_status_422(self, msg="Unprocessable Entity please check status key"):
        error_message = {"message": msg}
        return Response(error_message, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get_error_with_data(self, res, msg="error"):
        try:
            return Response({"message": msg, "data": res.data}, status=res.status_code)
        except:
            return Response({"message": msg, "data": res.text}, status=res.status_code)

    def get_success_with_data(self, data, status, msg="data found"):
        return Response({"message": msg, "data": data}, status=status)

    def get_status_401(self, msg="Unauthorized"):
        error_message = {"message": msg}
        return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)

    def get_exception_error(self, msg):
        return Response(msg, status=status.HTTP_500_INTERNAL_SERVER_ERROR)