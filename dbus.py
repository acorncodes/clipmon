#!/usr/bin/env python3

import subprocess

def dbus_send_notify(replaces_id, summary, body, expire_timeout):
    #return subprocess.check_output([
    #    '/usr/bin/dbus-send',
    #    '--print-reply',
    #    '--type=method_call',
    #    '--dest=org.freedesktop.Notifications',
    #    '/org/freedesktop/Notifications',
    #    'org.freedesktop.Notifications.Notify',
    #    'string:"clipmon"',            # app_name
    #    f'uint32:{replaces_id}',       # replaces_id
    #    'string:"dialog-information"', # app_icon
    #    f'string:"{summary}"',         # summary
    #    f'string:"{body}"',            # body
    #    'array:string:""',             # actions
    #    'dict:string:variant:""',      # hints
    #    f'int32:{expire_timeout}',     # expire_timeout
    #])

    return subprocess.check_output([
        'gdbus', 'call', '--session',
        '--dest=org.freedesktop.Notifications',
        '--object-path=/org/freedesktop/Notifications',
        '--method=org.freedesktop.Notifications.Notify',
        'clipmon',
        f'{replaces_id}',
        'gtk-dialog-info',
        summary,
        body,
        '[]',
        '{}',
        str(expire_timeout),
    ])

if __name__ == '__main__':
    print(dbus_send_notify(0, 'summary', 'body', 5000))
