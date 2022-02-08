# -*- coding: utf-8 -*-
from pandas import Series
from pandas_ta.utils import get_offset, verify_series


def remap(
    close: Series, from_min: float = None, from_max: float = None,
    to_min: float = None, to_max: float = None,
    offset: int = None, **kwargs
) -> Series:
    """
    Indicator: ReMap (REMAP)

    Basically a static normalizer, which maps the input min and max to a given
    output range. Many range bound oscillators move between 0 and 100, but
    there are also other variants. Refer to the example below or add more the
    list.

    Examples:
        RSI -> IFISHER: from_min=0, from_max=100, to_min=-1, to_max=1.0

    Sources:
        rengel8 for Pandas TA

    Args:
        close (pd.Series): Series of 'close's
        from_min (float): Input minimum. Default: 0
        from_max (float): Input maximum. Default: 100
        to_min (float): Output minimum. Default: 0
        to_max (float): Output maximum. Default: 100
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.Series: New feature generated.
    """
    # Validate
    close = verify_series(close)
    from_min = float(from_min) if from_min and from_min != 0.0 else 0.0
    from_max = float(from_max) if from_max and from_max != 0.0 else 100.0
    to_min = float(to_min) if to_min and to_min != 0.0 else -1.0
    to_max = float(to_max) if to_max and to_max != 0.0 else 1.0
    offset = get_offset(offset)

    # Calculate
    frange, trange = from_max - from_min, to_max - to_min
    result = to_min + (trange / frange) * (close.values - from_min)
    result = Series(result, index=close.index)

    # Offset
    if offset != 0:
        result = result.shift(offset)

    # Fill
    if "fillna" in kwargs:
        result.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        result.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    result.name = f"REMAP_{from_min}_{from_max}_{to_min}_{to_max}"
    # result.name = f"{close.name}_{from_min}_{from_max}_{to_min}_{to_max}" # OR
    result.category = "transform"

    return result
