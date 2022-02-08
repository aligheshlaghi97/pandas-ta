# -*- coding: utf-8 -*-
from numpy import fabs
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def mad(
    close: Series, length: int = None,
    offset: int = None, **kwargs
) -> Series:
    """Rolling Mean Absolute Deviation

    Calculates the Mean Absolute Deviation over a rolling period.

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 30
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if length and length > 0 else 30
    if "min_periods" in kwargs and kwargs["min_periods"] is not None:
        min_periods = int(kwargs["min_periods"])
    else:
        min_periods = length
    close = verify_series(close, max(length, min_periods))
    offset = get_offset(offset)

    if close is None:
        return

    # Calculate
    def mad_(series):
        """Mean Absolute Deviation"""
        return fabs(series - series.mean()).mean()

    mad = close.rolling(length, min_periods=min_periods).apply(mad_, raw=True)

    # Offset
    if offset != 0:
        mad = mad.shift(offset)

    # Fill
    if "fillna" in kwargs:
        mad.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        mad.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    mad.name = f"MAD_{length}"
    mad.category = "statistics"

    return mad
