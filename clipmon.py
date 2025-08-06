#!/usr/bin/env python3

import notification
import clipboard_monitor
import units


def analyze(s):
    output = ''
    output += f'Chars: {len(s)}'
    output += f'\nLines = {len(s.split('\n'))}'

    first_number = units.find_first_number(s)
    if first_number:
        d = units.parse_number(first_number)
        output += f'\nNumber: {d}'
        output += f'\nSI: {units.find_si_suffix(d)}'
        output += f'\nBinary: {units.find_binary_suffix(d)}'
    return output
    

if __name__ == '__main__':
    n = notification.Notification(expire_time_ms=10000)
    def update_notification(s):
        n.update('summary', analyze(s))
    clipboard_monitor.ClipboardMonitor(callback=update_notification, selection='PRIMARY')
