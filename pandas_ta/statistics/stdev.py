# -*- coding: utf-8 -*-
from numpy import sqrt
from pandas import Series
from pandas_ta.maps import Imports
from pandas_ta.utils import get_offset, verify_series
from .variance import variance


def stdev(
    close: Series, length: int = None,
    ddof: int = None, talib: bool = None,
    offset: int = None, **kwargs
) -> Series:
    """Rolling Standard Deviation

    Calculates the Standard Deviation over a rolling period.

    Args:
        close (pd.Series): Series of 'close's
        length (int): It's period. Default: 30
        ddof (int): Delta Degrees of Freedom.
                    The divisor used in calculations is N - ddof,
                    where N represents the number of elements. The 'talib'
                    argument must be false for 'ddof' to work. Default: 1
        talib (bool): If TA Lib is installed and talib is True, Returns
            the TA Lib version. TA Lib does not have a 'ddof' argument.
            Default: True
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    length = int(length) if isinstance(length, int) and length > 0 else 30
    if isinstance(ddof, int) and ddof >= 0 and ddof < length:
        ddof = int(ddof)
    else:
        ddof = 1
    close = verify_series(close, length)
    offset = get_offset(offset)
    mode_tal = bool(talib) if isinstance(talib, bool) else True

    if close is None:
        return

    # Calculate
    if Imports["talib"] and mode_tal:
        from talib import STDDEV
        stdev = STDDEV(close, length)
    else:
        stdev = variance(
            close=close, length=length, ddof=ddof, talib=mode_tal
        ).apply(sqrt)

    # Offset
    if offset != 0:
        stdev = stdev.shift(offset)

    # Fill
    if "fillna" in kwargs:
        stdev.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        stdev.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    stdev.name = f"STDEV_{length}"
    stdev.category = "statistics"

    return stdev
