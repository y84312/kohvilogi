from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.database import (
    init_db, add_expense, get_expenses, get_today_total,
    get_daily_summary, delete_expense, get_monthly_stats,
    get_world_stats, upsert_coffee_country, get_coffee_countries,
)

app = FastAPI(title="Kohvilogi")
templates = Jinja2Templates(directory="templates")

init_db()

COFFEE_TYPES = [
    "Espresso", "Americano", "Cappuccino", "Latte", "Flat White",
    "Macchiato", "Mocha", "Ristretto", "Lungo", "Cold Brew",
    "Filterkohv", "Muu",
]

CURRENCIES = [
    ("EUR", "€"), ("USD", "$"), ("GBP", "£"),
    ("SEK", "kr"), ("NOK", "kr"), ("DKK", "kr"),
    ("CHF", "Fr"), ("JPY", "¥"), ("TRY", "₺"),
    ("AUD", "A$"), ("CAD", "C$"), ("NZD", "NZ$"),
]

# Common country suggestions for autocomplete
COUNTRY_SUGGESTIONS = [
    ("EE", "Eesti", "🇪🇪"), ("FI", "Soome", "🇫🇮"), ("LV", "Läti", "🇱🇻"),
    ("LT", "Leedu", "🇱🇹"), ("SE", "Rootsi", "🇸🇪"), ("NO", "Norra", "🇳🇴"),
    ("DK", "Taani", "🇩🇰"), ("DE", "Saksamaa", "🇩🇪"), ("NL", "Holland", "🇳🇱"),
    ("BE", "Belgia", "🇧🇪"), ("FR", "Prantsusmaa", "🇫🇷"), ("ES", "Hispaania", "🇪🇸"),
    ("PT", "Portugal", "🇵🇹"), ("IT", "Itaalia", "🇮🇹"), ("AT", "Austria", "🇦🇹"),
    ("CH", "Šveits", "🇨🇭"), ("PL", "Poola", "🇵🇱"), ("CZ", "Tšehhi", "🇨🇿"),
    ("HU", "Ungari", "🇭🇺"), ("RO", "Rumeenia", "🇷🇴"), ("BG", "Bulgaaria", "🇧🇬"),
    ("GR", "Kreeka", "🇬🇷"), ("TR", "Türgi", "🇹🇷"), ("GB", "Suurbritannia", "🇬🇧"),
    ("IE", "Iirimaa", "🇮🇪"), ("US", "USA", "🇺🇸"), ("CA", "Kanada", "🇨🇦"),
    ("MX", "Mehhiko", "🇲🇽"), ("BR", "Brasiilia", "🇧🇷"), ("AR", "Argentina", "🇦🇷"),
    ("CO", "Colombia", "🇨🇴"), ("ET", "Etioopia", "🇪🇹"), ("KE", "Keenia", "🇰🇪"),
    ("JP", "Jaapan", "🇯🇵"), ("CN", "Hiina", "🇨🇳"), ("TH", "Tai", "🇹🇭"),
    ("VN", "Vietnam", "🇻🇳"), ("ID", "Indoneesia", "🇮🇩"), ("AU", "Austraalia", "🇦🇺"),
    ("NZ", "Uus-Meremaa", "🇳🇿"), ("AE", "Araabia Ühendemiraadid", "🇦🇪"),
    ("IN", "India", "🇮🇳"), ("CR", "Costa Rica", "🇨🇷"), ("GT", "Guatemala", "🇬🇹"),
]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    today = datetime.now().strftime("%Y-%m-%d")
    expenses = get_expenses(date=today)
    totals = get_today_total()
    summary = get_daily_summary()
    return templates.TemplateResponse(request, "index.html", {
        "expenses": expenses,
        "totals": totals,
        "summary": summary,
        "coffee_types": COFFEE_TYPES,
        "currencies": CURRENCIES,
        "countries": COUNTRY_SUGGESTIONS,
    })


@app.post("/add")
async def add(
    coffee_type: str = Form(...),
    amount: str = Form(...),
    currency: str = Form("EUR"),
    notes: str = Form(""),
    location: str = Form(""),
    country: str = Form(""),
    latitude: str = Form("0"),
    longitude: str = Form("0"),
):
    try:
        amt = float(amount.replace(",", "."))
        lat = float(latitude) if latitude else 0
        lon = float(longitude) if longitude else 0
        add_expense(
            item=coffee_type, coffee_type=coffee_type, amount=amt,
            currency=currency.upper(), notes=notes,
            location=location, country=country.upper(),
            latitude=lat, longitude=lon,
        )
    except ValueError:
        pass
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{expense_id}")
async def delete(expense_id: int):
    delete_expense(expense_id)
    return RedirectResponse(url="/", status_code=303)


@app.get("/stats", response_class=HTMLResponse)
async def stats(request: Request, month: str | None = None):
    if month is None:
        month = datetime.now().strftime("%Y-%m")
    data = get_monthly_stats(month)
    return templates.TemplateResponse(request, "stats.html", {
        "month": month,
        "data": data,
        "coffee_types": COFFEE_TYPES,
        "currencies": CURRENCIES,
    })


@app.get("/world", response_class=HTMLResponse)
async def world(request: Request):
    data = get_world_stats()
    return templates.TemplateResponse(request, "world.html", {
        "data": data,
        "coffee_types": COFFEE_TYPES,
        "currencies": CURRENCIES,
    })
