"""
QTPyLib-compatible indicator functions for BinanceBot strategies.
Simple implementations of commonly used indicators.
"""

import pandas as pd


def crossed_above(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Check if series1 crossed above series2.
    Returns True when series1 crosses from below to above series2.
    
    Args:
        series1: First pandas Series
        series2: Second pandas Series or scalar value
        
    Returns:
        Boolean Series indicating crossover points
    """
    above = series1 > series2
    previous_below = (series1.shift(1) <= series2.shift(1)) if isinstance(series2, pd.Series) else (series1.shift(1) <= series2)
    return above & previous_below


def crossed_below(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Check if series1 crossed below series2.
    Returns True when series1 crosses from above to below series2.
    
    Args:
        series1: First pandas Series
        series2: Second pandas Series or scalar value
        
    Returns:
        Boolean Series indicating crossunder points
    """
    below = series1 < series2
    previous_above = (series1.shift(1) >= series2.shift(1)) if isinstance(series2, pd.Series) else (series1.shift(1) >= series2)
    return below & previous_above
