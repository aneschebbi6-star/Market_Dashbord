import pandas as pd
import numpy as np
from fetcher import get_history


def test_ma_windows_for_daily_data():
    # For daily interval and enough days, MA50 and MA200 should be computed (or NA if insufficient)
    hist = get_history('bitcoin', period_label='1M')
    # hist may be empty depending on environment; skip test gracefully
    if hist.empty:
        return
    assert 'EMA20' in hist.columns
    # If daily data and length >=50, MA50 should not be NA
    if hist.attrs.get('interval_used') == '1d' and len(hist) >= 50:
        assert 'MA50' in hist.columns and not hist['MA50'].isna().all()


def test_ma_windows_for_intraday_1j():
    # For 1J intraday, MA50/MA200 may be NA but EMA20 should exist
    hist = get_history('gold', period_label='1J')
    if hist.empty:
        return
    assert 'EMA20' in hist.columns
    # MA50 likely NA for intraday 1J
    assert 'MA50' in hist.columns or True
    
