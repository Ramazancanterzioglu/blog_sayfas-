from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('oran-analizleri/', views.oran_analizleri, name='oran_analizleri'),
    path('muhasebe-terimleri/', views.muhasebe_terimleri, name='muhasebe_terimleri'),
    path('dizi-film-onerileri/', views.dizi_film_onerileri, name='dizi_film_onerileri'),
    path('dizi-film/<int:pk>/', views.dizi_film_detay, name='dizi_film_detay'),
    path('gezi-blog-onerileri/', views.gezi_blog_onerileri, name='gezi_blog_onerileri'),
    path('gezi-blog/<int:pk>/', views.gezi_blog_detay, name='gezi_blog_detay'),
    path('force-migrate/', views.force_migrate, name='force_migrate'),
    path('create-superuser/', views.create_superuser_view, name='create_superuser'),
    path('media-test/', views.media_test_view, name='media_test'),
    path('ornek/', views.ornek_sayfa, name='ornek_sayfa'),
    path('test/', views.test_view, name='test_view'),
]
