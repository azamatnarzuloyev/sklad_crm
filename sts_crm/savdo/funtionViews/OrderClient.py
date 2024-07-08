from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from magazin.models import AllShop, Savdo, DaySellerShop
from savdo.serializers import SavdoSerializer, DaySellerShopSerialziers
from savdo.utilss import render_to_pdf
from rest_framework.views import APIView
from django.template.loader import get_template
from xhtml2pdf import pisa
from rest_framework.decorators import api_view
from product.models import Product
from random import randint
from rest_framework.response import Response


def qwer_generator(ran):
    import qrcode

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(f"http://127.0.0.1:8000/crm/{ran}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"media/{ran}.png")


class GeneratePdf(APIView):

    def get(self, request, *args, **kwargs):
        data_product = []
        ran = randint(1000, 20000)
        # qwer_generator(ran=ran)
        product = Product.objects.all()[:20]
        for j in product:
            # j.price = j.price * 125
            j.price = j.price and j.price or 10
            data_product.append(
                {
                    "id": j.pk,
                    "product_name": j.product_name,
                    "sh": "SHT",
                    "price": j.price,
                    "count": 5,
                    "discount_price": j.price,
                    "NDS": round((j.price * 5 * 0.12), 2),
                    "umumiy": (j.price * 5) + (j.price * 5 * 0.12),
                }
            )
        dis_sum = 0
        nds_sum = 0
        umumiy = 0
        for j in data_product:
            dis_sum = dis_sum + round((j["discount_price"] and j['discount_price'] or 0), 2)
            nds_sum = nds_sum + j["NDS"]
            umumiy = umumiy + j["umumiy"]

        arr = {
            "dokon_name": "showroom",
            "savdo": "not create",
            "user_name": "Sardorjon",
            "data": date.today(),
        }
        products = {
            "product_name": data_product,
            "dis_sum": dis_sum,
            "nds_sum": nds_sum,
            "umumiy_sum": umumiy,
            "date": f"{date.today()}",
            "ran": ran,
        }

        data = {
            "name": "Mama",  # you can feach the data from database
            "id": 18,
            "amount": 333,
        }
        pdf = render_to_pdf("report.html", products)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Report_for_%s.pdf" % (222)
            content = "inline; filename= %s" % (filename)
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Page Not Found")


@api_view(["GET"])
def render_pdf_view(request):
    template_path = "table.html"
    context = {"product_name": "Блок Питания 12V 10A MINI "}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html,
        dest=response,
    )
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


@api_view(["GET"])
def savdo_getApiViews_pdf(request):
    if request.method == "GET":
        user = request.user
        dokon = AllShop.objects.get(userId__id=user.id)
        if Savdo.objects.filter(
            daySalesDate_create=date.today(), dokon_id=dokon.id
        ).exists():
            savdo = Savdo.objects.get(
                dokon_id__id=dokon.id, daySalesDate_create=date.today()
            )
            day_savdo = DaySellerShop.objects.filter(
                sellerdate_create=date.today(), user_id=user.id
            )
            serializers_savdo = DaySellerShopSerialziers(day_savdo, many=True)
            serializer = SavdoSerializer(savdo)

            arr = {
                "savdo": True,
                "dokon_name": dokon.dokon_name,
                "day_savdo": serializers_savdo.data,
                "savdolar": serializer.data,
                "user_name": dokon.foydalanuvchi_ism,
                "data": date.today(),
            }
            # return Response(arr)

        else:
            arr = {
                "savdo": False,
                "dokon_name": dokon.dokon_name,
                "savdo": "not create",
                "user_name": dokon.foydalanuvchi_ism,
                "data": date.today(),
            }
        pdf = render_to_pdf("table.html", arr)
        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")
            filename = "Report_for_%s.pdf" % (222)
            content = "inline; filename= %s" % (filename)
            response["Content-Disposition"] = content
            return response
        return HttpResponse("Page Not Found")
