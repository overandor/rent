"""Core KPI functions for OverLLM Primitive Ledger / RentMasseur packet."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class DailyRecord:
    date: str
    total_visits: int
    unique_visits: int
    phone_clicks: int
    email_clicks: int
    partial_day: bool = False

    @property
    def contact_actions(self) -> int:
        return self.phone_clicks + self.email_clicks

    @property
    def contact_density(self) -> float:
        return self.contact_actions / self.unique_visits if self.unique_visits else 0.0

    @property
    def phone_density(self) -> float:
        return self.phone_clicks / self.unique_visits if self.unique_visits else 0.0

    @property
    def email_density(self) -> float:
        return self.email_clicks / self.unique_visits if self.unique_visits else 0.0

    @property
    def repeat_visit_factor(self) -> float:
        return self.total_visits / self.unique_visits if self.unique_visits else 0.0


def aggregate(records: Iterable[DailyRecord]) -> dict:
    data = list(records)
    total_visits = sum(r.total_visits for r in data)
    unique_visits = sum(r.unique_visits for r in data)
    phone_clicks = sum(r.phone_clicks for r in data)
    email_clicks = sum(r.email_clicks for r in data)
    contact_actions = phone_clicks + email_clicks
    return {
        "total_visits": total_visits,
        "unique_visits": unique_visits,
        "phone_clicks": phone_clicks,
        "email_clicks": email_clicks,
        "contact_actions": contact_actions,
        "contact_density": contact_actions / unique_visits if unique_visits else 0.0,
        "total_visit_density": contact_actions / total_visits if total_visits else 0.0,
        "phone_density": phone_clicks / unique_visits if unique_visits else 0.0,
        "email_density": email_clicks / unique_visits if unique_visits else 0.0,
        "repeat_visit_factor": total_visits / unique_visits if unique_visits else 0.0,
    }


def opportunity(contact_actions: int, session_price: float = 159.0, close_rate: float = 1.0) -> float:
    return contact_actions * session_price * close_rate


def target_density_uplift(unique_visits: int, current_actions: int, target_density: float, session_price: float = 159.0, close_rate: float = 0.20) -> dict:
    target_actions = round(unique_visits * target_density)
    extra_actions = target_actions - current_actions
    extra_gross_opportunity = extra_actions * session_price
    expected_extra_revenue = extra_gross_opportunity * close_rate
    return {
        "target_actions": target_actions,
        "extra_actions": extra_actions,
        "extra_gross_opportunity": extra_gross_opportunity,
        "expected_extra_revenue": expected_extra_revenue,
    }
