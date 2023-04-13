from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>' , views.pages, name='pages'),
    path('result/', views.searchviwe, name='searchviwe'),
    path('newpage/', views.createpage, name='createpage'),
    path('randompage/', views.randpage, name='randpage'),
    path('editpage/<str:title>', views.editpage, name='editpage')  
]
