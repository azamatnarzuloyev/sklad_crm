from django.db import models
import uuid
from magazin.models import AllShop
from django.contrib.postgres.fields import ArrayField

from datetime import date

class TavarPutty(models.Model):
    """ putty product all """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shopId = models.ForeignKey(AllShop, on_delete=models.CASCADE, blank=True, null=True)
    send_maagzinId = models.UUIDField(blank=True, null=True)
    product_status = models.BooleanField(default=False, blank=True)
    comentary = models.CharField(max_length=300, blank=True, null=True)
    putty_status = models.BooleanField(default=False, blank=True)
    qabul = models.BooleanField(default=False, blank=True)
    create_date = models.DateField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    putty_delete = models.BooleanField(default=False, blank=True)
    tavarlar = ArrayField(models.JSONField(blank=True), blank=True, null=True)
    zakasproductstatus =  models.IntegerField(blank=True, null=True)

    @property
    def choose_dokon(self):
        if AllShop.objects.count():
            for i in AllShop.objects.all():
                return ({"id": i.id,"dokon_name": i.dokon_name })


    class Meta:
        verbose_name_plural = "TavarPutty"
        ordering = ["pk"]
    

    def __str__(self):
        return f"{self.send_maagzinId}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class DokonPutty(models.Model):
    dokon_uuid = models.ForeignKey(AllShop , on_delete=models.CASCADE, blank=True, null=True)
    created = models.BooleanField(default=False, blank=True, null=True)
    # vendor_tavarlar = models.JSONField(blank=True, null=True, default=)
    tavarlar = models.JSONField(blank=True, null=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    
class ZakasProduct(models.Model):
    "tavarni skladga zakas qilish "
    products = models.JSONField(blank=True)

    nomer_zakas =models.IntegerField(blank=True, null=True)

    qabul = models.BooleanField(default=False, blank=True)

    shop_id = models.UUIDField(blank=True)

    date_filter = models.DateField(blank=True, null=True)

    shop_name = models.CharField(blank=True, null=True)
    
    create_at = models.DateTimeField(blank=True, auto_now_add=True)

    update_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_filter is None:
            self.date_filter = date.today()
        if self.shop_id is not None:
            all_shop = AllShop.objects.get(id=self.shop_id)
            self.shop_name = all_shop.dokon_name
        super().save(*args, **kwargs)