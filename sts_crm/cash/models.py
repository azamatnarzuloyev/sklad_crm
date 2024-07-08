from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.

class Kard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    kard_cod  = models.BigIntegerField(blank=True,null=True)
    activae_kard = models.BooleanField(default=False, blank=True)
    karta_sum = models.PositiveIntegerField(blank=True, default=0)
    karta_random = models.BooleanField(default=False,  blank=True)
    kardSumma_arxiv = models.JSONField(blank=True, null=True)

    
    class Meta:
        verbose_name_plural = "kard"
        ordering = ["pk", "kard_cod"]

   

class DepozitCarddata(models.Model):
    depozit_kard = models.BigIntegerField(blank=True, null=True)
    depozit_sum = models.PositiveIntegerField(blank=True, default=0)
    depozit_random = models.BooleanField(default=False, blank=True)
    activate_depozit = models.BooleanField(default=False, blank=True)
    depozit_arxiv = models.JSONField(blank=True, null=True)
    

class Hamyon(models.Model):
    uuidfiled = models.UUIDField(default=uuid.uuid4, editable=False, auto_created=True)
    kard = models.ManyToManyField(Kard, blank=True)
    money = models.PositiveIntegerField(blank=True, default=0)
    activete = models.BooleanField(default=False, blank=True)
    karta_date = models.DateTimeField(auto_now_add=True, blank=True,)
    depozitcardId = models.ForeignKey(DepozitCarddata, on_delete=models.CASCADE, blank=True, null=True)  


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
