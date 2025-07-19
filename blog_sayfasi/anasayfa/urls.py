from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('oran-analizleri/', views.oran_analizleri, name='oran_analizleri'),
    path('muhasebe-terimleri/', views.muhasebe_terimleri, name='muhasebe_terimleri'),
]
