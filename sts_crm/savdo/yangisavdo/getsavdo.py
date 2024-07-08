from rest_framework.views import APIView
from django.http import JsonResponse
from magazin.models import DaySellerShop, AllShop, Savdo
from permission.permissions import DokonUserAuthentication
from datetime import date

from savdo.serializers import SavdoSerializer 


class DokonSavdoViews(APIView):
    permission_classes = [DokonUserAuthentication]
    def get(self, request, format=None):
        user = request.user
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        shop = AllShop.objects.filter(userId=user.id).first()
        if bool(shop):
            if shop.sklad:
                if start_date is not None and end_date is not None:
                    savdo = Savdo.objects.filter(dokon_id=shop, daySalesDate_create__gte=start_date ,daySalesDate_create__lte=end_date).order_by("?")
                    
                else:
                    savdo = Savdo.objects.filter(daySalesDate_create=date.today()).order_by("?")

            else:
                if start_date is not None and end_date is not None:
                    savdo = Savdo.objects.filter(dokon_id=shop, daySalesDate_create__gte=start_date ,daySalesDate_create__lte=end_date).order_by("?")
                else:
                    savdo = Savdo.objects.filter(dokon_id=shop, daySalesDate_create=date.today()).order_by("?")
            serialzir = SavdoSerializer(savdo , many=True)
            return JsonResponse({ "data": serialzir.data,  "errors": False, "message": "",}, safe=False,)
        return JsonResponse({"data": None, "errors": True, "message": "user errors"}, safe=False)



