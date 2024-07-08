from django.db import models
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify
import random, string


from PIL import Image as image


# Create your models here.

class SuperCategory(models.Model):
    super_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    category_image   = models.ImageField(
        upload_to='categories/super/imgs/', verbose_name=("Category Image"), blank=True, null=True, help_text=("Please use our recommended dimensions: 120px X 120px"))
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    meta_name = models.CharField(max_length=200, blank=True, null=True)
    meta_content = models.CharField(max_length=300, blank=True, null=True)
    sts_site = models.BooleanField(default=False)
    rts_site = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


   

    class Meta:
        verbose_name_plural = "SuperCategory"
        ordering = ["pk", "super_name"]

    def __str__(self):
        return self.super_name


    @classmethod
    def make_slug(cls, super_name):
        slug = slugify(super_name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                super_name + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug


    def save(self, *args, **kwargs):
        self.super_name = self.super_name.title() if self.super_name else self.super_name
        self.slug = self.make_slug(self.super_name)

        super().save(*args, **kwargs)
        

class MainCategory(models.Model):
    superCategory=models.ForeignKey(SuperCategory, on_delete=models.CASCADE, blank=True, null=True)
    main_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    main_image   = models.ImageField(
        upload_to='categories/main/imgs/', verbose_name=(" Main Category Image"), blank=True, null=True)
     
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    main_meta = models.CharField(max_length=200, blank=True, null=True)
    main_content = models.CharField(max_length=300, blank=True, null=True)
    sts_site = models.BooleanField(default=False)
    rts_site = models.BooleanField(default=False)
    created = models.DateTimeField(blank=True, null=True)


   

    class Meta:
        verbose_name_plural = "MainCategory"
        ordering = ["pk", "main_name"]

    def __str__(self):
        return self.main_name


    @classmethod
    def make_slug(cls,  main_name):
        slug = slugify( main_name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                 main_name + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug


    def save(self, *args, **kwargs):
        self.main_name = self.main_name.title() if self. main_name else self. main_name
        self.slug = self.make_slug(self.main_name)

        super().save(*args, **kwargs)


class SubCategory(models.Model):
    mainCategory=models.ForeignKey(MainCategory, on_delete=models.CASCADE, blank=True, null=True)
    sub_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    sub_image   = models.ImageField(
        upload_to='categories/main/imgs/', verbose_name=("Sub Category Image"), blank=True, null=True)
     
    slug = models.SlugField(unique=True, null=True, editable=False, blank=True)
    sub_meta = models.CharField(max_length=200, blank=True, null=True)
    sub_content = models.CharField(max_length=300, blank=True, null=True)
    sts_site = models.BooleanField(default=False)
    rts_site = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


   

    class Meta:
        verbose_name_plural = "SubCategory"
        ordering = ["pk", "sub_name"]

    def __str__(self):
        return self.sub_name


    @classmethod
    def make_slug(cls, sub_name):
        slug = slugify(sub_name, allow_unicode=False)
        letters = string.ascii_letters + string.digits

        while cls.objects.filter(slug=slug).exists():
            slug = slugify(
                sub_name + "-" + "".join(random.choices(letters, k=6)), allow_unicode=False
            )
        return slug


    def save(self, *args, **kwargs):
        self.sub_name = self.sub_name.title() if self.sub_name else self.sub_name
        self.slug = self.make_slug(self.sub_name)

        super().save(*args, **kwargs)

