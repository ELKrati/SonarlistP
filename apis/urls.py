from django.urls import path

from . import views

urlpatterns = [
    path('get/',views.index,name="index"),
    path('valid_url/',views.valid_url,name="index"),
    path('gettags/',views.get_tages),
]