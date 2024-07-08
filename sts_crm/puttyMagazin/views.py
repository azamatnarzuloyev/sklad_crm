from puttyMagazin.models import   DokonPutty
from rest_framework.views import APIView
from rest_framework.response import Response



class DokonPuttyViews(APIView):
    def get(self, requests, format=None):
        dokonputty = DokonPutty.objects.first()
        data = []
        for i in dokonputty.tavarlar:
            data.append({
                "product_id": i,
                "product_name": dokonputty.tavarlar[i]['product_name'],
                "product_serena": dokonputty.tavarlar[i]['product_serena']

                
            })
        return Response(data=data)