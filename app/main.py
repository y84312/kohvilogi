from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.database import init_db, add_expense, get_expenses, get_today_total, get_daily_summary, delete_expense

app = FastAPI(title="Kohvilogi")
templates = Jinja2Templates(directory="templates")

init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    today = datetime.now().strftime("%Y-%m-%d")
    expenses = get_expenses(date=today)
    total = get_today_total()
    summary = get_daily_summary()
    return templates.TemplateResponse(request, "index.html", {
        "expenses": expenses,
        "total": total,
        "summary": summary,
    })


@app.post("/add")
async def add(item: str = Form(...), amount: str = Form(...), currency: str = Form("EUR"), notes: str = Form("")):
    try:
        amt = float(amount.replace(",", "."))
        add_expense(item=item, amount=amt, currency=currency.upper(), notes=notes)
    except ValueError:
        pass
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{expense_id}")
async def delete(expense_id: int):
    delete_expense(expense_id)
    return RedirectResponse(url="/", status_code=303)
