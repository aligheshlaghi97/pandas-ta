# -*- coding: utf-8 -*-
from numpy import exp, logical_and, max, min
from pandas import DataFrame, Series
from pandas_ta.utils import get_offset, verify_series
from .remap import remap


def ifisher(
    close: Series,
    amp: float = None, signal_offset: int = None,
    offset: int = None, **kwargs
) -> DataFrame:
    """
    Indicator: Inverse Fisher Transform

    John Ehlers describes this indicator as a tool to change the
    "Probability Distribution Function (PDF)" for the results of known
    oscillator-indicators (time series) to receive clearer signals. Its input
    needs to be normalized into the range from -1 to 1. Input data in the
    range of -0.5 to 0.5 would not have a significant impact. Ehlers note's as
    an important fact that larger values will be transformed or compressed
    stronger to the underlying unity of -1 to 1.

    Preparation Examples (or use 'remap'-indicator for this preparation):
        (RSI - 50) * 0.1        RSI [0 to 100] -> -5 to 5
        (RSI - 50) * 0.02       RSI [0 to 100] -> -1 to 1, use amp of 5 to
                                                           match input of
                                                           example above

    Sources:
        https://www.mesasoftware.com/papers/TheInverseFisherTransform.pdf,
        Book: Cycle Analytics for Traders, 2014, written by John Ehlers, page 198
        Implemented by rengel8 for Pandas TA based on code of Markus K. (cryptocoinserver)

    Args:
        close (pd.Series): Series of 'close's
        amp (float): Use the amplifying factor to increase the impact of
            the soft limiter. Default: 1
        signal_offset (int): Offset the signal line. Default: -1
        offset (int): How many periods to offset the result. Default: 0

    Kwargs:
        fillna (value, optional): pd.DataFrame.fillna(value)
        fill_method (value, optional): Type of fill method

    Returns:
        pd.DataFrame: New feature generated.
    """
    # Validate
    close = verify_series(close)
    amp = float(amp) if amp and amp != 0 else 1.0
    signal_offset = int(signal_offset) if signal_offset and signal_offset > 0 else 1
    offset = get_offset(offset)

    # Calculate
    np_close = close.values
    is_remapped = logical_and(np_close >= -1, np_close <= 1)
    if not all(is_remapped):
        np_max, np_min = max(np_close), min(np_close)
        close_map = remap(close, from_min=np_min, from_max=np_max, to_min=-1, to_max=1)
        np_close = close_map.values
    amped = exp(amp * np_close)
    result = (amped - 1) / (amped + 1)

    inv_fisher = Series(result, index=close.index)
    signal = Series(result, index=close.index)

    # Offset
    if offset != 0:
        inv_fisher = inv_fisher.shift(offset)
        signal = signal.shift(offset)
    if signal_offset != 0:
        inv_fisher = inv_fisher.shift(signal_offset)
        signal = signal.shift(signal_offset)

    # Fill
    if "fillna" in kwargs:
        inv_fisher.fillna(kwargs["fillna"], inplace=True)
        signal.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        inv_fisher.fillna(method=kwargs["fill_method"], inplace=True)
        signal.fillna(method=kwargs["fill_method"], inplace=True)

    # Name and Category
    _props = f"_{amp}"
    inv_fisher.name = f"INVFISHER{_props}"
    signal.name = f"INVFISHERs{_props}"
    inv_fisher.category = signal.category = "transform"

    data = {inv_fisher.name: inv_fisher, signal.name: signal}
    df = DataFrame(data)
    df.name = f"INVFISHER{_props}"
    df.category = inv_fisher.category

    return df
