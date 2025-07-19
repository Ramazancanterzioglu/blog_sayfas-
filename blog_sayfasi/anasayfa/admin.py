from django.contrib import admin
from .models import DiziFilm

@admin.register(DiziFilm)
class DiziFilmAdmin(admin.ModelAdmin):
    list_display = ('isim', 'kategori', 'tur', 'yayın_yili', 'imdb_puani', 'onerilen', 'olusturma_tarihi')
    list_filter = ('kategori', 'tur', 'onerilen', 'yayın_yili')
    search_fields = ('isim', 'tanim', 'admin_yorumu')
    list_editable = ('onerilen',)
    readonly_fields = ('olusturma_tarihi', 'guncelleme_tarihi')
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('isim', 'kategori', 'tur', 'fotograf')
        }),
        ('İçerik Bilgileri', {
            'fields': ('tanim', 'admin_yorumu', 'yayın_yili', 'sure', 'imdb_puani')
        }),
        ('Ayarlar', {
            'fields': ('onerilen',)
        }),
        ('Tarih Bilgileri', {
            'fields': ('olusturma_tarihi', 'guncelleme_tarihi'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-olusturma_tarihi')
