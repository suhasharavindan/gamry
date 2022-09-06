"""
Functions and constants to handle units.
"""

import re

UNITS = {'V':'V',
         'I':'μA',
         'Q':'C',
         'Scan Rate':'mV/s',
         'Phase':'°',
         'Im(Z)':'Ω',
         'Re(Z)':'Ω',
         '|Z|':'Ω',
         '|Z| dB': 'dB',
         'Freq':'Hz',
         'Time':'s',
         'Plating Voltage':'V',
         'Plating Time':'min',
         'Plating Freq':'Hz',
         'Plating Duty Cycle':'%'}

UNIT_FACTOR = {
    'T':1e12,
    'G':1e9,
    'M':1e6,
    'k':1e3,
    1:1,
    'c':1e-2,
    'm':1e-3,
    'u':1e-6,
    'µ':1e-6,
    'n':1e-9,
    'p':1e-12,
    'f':1e-15
}

FACTOR_DEFAULT = dict(
    v=1,
    a='u',
    ohm=1,
    m='c',
    s=1,
    min=1
)

def factor_conversion(val):
    """Convert values to correct unit.

    Args:
        val (str): Value with units.
    Returns:
        float: Converted value without units since not string.
    """

    if m := re.match(r'^(\d+\.*\d*)\s*([TGMkcmuµnpf]*)([a-zA-Z]+)(\d*)$', val):
        num = float(m.group(1))
        factor = m.group(2) if m.group(2) else 1
        unit = m.group(3).lower()
        exponent = float(m.group(4)) if m.group(4) else 1

        if factor in UNIT_FACTOR.keys() and unit in FACTOR_DEFAULT.keys():
            converted_num = num * (UNIT_FACTOR[factor] / UNIT_FACTOR[FACTOR_DEFAULT[unit]]) ** exponent
            return converted_num

        return None

    elif m := re.match(r'^(\d+\.*\d*)$', val):
        return float(val)

    return None
