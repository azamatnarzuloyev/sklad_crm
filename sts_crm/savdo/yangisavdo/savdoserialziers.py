from rest_framework import serializers
from magazin.models import DaySellerShop 

def get_savdo_status():
    return {
        "hisobot": { "tavar_summasi": None, "jami_skidka": None, "olingan_summa": None, "tushgan_cashback_summa": None,"yechilgan_cashback_summ": None, "depozitga_tushgan_summa": None,},
        "tolov_usullar": {
            "naxt": {"active": False,"summa": 0, "check": False},
            "plastik": { "active": False, "summa": 0, "check": False, },
            "joyidaTolov": { "active": False,  "summa": 0, "check": False,  "id_raqam": None},
            "qarz": {"active": False,  "summa": 0, "update_at": None, "eslatma": {"date": None, "status": False}, },
            "depozit": { "active": False,"summa": 0, "check": False,},
            "shartnoma": {"active": False,"summa": 0,"check": False,"id_raqam": None , "shartnoma_raqam":None },
            }
        }




