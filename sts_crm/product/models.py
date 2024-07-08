from django.db import models
from category.models import SubCategory, SuperCategory, MainCategory
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import random, string
from PIL import Image as image
from django.utils.html import format_html
from datetime import date 
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import datetime

class Image(models.Model):
    product = models.ForeignKey(
        "product.Product", models.SET_NULL, null=True, related_name="images"
    )
    image = models.ImageField(upload_to="products", blank=False, null=True)



class Product(models.Model):
    product_name = models.CharField(max_length=300, blank=True)
    material_nomer = models.BigIntegerField(blank=True, null=True, unique=True)
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    articul = models.PositiveIntegerField(blank=True , null=True)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_data = models.CharField(max_length=300, blank=True, null=True)
    tavar_dagavornaya = models.BooleanField(default=False)
    super_category = models.ForeignKey(SuperCategory, on_delete=models.SET_NULL,  blank=True, null=True)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, blank=True, null=True)
    product_status = models.BooleanField(default=False, blank=True)
    seller_count = models.PositiveIntegerField(blank=True, default=0)
    short_description = RichTextField(blank=True, null=True)
    full_description = RichTextField(blank=True, null=True)
    product_video = models.FileField(upload_to="productvideo", blank=True, null=True)
    product_picture = models.ImageField(upload_to="products/images/", verbose_name="product images", blank=True, null=True)
    # product_filter = models.ManyToManyField(ProductFilter, blank=True, null=True)
    deliver_date = models.PositiveIntegerField(blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    tavar_ckidka = models.PositiveIntegerField(blank=True, default=0)
    total_number = models.IntegerField(blank=True, null=True)   # shu nomerni nechi bo'lsa osnovnoy skladda shuni ko'rsataman
    Umumiy_soni = ArrayField(models.IntegerField(), blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    tavar_putty = models.BooleanField(default=False, blank=True)
    site_sts = models.BooleanField(default=False, blank=True)
    site_rts = models.BooleanField(default=False, blank=True)
    serenaTrue_countFalse = models.BooleanField(default=True)
    dokon_tavarlar = ArrayField(models.JSONField(blank=True), blank=True, null=True)
    

    @property
    def image(self):
        obj = self.images.first()
        if obj and obj.image:
            return obj.image.url
        return None
    def image_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 2px;' src='{}'>".format(self.image))
    @property
    def image_count(self):
        return self.images.all().count()

    @property
    def url(self):
        return reverse("products_detail", kwargs={"slug": self.slug})

    @property
    def has_banner_ad(self):
        if self.banner_ad:
            return True
        return False


    class Meta:
        verbose_name_plural = "Product"
        ordering = ["pk", "product_name"]

    def __str__(self):
        return self.product_name


    @classmethod
    def make_slug(cls,product_name):
        slug = slugify( product_name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                product_name + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug


    def save(self, *args, **kwargs):
        self.product_name = self.product_name.title() if self.product_name else self.product_name
        self.slug = self.make_slug(self.product_name)

        super().save(*args, **kwargs)



        





class ProductJsonArxiv(models.Model):
    date = models.DateField(blank=True)
    json_product = models.JSONField(blank=True, null=True)


    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    




class ProductNewsImport(models.Model):
    """ import product new serena or count """
    import_id = models.IntegerField(blank=True, unique=True , verbose_name=_("import products"))
    commentary = models.CharField(max_length=100,  blank=True, null=True)
    create_at = models.DateField(blank=True, null=True, verbose_name=_("create date product"))
    datetime_create = models.DateTimeField(blank=True, null=True)
    createStatus_number = models.IntegerField(default=0 , blank=True , verbose_name=_("number status")) # number values of 0 = create; 1 = product create ; 2 = success
    products = models.JSONField(blank=True, null=True)
    close_data = models.BooleanField(default=False , blank=True)
    shop_id = models.UUIDField(blank=True, null=True)
    file_url = models.URLField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.create_at is None:
            self.create_at = f"{date.today()}"
        if self.datetime_create is None:
            self.datetime_create = f"{datetime.now()}"
        return super().save(*args, **kwargs)
    





class TavarTekshiruv(models.Model):
    shop_id = models.UUIDField(blank=True, null=True)
    shop_name = models.CharField(blank=True, null=True)
    products=  models.JSONField(blank=True, null=True)
    status = models.BooleanField(default=False, blank=True,  help_text=_("status bu dokondan barcha tavarlarni tekshirgan yoki tekshirmagani bildiriadi"))
    qarzdorlik = models.PositiveIntegerField(default=0 , blank=True ,help_text=_("qarzdorlik bo'yicha chiqmagan tavarlarni umumiy narxi"))
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    

#  ---------------------------------------------- serena path ------------------------------------------------------------------


class ProductSerenapathOne(models.Model):
    """ Product serena yolini ko'rsatish 1 model """
    # articel = models.IntegerField(blank=True , unique=True, null=True)
    product_id = models.IntegerField(blank=True , unique=True)
    product_name = models.CharField(max_length=200, blank=True)
    material_nomer = models.CharField(max_length=30 , blank=True , null=True)
    serena_path = models.JSONField(blank=True, null=True)


    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
 

class ProductSerenapathTwo(models.Model):
    """ Product serena yolini ko'rsatish 2 model """
    # articel = models.IntegerField(blank=True , unique=True, null=True)
    product_id = models.IntegerField(blank=True , unique=True)
    product_name = models.CharField(max_length=200, blank=True)
    material_nomer = models.CharField(max_length=30 , blank=True , null=True)
    serena_path = models.JSONField(blank=True, null=True)


    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class ProductSerenapathFour(models.Model):
    """Product serena yolini ko'rsatish 3 model """
    # articel = models.IntegerField(blank=True , unique=True, null=True)
    product_id = models.IntegerField(blank=True , unique=True)
    product_name = models.CharField(max_length=200, blank=True)
    material_nomer = models.CharField(max_length=30 , blank=True , null=True)

    serena_path = models.JSONField(blank=True, null=True)


    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

class ProductSerenapathEnd(models.Model):
    """Product serena yolini ko'rsatish 4 model """
    # articel = models.IntegerField(blank=True , unique=True, null=True)
    product_id = models.IntegerField(blank=True , unique=True)
    product_name = models.CharField(max_length=200, blank=True)
    material_nomer = models.CharField(max_length=30 , blank=True , null=True)
    serena_path = models.JSONField(blank=True, null=True)

    """
     path: [
        {
          "date": {"sender": "showroom" , "recipient": "", "status": "client","client_id": "" , "client_name": ""},
          "date" : {},
        }
     ]

    """


    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
 

class ZerenaPathStatus(models.Model):
    """ Zerena path uchun setting model bunda agar modellar true bo'lsa malumotlar shunga qo'shiladi """
    datatest = models.CharField(blank=True, default='test' , verbose_name=_('test settings') , help_text=_("buni o'zgartirmang"), editable=False)
    count_status = models.IntegerField(default=1 , blank=True)
    year_filter = models.IntegerField(blank=True , unique=True)
    delete_bool =  models.BooleanField(default=False , blank=True)



    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)













    