# Namaz Vakti Rehberi verileri

Namaz Vakti Rehberi uygulamasının internetten indirdiği dosyalar.

- `vakit/` Yurt dışındaki şehirler için Diyanet İşleri Başkanlığı'nın yayımladığı namaz vakti çizelgeleri. Kaynak: namazvakitleri.diyanet.gov.tr
- `kadin/` Kur'an surelerinin hafize okuyuşu. Okuyan: "Bir Hâfizenin Sesinden" YouTube kanalı (https://www.youtube.com/channel/UCCb_RmfhGapjB2Ixbm2-xKQ). Sureler kanalın 30 cüz mukabelesinden ayrılmıştır.

## Otomatik güncelleme

`betik/guncelle.py` her pazartesi GitHub Actions ile çalışır. Diyanet'in şehir sayfalarında yeni
açılan günleri `vakit/` çizelgelerine ekler, bir haftadan eski günleri siler.
