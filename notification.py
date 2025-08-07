#!/usr/bin/env python3

import subprocess
import re

import dbus

# TODO: Move this to dbus
# Example: (uint32 60,)\n
num_re = re.compile(r' ([0-9]+)')

class Notification(object):
    def __init__(self, expire_time_ms=5000):
        self.notification_id = 0
        self.expire_time_ms = expire_time_ms

    def update(self, summary, body):
        output = dbus.dbus_send_notify(self.notification_id, summary, body, self.expire_time_ms)
        try:
            m = num_re.search(output.decode())
            self.notification_id = int(m.group(1))
        except Exception as e:
            print('ERROR CREATING NOTIFICATION', e)
        return

    def create_notification_notify_send(self, summary, body):
        p = subprocess.Popen(['/usr/bin/notify-send',
                              '--app-name', 'clipmon',
                              '--urgency', 'low',
                              '--expire-time', str(self.expire_time_ms),
                              '--print-id',
                              f"{summary}",
                              f"{body}"],
                              stdout=subprocess.PIPE)
        p.wait()
        output = p.stdout.read()
        print(output)
        self.notification_id = output.strip()
        if not self.notification_id:
            print('ERROR CREATING NOTIFICATION')

    def update_notify_send(self, summary, body):
        if not self.notification_id:
            self.create_notification(summary, body)
        else:
            subprocess.Popen(['/usr/bin/notify-send',
                                '--replace-id', self.notification_id,
                                f"{summary}",
                                f"{body}"]).wait()


if __name__ == '__main__':
    n = Notification()
    n.update('summary', 'body')
