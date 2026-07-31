"""Cache wrappers for fetcher functions using Streamlit cache_data.

This file keeps caching in the UI layer so `fetcher.py` remains usable
outside Streamlit (tests, CLI, API).
"""

from typing import List, Any
import streamlit as st
from fetcher import get_prices, get_history, get_news


@st.cache_data(ttl=300)
def cached_get_prices(symbols: List[str] | None = None) -> dict:
    """Cached wrapper for `get_prices` (5 minutes TTL)."""
    if symbols is None:
        return get_prices()
    return get_prices(symbols)


@st.cache_data(ttl=60)
def cached_get_history(ticker_or_name: str = "bitcoin", period_label: str = "1M") -> Any:
    """Cached wrapper for `get_history` (1 minute TTL for intraday)."""
    return get_history(ticker_or_name, period_label)


@st.cache_data(ttl=600)
def cached_get_news(crypto_name: str, limit: int = 10) -> list:
    """Cached wrapper for `get_news` (10 minutes TTL)."""
    return get_news(crypto_name, limit)
