
from cash.models import Hamyon, Kard, DepozitCarddata
from magazin.models import Klient
from django.utils.timezone import datetime


class CashbackDataUpdate:
    def __init__(
        self,
        savdo_id: str,
        telefon: int,
        summa: float,
        shop_name: str,
        dokon=False,
        site=False,
        mobile=False,
    ):
        """agar payment true bo'lsa pul yechiladi false bo'lsa pul tashaladi"""
        self.id = telefon
        self.summa = summa
        self.shop_name = shop_name
        self.savdo_id = savdo_id
        self.dokon = dokon
        self.site = site
        self.mobile = mobile
        self.hamyon = Hamyon.objects.get(id=self.id)

    @property
    def cashback_verify(self):
        for i in self.hamyon.kard.all():
            if i.activae_kard and i.kardSumma_arxiv is not None:
                for j in i.kardSumma_arxiv:
                    if str(j["savdo_nomer"]) == str(self.savdo_id):
                        return True
        return False

    @property
    def cashback_tushurish(self):
        if self.cashback_verify:
            return False
        karta_status = False
        if self.hamyon.activete:
            for i in self.hamyon.kard.all():
                if i.activae_kard:
                    ids = Kard.objects.get(id=i.id)
                    ids.karta_sum = ids.karta_sum + self.summa
                    ids.kardSumma_arxiv = ids.kardSumma_arxiv and ids.kardSumma_arxiv or []
                    ids.kardSumma_arxiv.append(
                        {
                            "payment": False,
                            "summa": self.summa,
                            "dokon_name": self.shop_name,
                            "site_status": self.site,
                            "dokon_status": self.dokon,
                            "mobile_status": self.mobile,
                            "savdo_nomer": self.savdo_id,
                            "create_at": f"{datetime.now()}"
                        }
                    )
                    ids.save()
                    karta_status = True
                    return karta_status
        return karta_status

    @property
    def cashback_yechish(self):
        if self.cashback_verify:
            return False
        if self.hamyon.activete:
            for i in self.hamyon.kard.all():
                if i.activae_kard and bool(i.karta_sum >= self.summa):
                    ids = Kard.objects.get(id=i.id)
                    ids.karta_sum = ids.karta_sum - self.summa
                    ids.kardSumma_arxiv = (
                        ids.kardSumma_arxiv and ids.kardSumma_arxiv or []
                    )
                    ids.kardSumma_arxiv.append(
                        {
                            "payment": True,
                            "summa": self.summa,
                            "dokon_name": self.shop_name,
                            "site_status": self.site,
                            "dokon_status": self.dokon,
                            "mobile_status": self.mobile,
                            "savdo_nomer": self.savdo_id,
                            "create_at": f"{datetime.now()}"
                        }
                    )
                    ids.save()

                    return True
        return False


class HisobRaqam:
    def __init__(
        self,
        telefon: int,
        summa: float,
        shop_name: str,
        # article:int,
        dokon=False,
        site=False,
        mobile=False,
        savdo_nomer = None
    ):
        """payment  = true pul yechiladi agar false bo'lsa pull tashaladi"""
        self.id = telefon
        self.summa = summa
        self.shop_name = shop_name
        self.dokon = dokon
        self.site = site
        self.mobile = mobile
        self.savdo_nomer = savdo_nomer
        # self.article = article # bu article dasturni o'zi render qilib client bilan arxiv hisobga joylanadi 
        # self.client = Klient.objects.get(client_user__phone=self.id)
        self.hamyon = Hamyon.objects.get(id=self.id)

    @property
    def hisob_validate(self):
        return True

    @property
    def hisob_tushurish(self):
        if self.hisob_validate:
            ids = DepozitCarddata.objects.get(id=self.hamyon.depozitcardId.pk)
            ids.depozit_sum = ids.depozit_sum + float(self.summa)
            ids.depozit_arxiv = ids.depozit_arxiv and ids.depozit_arxiv or []
            ids.depozit_arxiv.append(
                {
                    "payment": False,
                    "summa": self.summa,
                    "dokon_name": self.shop_name,
                    "site_status": self.site,
                    "dokon_status": self.dokon,
                    "mobile_status": self.mobile,
                    "create_at": f"{datetime.now()}",
                    "savdo_nomer": self.savdo_nomer
                }
            )
            ids.save()
       

    @property
    def hisob_yechish(self):
        if self.hisob_validate:
            ids = DepozitCarddata.objects.get(id=self.hamyon.depozitcardId.pk)
            if ids.depozit_sum >= self.summa:
                ids.depozit_sum = ids.depozit_sum - float(self.summa)
                ids.depozit_arxiv = ids.depozit_arxiv and ids.depozit_arxiv or []
                ids.depozit_arxiv.append(
                    {
                        "payment": True,
                        "summa": self.summa,
                        "dokon_name": self.shop_name,
                        "site_status": self.site,
                        "dokon_status": self.dokon,
                        "mobile_status": self.mobile,
                        "create_at": f"{datetime.now()}",
                        "savdo_nomer": self.savdo_nomer
                    }
                )
                ids.save()
        return False
