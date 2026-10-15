# Namaz Vakti Rehberi verileri

Namaz Vakti Rehberi uygulamasının internetten indirdiği dosyalar.

- `vakit/` Yurt dışındaki şehirler için Diyanet İşleri Başkanlığı'nın yayımladığı namaz vakti çizelgeleri. Kaynak: namazvakitleri.diyanet.gov.tr
- `hutbe/` Diyanet İşleri Başkanlığı'nın son 12 Cuma hutbesi. Kaynak: dinhizmetleri.diyanet.gov.tr. Ses dosyaları Diyanet'in sitesinden çalınır.
- `kadin/` Kur'an surelerinin hafize okuyuşu. Okuyan: "Bir Hâfizenin Sesinden" YouTube kanalı (https://www.youtube.com/channel/UCCb_RmfhGapjB2Ixbm2-xKQ). Sureler kanalın 30 cüz mukabelesinden ayrılmıştır.

## Otomatik güncelleme

`betik/guncelle.py` her pazartesi GitHub Actions ile çalışır. Diyanet'in şehir sayfalarında yeni
açılan günleri `vakit/` çizelgelerine ekler, bir haftadan eski günleri siler.

`betik/hutbe.py` her perşembe ve cuma çalışarak Diyanet'in yeni hutbesini `hutbe/` klasörüne ekler.
