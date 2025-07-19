# Finansal Terimler Rehberi - Django Projesi

Bu proje, finansal terimler ve oran analizlerini içeren modern bir Django web uygulamasıdır.

## Özellikler

- 📊 34 farklı oran analizi
- 📚 Kapsamlı muhasebe terimleri
- 🎨 Modern ve responsive tasarım
- 🌙 Dark mode desteği
- 📱 Mobil uyumlu

## Render.com'da Deploy Etme

### 1. Gereksinimler

Projeniz aşağıdaki dosyaları içermektedir:
- `requirements.txt` - Python bağımlılıkları
- `build.sh` - Build script
- `render.yaml` - Render konfigürasyonu
- Güncellenmiş `settings.py` - Production ayarları

### 2. Deploy Adımları

1. **GitHub Repository Oluşturun:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Render.com'a Gidin:**
   - [render.com](https://render.com) adresine gidin
   - GitHub hesabınızla giriş yapın

3. **Yeni Service Oluşturun:**
   - "New" → "Web Service" seçin
   - GitHub repository'nizi seçin
   - Service ayarları:
     - **Name**: `finansal-terimler-rehberi`
     - **Environment**: `Python 3`
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn blog_sayfasi.wsgi:application`

4. **Environment Variables:**
   Render dashboard'da şu değişkenleri ekleyin:
   - `SECRET_KEY`: Django secret key (otomatik oluşturulacak)
   - `RENDER_EXTERNAL_HOSTNAME`: Otomatik atanacak

5. **Database Oluşturun:**
   - "New" → "PostgreSQL" seçin
   - Database name: `blog_sayfasi_db`
   - User: `blog_sayfasi_user`

6. **Deploy:**
   - "Create Web Service" butonuna tıklayın
   - Build süreci otomatik başlayacak

### 3. Render.yaml ile Otomatik Deploy

Alternatif olarak, repository'nizdeki `render.yaml` dosyası sayesinde:

1. Render dashboard'da "New" → "Blueprint" seçin
2. GitHub repository'nizi seçin
3. `render.yaml` dosyası otomatik algılanacak
4. "Apply" butonuna tıklayın

### 4. Domain

Deploy tamamlandıktan sonra:
- Render size bir URL verecek: `https://your-app-name.onrender.com`
- Custom domain bağlayabilirsiniz (opsiyonel)

## Yerel Geliştirme

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Migrations
python manage.py migrate

# Static files topla
python manage.py collectstatic

# Development server
python manage.py runserver
```

## Dosya Yapısı

```
blog_sayfasi/
├── blog_sayfasi/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── anasayfa/
│   ├── views.py
│   ├── urls.py
│   └── models.py
├── templates/
│   └── anasayfa/
│       ├── index.html
│       ├── oran-analizleri.html
│       └── muhasebe-terimleri.html
├── static/
│   ├── css/
│   └── js/
├── requirements.txt
├── build.sh
├── render.yaml
└── manage.py
```

## Production Ayarları

- **Database**: PostgreSQL (Render tarafından sağlanır)
- **Static Files**: WhiteNoise ile sunulur
- **Security**: HTTPS zorunlu
- **Debug**: Production'da kapatılır

## Troubleshooting

### Build Hatası
```bash
# Build loglarını kontrol edin
# Render dashboard → Service → Logs
```

### Static Files Sorunu
```bash
# Yerel olarak test edin
python manage.py collectstatic --no-input
```

### Database Bağlantı Sorunu
- DATABASE_URL environment variable'ının doğru set edildiğini kontrol edin
- PostgreSQL service'inin aktif olduğunu doğrulayın

## Geliştirici Notları

- Python 3.12 uyumlu
- Django 5.0.2 kullanır
- Responsive CSS Grid Layout
- Font Awesome iconları
- Modern JavaScript ES6+

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. 