from django.contrib import admin
from .models import DiziFilm, GeziBlog

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


@admin.register(GeziBlog)
class GeziBlogAdmin(admin.ModelAdmin):
    list_display = ('yer_adi', 'sehir', 'kategori', 'puanim', 'ziyaret_tarihi', 'en_iyi_mevsim', 'onerilen', 'olusturma_tarihi')
    list_filter = ('kategori', 'puanim', 'en_iyi_mevsim', 'onerilen', 'sehir')
    search_fields = ('yer_adi', 'sehir', 'kisa_aciklama', 'deneyim', 'tavsiyeler')
    list_editable = ('onerilen',)
    readonly_fields = ('olusturma_tarihi', 'guncelleme_tarihi')
    date_hierarchy = 'ziyaret_tarihi'
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('yer_adi', 'sehir', 'kategori', 'fotograf')
        }),
        ('Gezi Bilgileri', {
            'fields': ('kisa_aciklama', 'deneyim', 'puanim', 'ziyaret_tarihi', 'en_iyi_mevsim')
        }),
        ('Pratik Bilgiler', {
            'fields': ('maliyet', 'konaklama', 'ulasim', 'tavsiyeler')
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
    
    # Admin panelinde puanı yıldız olarak göster
    def puan_yildiz(self, obj):
        return obj.get_puan_yildiz()
    puan_yildiz.short_description = 'Puan'
    
    # List display'e puan_yildiz eklenebilir
    # list_display = (..., 'puan_yildiz', ...)
