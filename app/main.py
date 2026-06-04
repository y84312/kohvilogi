from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.database import init_db, add_expense, get_expenses, get_today_total, get_daily_summary, delete_expense, get_monthly_stats

app = FastAPI(title="Kohvilogi")
templates = Jinja2Templates(directory="templates")

init_db()

COFFEE_TYPES = [
    "Espresso",
    "Americano",
    "Cappuccino",
    "Latte",
    "Flat White",
    "Macchiato",
    "Mocha",
    "Ristretto",
    "Lungo",
    "Cold Brew",
    "Filterkohv",
    "Muu",
]

CURRENCIES = [
    ("EUR", "€"),
    ("USD", "$"),
    ("GBP", "£"),
    ("SEK", "kr"),
    ("NOK", "kr"),
    ("DKK", "kr"),
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
    })


@app.post("/add")
async def add(coffee_type: str = Form(...), amount: str = Form(...), currency: str = Form("EUR"), notes: str = Form("")):
    try:
        amt = float(amount.replace(",", "."))
        add_expense(item=coffee_type, coffee_type=coffee_type, amount=amt, currency=currency.upper(), notes=notes)
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
