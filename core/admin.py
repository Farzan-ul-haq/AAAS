from django.contrib import admin
# from django.contrib.admin.options import ModelAdmin

from core import models

# @admin.register(models.Product)
# class ProductAdmin(ModelAdmin):
#     body = admin.CharField(widget=admin.Textarea(attrs={'id': "richtext_field"}))


admin.site.register(models.Product)
admin.site.register(models.User)
admin.site.register(models.Logo)
admin.site.register(models.HtmlTemplate)
admin.site.register(models.DownloadSoftware)
admin.site.register(models.ApiService)
admin.site.register(models.Endpoints)
admin.site.register(models.ProductPackage)
admin.site.register(models.ClientPackages)
admin.site.register(models.Notification)
admin.site.register(models.Feedback)
admin.site.register(models.Brochure)
admin.site.register(models.BrochureTemplates)
admin.site.register(models.MarketingPlatforms)
admin.site.register(models.DribbleProduct)
admin.site.register(models.Transaction)
admin.site.register(models.Tag)
admin.site.register(models.Category)
admin.site.register(models.ClientActivity)
admin.site.register(models.CoroloftProduct)
admin.site.register(models.PinterestProduct)
admin.site.register(models.ProductImpression)
admin.site.register(models.ProductClick)