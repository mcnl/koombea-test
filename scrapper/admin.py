from django.contrib import admin
from .models import Page, Link


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "total_links", "page_link")
    search_fields = ("name", "page_link")


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("id", "page", "name", "link")
    search_fields = ("name", "link")
    list_filter = ("page",)
