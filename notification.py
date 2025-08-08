#!/usr/bin/env python3

import re
import subprocess


class Notification(object):
    def __init__(self, expire_time_ms=5000):
        self.notification_id = 0
        self.expire_time_ms = expire_time_ms

    def update(self, summary, body):
        try:
            self.notification_id = send_dbus_notification(self.notification_id, summary, body, self.expire_time_ms)
        except Exception as e:
            print('ERROR CREATING NOTIFICATION', e)
        return


# Example command output: (uint32 60,)\n
num_re = re.compile(r' ([0-9]+)')

def send_dbus_notification(replaces_id, summary, body, expire_timeout):
    output = subprocess.check_output([
        'gdbus', 'call', '--session',
        '--dest=org.freedesktop.Notifications',
        '--object-path=/org/freedesktop/Notifications',
        '--method=org.freedesktop.Notifications.Notify',
        'clipmon',             # app name
        f'{replaces_id}',      # replaces_id
        'gtk-dialog-info',     # app_icon
        summary,               # summary
        body,                  # body
        '[]',                  # actions
        '{}',                  # hints
        str(expire_timeout),   # expire_timeout
    ])
    m = num_re.search(output.decode())
    return int(m.group(1))



if __name__ == '__main__':
    n = Notification()
    n.update('summary', 'body')
