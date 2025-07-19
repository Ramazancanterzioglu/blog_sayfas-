from django.shortcuts import render

def anasayfa(request):
    return render(request, 'anasayfa/index.html')

def oran_analizleri(request):
    return render(request, 'anasayfa/oran-analizleri.html')

def muhasebe_terimleri(request):
    return render(request, 'anasayfa/muhasebe-terimleri.html')

def ornek_sayfa(request):
    return render(request, 'anasayfa/ornek.html')
