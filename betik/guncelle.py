# Diyanet'in yurt dışı şehir sayfalarındaki yeni günleri vakit/ klasöründeki çizelgelere ekler.
# Diyanet her sayfada önümüzdeki 30 günü ve bir sonraki takvim yılını gösterir. Bu betik haftada
# bir çalışarak yeni açılan günleri toplar. Geçmişte kalan günler dosyadan silinir.
import datetime, html, json, os, re, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {"User-Agent": "Mozilla/5.0 (namaz-vakti-rehberi; haftalik guncelleme)"}
BASE = "https://namazvakitleri.diyanet.gov.tr"
MONTHS = {'Ocak': 1, 'Şubat': 2, 'Mart': 3, 'Nisan': 4, 'Mayıs': 5, 'Haziran': 6, 'Temmuz': 7,
          'Ağustos': 8, 'Eylül': 9, 'Ekim': 10, 'Kasım': 11, 'Aralık': 12}
KEEP_FROM = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()


def fetch(url):
    for attempt in range(5):
        try:
            req = urllib.request.Request(BASE + url, headers=UA)
            return urllib.request.urlopen(req, timeout=90).read().decode('utf-8', 'ignore')
        except Exception:
            time.sleep(5 + attempt * 10)
    return None


def parse(page):
    days = {}
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>', page, re.S):
        cells = [html.unescape(re.sub(r'<[^>]+>', '', c)).strip()
                 for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.S)]
        if len(cells) < 8 or not all(re.fullmatch(r'\d\d:\d\d', t) for t in cells[2:8]):
            continue
        m = re.match(r'(\d+) (\S+) (\d{4})', cells[0])
        if m and m.group(2) in MONTHS:
            key = f"{m.group(3)}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}"
            days[key] = ''.join(t.replace(':', '') for t in cells[2:8])
    return days


def update(item):
    city, url = item
    path = f'vakit/{city}.json'
    page = fetch(url)
    if not page:
        return 'hata'
    new = parse(page)
    if not new:
        return 'bos'
    table = json.load(open(path))
    merged = {k: v for k, v in table['g'].items() if k >= KEEP_FROM}
    merged.update(new)
    merged = dict(sorted(merged.items()))
    if merged == table['g']:
        return 'ayni'
    table['g'] = merged
    with open(path, 'w') as f:
        json.dump(table, f, separators=(',', ':'))
    return 'guncel'


if __name__ == '__main__':
    cities = json.load(open('betik/sehirler.json'))
    counts = {}
    with ThreadPoolExecutor(4) as pool:
        for result in pool.map(update, cities):
            counts[result] = counts.get(result, 0) + 1
    print(counts)
    # Şehirlerin çoğuna ulaşılamadıysa çalışma başarısız sayılır.
    if counts.get('hata', 0) > len(cities) // 4:
        raise SystemExit('Diyanet sayfalarının çoğuna ulaşılamadı')
