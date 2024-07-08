from django.shortcuts import render
from django.http import JsonResponse


class Custom404Middleware:
   
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        response = self.get_response(request)

        # if response.status_code == 404:
        #     return JsonResponse({"errors": True, "message":f"{response}", "status_code": 404,}, safe=False)
        # if response.status_code ==500:
        #     return JsonResponse({"errors": True, "message": f"{response}", "status_code": 500}, safe=False)
        # if response.status_code ==403:
        #     return JsonResponse({"errors": True, "message": f"{response}", "status_code": 403}, safe=False)

        # if response.status_code ==405:
        #     return JsonResponse({"errors": True, "message": f"{response}", "status_code": 405}, safe=False)

        return response