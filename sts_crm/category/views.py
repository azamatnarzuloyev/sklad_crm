from .models import  SubCategory , SuperCategory , MainCategory
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import SuperCategorySerialzier , MainCategorySerialzeir , SubCategorySeriazler




@api_view(['GET'])
def Category_views(request):
    """
    super_id: int id
    main_id: int id 
    """
    if request.method =='GET':
        super_id = request.GET.get('super_id')
        main_id = request.GET.get('main_id')
        if super_id is not None:
            data = MainCategory.objects.filter(superCategory__id=super_id)
            serialzier= MainCategorySerialzeir(data, many=True)
            return Response(
                {
                    "data": serialzier.data,
                    "errors": False,
                    "message": "",
                    "status": 200,
                    "status_code": 200,
                    "token": "",
                }
            )
        if main_id is not None:
            data = SubCategory.objects.filter(mainCategory__id=main_id)
            serialzier= SubCategorySeriazler(data, many=True)
            return Response(
                {
                    "data": serialzier.data,
                    "errors": False,
                    "message": "",
                    "status": 200,
                    "status_code": 200,
                    "token": "",
                }
            )
            
        super_category = SuperCategory.objects.all()
        super_serializer = SuperCategorySerialzier(super_category, many=True)
        return Response(
                {
                    "data": super_serializer.data,
                    "errors": False,
                    "message": "",
                    "status": 200,
                    "status_code": 200,
                    "token": "",
                }
            )

