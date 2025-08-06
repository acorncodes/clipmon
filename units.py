#!/usr/bin/env python3

import decimal
import re

non_number_re = re.compile(f'[^0-9]')
number_re = re.compile(f'[0-9,].+.?[0-9].*')

def find_first_number(s):
    m = number_re.search(s)
    if m:
        return m.group(0)
    return ''

def parse_number(s):
    if not s:
        return None
    stripped = non_number_re.sub('', s)
    try:
        return decimal.Decimal(stripped)
    except decimal.ConversionSyntax:
        return None

si_suffixes = {
    -3: 'n',
    -2: 'µ',
    -1: 'm',
    1: 'K',
    2: 'M',
    3: 'G',
    4: 'T',
    5: 'P',
    6: 'E',
}
def find_si_suffix(d):
    e1000 = 0
    while d < 0.01:
        e1000 -= 1
        if e1000 not in si_suffixes:
            e1000 += 1
            break
        d *= 1000
    while d > 999:
        e1000 += 1
        if e1000 not in si_suffixes:
            e1000 -= 1
            break
        d /= 1000
    output = str(round(d, 2))
    output += si_suffixes.get(e1000, '')
    return output


binary_suffixes = {
    -3: 'ni',
    -2: 'µi',
    -1: 'mi',
    1: 'Ki',
    2: 'Mi',
    3: 'Gi',
    4: 'Ti',
    5: 'Pi',
    6: 'Ei',
}
def find_binary_suffix(d):
    e = 0
    while d < 0.01:
        e -= 1
        if e not in binary_suffixes:
            e += 1
            break
        d *= 1024
    while d > 999:
        e += 1
        if e not in binary_suffixes:
            e -= 1
            break
        d /= 1024
    output = str(round(d, 2))
    output += binary_suffixes.get(e, '')
    return output