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
