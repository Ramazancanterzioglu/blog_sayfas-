from django.db import models
from django.urls import reverse

# Create your models here.

class DiziFilm(models.Model):
    KATEGORI_CHOICES = [
        ('dizi', 'Dizi'),
        ('film', 'Film'),
    ]
    
    TUR_CHOICES = [
        ('aksiyon', 'Aksiyon'),
        ('komedi', 'Komedi'),
        ('drama', 'Drama'),
        ('korku', 'Korku'),
        ('romantik', 'Romantik'),
        ('bilim_kurgu', 'Bilim Kurgu'),
        ('gerilim', 'Gerilim'),
        ('belgesel', 'Belgesel'),
        ('animasyon', 'Animasyon'),
        ('macera', 'Macera'),
    ]
    
    isim = models.CharField(max_length=200, verbose_name="Dizi/Film İsmi")
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICES, verbose_name="Kategori")
    tur = models.CharField(max_length=20, choices=TUR_CHOICES, verbose_name="Tür")
    fotograf = models.ImageField(upload_to='dizi_film/', verbose_name="Fotoğraf")
    tanim = models.TextField(verbose_name="Açıklama/Tanım")
    admin_yorumu = models.TextField(verbose_name="Admin Yorumu")
    yayın_yili = models.IntegerField(verbose_name="Yayın Yılı")
    imdb_puani = models.FloatField(null=True, blank=True, verbose_name="IMDB Puanı")
    sure = models.CharField(max_length=50, verbose_name="Süre", help_text="Örn: 120 dk veya 8 sezon")
    onerilen = models.BooleanField(default=True, verbose_name="Önerilen")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        verbose_name = "Dizi/Film"
        verbose_name_plural = "Dizi/Filmler"
        ordering = ['-olusturma_tarihi']
    
    def __str__(self):
        return f"{self.isim} ({self.kategori})"
    
    def get_absolute_url(self):
        return reverse('dizi_film_detay', kwargs={'pk': self.pk})


class GeziBlog(models.Model):
    KATEGORI_CHOICES = [
        ('dogal', 'Doğal Güzellik'),
        ('tarihi', 'Tarihi Yer'),
        ('sehir', 'Şehir Turu'),
        ('sahil', 'Sahil/Deniz'),
        ('dag', 'Dağ/Yayla'),
        ('kultur', 'Kültürel'),
        ('macera', 'Macera'),
        ('yeme_icme', 'Yeme İçme'),
    ]
    
    PUAN_CHOICES = [
        (1, '⭐ Çok Kötü'),
        (2, '⭐⭐ Kötü'),
        (3, '⭐⭐⭐ Orta'),
        (4, '⭐⭐⭐⭐ İyi'),
        (5, '⭐⭐⭐⭐⭐ Mükemmel'),
    ]
    
    MEVSIM_CHOICES = [
        ('ilkbahar', 'İlkbahar'),
        ('yaz', 'Yaz'),
        ('sonbahar', 'Sonbahar'),
        ('kis', 'Kış'),
        ('yil_boyu', 'Yıl Boyu'),
    ]
    
    yer_adi = models.CharField(max_length=200, verbose_name="Gezilen Yer Adı")
    sehir = models.CharField(max_length=100, verbose_name="Şehir")
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, verbose_name="Kategori")
    fotograf = models.ImageField(upload_to='gezi_blog/', verbose_name="Fotoğraf")
    kisa_aciklama = models.TextField(max_length=300, verbose_name="Kısa Açıklama", help_text="Kısa tanıtım metni")
    deneyim = models.TextField(verbose_name="Gezi Deneyimi", help_text="Detaylı gezi deneyiminizi paylaşın")
    puanim = models.IntegerField(choices=PUAN_CHOICES, verbose_name="Puanım")
    ziyaret_tarihi = models.DateField(verbose_name="Ziyaret Tarihi")
    en_iyi_mevsim = models.CharField(max_length=15, choices=MEVSIM_CHOICES, verbose_name="En İyi Mevsim")
    maliyet = models.CharField(max_length=100, verbose_name="Yaklaşık Maliyet", help_text="Örn: 500-1000 TL")
    konaklama = models.CharField(max_length=200, blank=True, verbose_name="Konaklama Önerisi")
    ulasim = models.TextField(verbose_name="Ulaşım Bilgileri")
    tavsiyeler = models.TextField(verbose_name="Tavsiyelerim", help_text="Gideceklere önerileriniz")
    onerilen = models.BooleanField(default=True, verbose_name="Önerilen")
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    guncelleme_tarihi = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    
    class Meta:
        verbose_name = "Gezi Blog"
        verbose_name_plural = "Gezi Blogları"
        ordering = ['-olusturma_tarihi']
    
    def __str__(self):
        return f"{self.yer_adi} - {self.sehir}"
    
    def get_absolute_url(self):
        return reverse('gezi_blog_detay', kwargs={'pk': self.pk})
    
    def get_puan_yildiz(self):
        """Puanı yıldız formatında döndürür"""
        return "⭐" * self.puanim
    
    def get_puan_yuzde(self):
        """Puanı yüzde formatında döndürür (progress bar için)"""
        return (self.puanim * 20)  # 5 üzerinden 100'e çevir
