from django.urls import path
from . import views
app_name = 'dashboard'


urlpatterns = [
    path("", views.index, name="index"),
    path("short/url/<str:link>", views.short_url, name="short_url"),
    path("list/short/urls", views.list_short_urls, name="list_short_urls"),
    path("edit/short/url/<str:link>", views.edit_short_url, name="edit_short_url"),
    path("delete/short/url/<str:link>",
         views.delete_short_url, name="delete_short_url"),
    path("disable/short/url/<str:link>",
         views.disable_short_url, name="disable_short_url"),




]
