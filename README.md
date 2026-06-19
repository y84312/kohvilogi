# Kohvilogi

Kohvi tarbimise jälgimise veebirakendus — logi kohvi, vaata statistikat ja avasta kohvikultuur maailmas.

![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)

## Funktsioonid

- **Kohvi logimine** — tüüp, summa, valuuta, asukoht, riik, GPS-koordinaadid
- **Statistika** — päevane kuu, streak, unikaalsed riigid, ilmakaare edenemine
- **Maailmakaart** — interaktiivne kaart kohviregioonidega (27 piirkonda)
- **Kohvipass** — jälgib millistes riikides oled kohvi joonud
- **PWA** — installitav, offline-töötav
- **Jagamine** — QR-koodiga jagatav kokkuvõte

## Kiirkäivitus

### Docker (soovitatud)

```bash
docker build -t kohvilogi .
docker run -p 8000:8000 kohvilogi
```

### Käsurealt

```bash
pip install -e .
uvicorn app.main:app --reload
```

Rakendus kättesaadav: http://localhost:8000
API dokumentatsioon: http://localhost:8000/docs

## API

| Endpoint | Kirjeldus |
|---|---|
| `GET /` | Pealeht |
| `POST /add` | Lisa kohvi kirje |
| `POST /delete/{id}` | Kustuta kirje |
| `GET /stats` | Kuu statistika |
| `GET /map` | Maailmakaart |
| `GET /api/streak` | Streak + kiired statistikud |
| `GET /api/world` | Maailma andmed |
| `GET /health` | Tervisekontroll |

## Testid

```bash
pytest tests/ -v
```

## Tehnoloogiad

- **Backend:** FastAPI + SQLite
- **Frontend:** Jinja2 templated, PWA
- **Andmebaas:** SQLite (aiosqlite)
- **Deploy:** Docker

## Litsents

MIT
