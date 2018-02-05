from django.contrib import admin
from . import models


class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class MoldingAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PaintingAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class StyleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

# Register your models here.
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Molding, MoldingAdmin)
admin.site.register(models.Painting, PaintingAdmin)
admin.site.register(models.Service)
admin.site.register(models.Style, StyleAdmin)
admin.site.register(models.Item)
admin.site.register(models.Order)
