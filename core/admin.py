from django.contrib import admin

from core import models

# Register your models here.

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