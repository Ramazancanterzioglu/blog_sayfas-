"""
URL configuration for blog_sayfasi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# Test view - Django'nun çalışıp çalışmadığını kontrol et
def root_test(request):
    return HttpResponse("""
    <h1>🎉 DJANGO ÇALIŞIYOR!</h1>
    <p>Bu Render.com'da çalışan Django uygulamasıdır.</p>
    <h2>Test Linkleri:</h2>
    <ul>
        <li><a href="/test/">Detaylı Test</a></li>
        <li><a href="/admin/">Admin Panel</a></li>
    </ul>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('root-test/', root_test, name='root_test'),
    path('', include('anasayfa.urls')),
]


# Static files (CSS, JavaScript, Images) için URL patterns ekle
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Media files için URL patterns - Her durumda çalışır (development & production)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
