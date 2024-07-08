from django.contrib import admin

# Register your models here.
from .models import Product, Image, ProductJsonArxiv, ProductNewsImport


from django.db.models.fields.json import JSONField
from jsoneditor.forms import JSONEditor

# admin.site.register(ProductJsonArxiv)


@admin.register(ProductJsonArxiv)
class ProductJsonArxivAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditor},
    }
    list_display = ("date",)


class GalleryInlines(admin.TabularInline):
    model = Image
    max_num = 6


@admin.register(Product)
class ProductsModelAdmin(admin.ModelAdmin):
    list_display = [
        "product_name",
        "price",
        "image_tag",
    ]

    fields = [
        "product_name",
        "price",
        "discount_price",
        "tavar_ckidka",
        "meta_title",
        "meta_data",
        "super_category",
        "main_category",
        "sub_category",
        "product_status",
        "product_video",
        "product_picture",
        "short_description",
        "full_description",
        "material_nomer",
    ]

    inlines = [GalleryInlines]

    search_fields = [
        "product_name",
        "price",
    ]
    # list_editable = [
    #     "price",
    # ]
    list_filter = [
        "site_sts",
        "site_rts",
    ]


admin.site.register(ProductNewsImport)
