from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from fetcher import get_history, get_prices

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PORTFOLIO_FILE = DATA_DIR / "portfolio.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
if not PORTFOLIO_FILE.exists():
    PORTFOLIO_FILE.write_text("[]", encoding="utf-8")


def _normalize_ticker(raw_ticker: str) -> str:
    ticker = raw_ticker.strip().upper()
    if ticker in {"GOLD", "XAU"}:
        return "GC=F"
    if ticker in {"SILVER", "XAG"}:
        return "SI=F"
    if ticker in {"OIL", "CL"}:
        return "CL=F"
    if "-" not in ticker and "=" not in ticker:
        return f"{ticker}-USD"
    return ticker


def _symbol_key(symbol: str) -> str:
    if symbol == "GC=F":
        return "gold"
    if symbol == "SI=F":
        return "silver"
    if symbol == "CL=F":
        return "oil"
    if symbol.endswith("-USD"):
        return symbol[:-4].lower()
    return symbol.lower()


def _load_json() -> list[dict[str, Any]]:
    try:
        return json.loads(PORTFOLIO_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_json(data: list[dict[str, Any]]) -> None:
    PORTFOLIO_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_portfolio() -> list[dict[str, Any]]:
    return _load_json()


def save_portfolio(positions: list[dict[str, Any]]) -> None:
    _save_json(positions)


def add_position(ticker: str, quantity: float, purchase_price: float, purchase_date: date | str | None = None) -> None:
    positions = load_portfolio()
    if purchase_date is None:
        purchase_date = date.today()
    if isinstance(purchase_date, datetime):
        purchase_date = purchase_date.date()
    if isinstance(purchase_date, date):
        purchase_date = purchase_date.isoformat()

    position = {
        "ticker": ticker.strip().upper(),
        "quantity": float(quantity),
        "purchase_price": float(purchase_price),
        "purchase_date": purchase_date,
    }
    positions.append(position)
    save_portfolio(positions)


def remove_position(index: int) -> None:
    positions = load_portfolio()
    if 0 <= index < len(positions):
        positions.pop(index)
        save_portfolio(positions)


def _current_price_for_symbol(symbol: str) -> float | None:
    normalized = _normalize_ticker(symbol)
    prices = get_prices([normalized])
    key = _symbol_key(normalized)
    if key in prices and prices[key].get("usd") is not None:
        return float(prices[key]["usd"])

    hist = get_history(normalized, "1J")
    if hist is not None and not hist.empty and "Close" in hist.columns:
        return float(hist["Close"].iloc[-1])
    return None


def portfolio_snapshot() -> pd.DataFrame:
    positions = load_portfolio()
    rows: list[dict[str, Any]] = []
    total_cost = 0.0
    total_value = 0.0

    for pos in positions:
        ticker = pos.get("ticker", "").upper()
        quantity = float(pos.get("quantity", 0.0))
        purchase_price = float(pos.get("purchase_price", 0.0))
        purchase_date = pos.get("purchase_date", "-")

        current_price = _current_price_for_symbol(ticker)
        invested = quantity * purchase_price
        current_value = quantity * current_price if current_price is not None else 0.0
        pnl = current_value - invested
        pnl_pct = (pnl / invested * 100) if invested else 0.0

        rows.append(
            {
                "Ticker": ticker,
                "Quantité": quantity,
                "Prix d'achat ($)": purchase_price,
                "Coût total ($)": invested,
                "Prix actuel ($)": current_price if current_price is not None else "N/A",
                "Valeur actuelle ($)": current_value,
                "PnL ($)": pnl,
                "PnL (%)": pnl_pct,
                "Date d'achat": purchase_date,
            }
        )

        total_cost += invested
        total_value += current_value

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(by="PnL (%)", ascending=False)
    df.attrs["total_cost"] = total_cost
    df.attrs["total_value"] = total_value
    return df
