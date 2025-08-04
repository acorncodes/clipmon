#!/usr/bin/env python3

import subprocess

class Notification(object):
    def __init__(self, expire_time_ms=5000):
        self.notification_id = None
        self.expire_time_ms = expire_time_ms

    def create_notification(self, summary, body):
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

    def update(self, summary, body):
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
