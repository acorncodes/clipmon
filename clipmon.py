#!/usr/bin/env python3

import notification
import clipboard_monitor

if __name__ == '__main__':
    n = notification.Notification(expire_time_ms=10000)
    def update_notification(s):
        body = ''
        body += f'len: {len(s)}'
        n.update('summary', body)
    clipboard_monitor.ClipboardMonitor(callback=update_notification, selection='PRIMARY')
