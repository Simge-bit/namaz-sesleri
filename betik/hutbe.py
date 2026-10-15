# Diyanet'in yayımladığı son Cuma hutbelerini hutbe/ klasörüne yazar.
# Kaynak: dinhizmetleri.diyanet.gov.tr, Hutbeler (Türkçe). Metin Word dosyasından alınır,
# ses Diyanet'in sesli hutbesidir ve uygulama onu doğrudan Diyanet'ten çalar.
import html, json, os, re, shutil, subprocess, tempfile, time, urllib.parse, urllib.request

BASE = 'https://dinhizmetleri.diyanet.gov.tr'
LIST = BASE + '/kategoriler/yayinlarimiz/hutbeler/t%C3%BCrk%C3%A7e'
UA = {'User-Agent': 'Mozilla/5.0 (namaz-vakti-rehberi; hutbe)'}
KEEP = 12


def get(url, binary=False):
    for attempt in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
            return data if binary else data.decode('utf-8', 'ignore')
        except Exception:
            time.sleep(5 + attempt * 10)
    raise SystemExit(f'İndirilemedi: {url}')


def doc_to_text(data):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'h.doc')
        open(path, 'wb').write(data)
        if shutil.which('textutil'):
            subprocess.run(['textutil', '-convert', 'txt', '-output', path + '.txt', path], check=True)
            return open(path + '.txt', encoding='utf-8').read()
        return subprocess.run(['catdoc', '-d', 'utf-8', '-w', path], check=True,
                              capture_output=True, text=True).stdout


def parse(text):
    lines = [l.strip() for l in text.replace('\r', '\n').splitlines()]
    lines = [l for l in lines if l and not re.search(r'[؀-ۿ]', l)]
    body, notes = [], []
    for line in lines:
        if line.startswith('Tarih:') or line == 'Din Hizmetleri Genel Müdürlüğü':
            continue
        # Dipnotlar sondaki kısa kaynak satırlarıdır (ör. "Tirmizî, Birr, 15.").
        if len(line) < 60 and re.search(r'\d', line) and not line.endswith('!'):
            notes.append(line.rstrip('.') + '.')
            continue
        body.append(line)
    title = body.pop(0) if body and body[0].isupper() else ''
    paragraphs = [{'h': l} if len(l) < 40 and l.endswith('!') else {'p': l} for l in body]
    return title, paragraphs, notes


def main():
    page = get(LIST)
    match = re.search(r'WPQ1ListData = (\{.*?\});\s*var', page, re.S)
    rows = json.loads(match.group(1))['Row']
    rows.sort(key=lambda r: tuple(reversed(r['Tarih'].split('.'))), reverse=True)
    os.makedirs('hutbe', exist_ok=True)
    index = []
    for row in rows[:KEEP]:
        day, month, year = row['Tarih'].split('.')
        date = f'{year}-{month}-{day}'
        path = f'hutbe/{date}.json'
        if not os.path.exists(path):
            text = doc_to_text(get(BASE + urllib.parse.quote(row['Word'], safe='/%!()'), binary=True))
            title, paragraphs, notes = parse(text)
            item = {
                'date': date,
                'title': html.unescape(row['Title']),
                'paragraphs': paragraphs,
                'sources': notes,
                'audio': BASE + row['Ses'] if row.get('Ses') else None,
                'pdf': BASE + row['PDF'] if row.get('PDF') else None,
            }
            with open(path, 'w') as f:
                json.dump(item, f, ensure_ascii=False, separators=(',', ':'))
        index.append({'date': date, 'title': html.unescape(row['Title'])})
    for name in os.listdir('hutbe'):
        if name != 'index.json' and name[:-5] not in {i['date'] for i in index}:
            os.remove(os.path.join('hutbe', name))
    with open('hutbe/index.json', 'w') as f:
        json.dump(index, f, ensure_ascii=False, separators=(',', ':'))
    print(len(index), 'hutbe')


if __name__ == '__main__':
    main()
