from django.contrib import admin
from .models import Photo
from core.admin import admin_site

# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    list_display = ["id", "file"]
    search_fields = ["file"]

admin_site.register(Photo, PhotoAdmin)
