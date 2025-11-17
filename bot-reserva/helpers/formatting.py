from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation


def _normalize_iso(value: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        return ""
    if cleaned.endswith("Z"):
        cleaned = cleaned[:-1] + "+00:00"
    if "T" in cleaned:
        date_part, time_part = cleaned.split("T", 1)
        if len(time_part.split(":")) == 2:
            cleaned = f"{date_part}T{time_part}:00"
    return cleaned


def format_datetime(value: str) -> str:
    cleaned = _normalize_iso(value)
    if not cleaned:
        return "-"
    try:
        dt = datetime.fromisoformat(cleaned)
        return dt.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return format_date(value)


def format_date(value: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        return "-"
    try:
        dt = datetime.strptime(cleaned[:10], "%Y-%m-%d")
        return dt.strftime("%d/%m/%Y")
    except ValueError:
        return cleaned


def format_currency(value) -> str:
    if value is None:
        return "-"
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return str(value)
    formatted = f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def format_status(value: str) -> str:
    mapping = {
        "PENDENTE": "Pendente",
        "CONFIRMADA": "Confirmada",
        "CANCELADA": "Cancelada",
    }
    return mapping.get((value or "").upper(), value or "-")
