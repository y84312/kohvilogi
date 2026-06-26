# Kohvilogi

**Log coffee to the map & journal** — track your coffee consumption with statistics and world map visualization.

[![CI](https://github.com/stennu718/kohvilogi/actions/workflows/ci.yml/badge.svg)](https://github.com/stennu718/kohvilogi/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Coffee logging** — record coffee type, location, time, and notes
- **World map** — visualize coffee consumption on an interactive map
- **Statistics** — daily/weekly/monthly consumption analytics
- **PWA support** — installable as a mobile app
- **QR sharing** — share your coffee profile via QR code
- **Journal** — personal notes and reflections

## Quick Start

```bash
# Clone
git clone https://github.com/stennu718/kohvilogi.git
cd kohvilogi

# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
```

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** Jinja2 templates, vanilla JS
- **Map:** Leaflet.js
- **Deploy:** Docker, Railway

## Screenshots

| Dashboard | Map | Stats |
|-----------|-----|-------|
| ![Dashboard](docs/screenshot-dashboard.png) | ![Map](docs/screenshot-map.png) | ![Stats](docs/screenshot-stats.png) |

## API Documentation

Interactive API docs available at `/docs` when running the server.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT
