#!/usr/bin/env python3
# Most of this file is copied from python-xlib examples for XFixesSelectionOwnerNotify and XSelection

import binascii
import sys
import os

from Xlib import X, display, Xutil, Xatom
from Xlib.ext import xfixes

class ClipboardMonitor(object):
    # SELECTION is typically PRIMARY, SECONDARY or CLIPBOARD.
    def __init__(self, callback, selection='PRIMARY'):
        self.callback = callback
        self.selection = selection

        self.d = display.Display()
        self.sel_atom = self.d.get_atom(selection)

        if not self.d.has_extension('XFIXES'):
            if self.d.query_extension('XFIXES') is None:
                raise Exception('XFIXES extension not supported')

        xfixes_version = self.d.xfixes_query_version()
        print('Found XFIXES version %s.%s' % (
        xfixes_version.major_version,
        xfixes_version.minor_version,
        ), file=sys.stderr)

        screen = self.d.screen()

        mask = xfixes.XFixesSetSelectionOwnerNotifyMask | \
            xfixes.XFixesSelectionWindowDestroyNotifyMask | \
            xfixes.XFixesSelectionClientCloseNotifyMask

        self.d.xfixes_select_selection_input(screen.root, self.sel_atom, mask)

        reader = SelectionReader(self.d)

        try:
            while True:
                e = self.d.next_event()
                print(e)
                if (e.type, e.sub_code) == self.d.extension_event.SetSelectionOwnerNotify:
                    output = reader.read_selection(selection, event=e)
                    self.callback(output)
        except KeyboardInterrupt:
            pass
        reader.cleanup()



class SelectionReader(object):
    def __init__(self, display):
        self.d = display
        self.w = self.d.screen().root.create_window(
            0, 0, 10, 10, 0, X.CopyFromParent)
        self.w.set_wm_name(os.path.basename(sys.argv[0]))
        self.data_atom = self.d.get_atom('SEL_DATA')
        # The data_atom should not be set according to ICCCM, and since
        # this is a new window that is already the case here.
    
    def read_selection(self, selection, target_type=None, event=None):
        selection_atom = self.d.get_atom(selection)

        if event is None:
            # We shouldn't use X.CurrentTime, but since we don't have an event here we have to.
            event_timestamp = X.CurrentTime
            # Ask the server who owns this selection, if any
            owner = self.d.get_selection_owner(selection_atom)
        else:
            event_timestamp = event.selection_timestamp
            owner = event.owner

        if owner == X.NONE:
            print(f'No owner for selection {selection}')
            return ''

        if not target_type:
            target_type = 'UTF8_STRING'
        target_atom = self.d.get_atom(target_type)
        self.w.convert_selection(selection_atom, target_atom, self.data_atom, event_timestamp)

        # Wait for the notification that we got the selection
        while True:
            e = self.d.next_event()
            if e.type == X.SelectionNotify:
                break

        # Do some sanity checks
        if (e.requestor != self.w
            or e.selection != selection_atom
            or e.target != target_atom):
            print(f'SelectionNotify event does not match our request: {e}')

        if e.property == X.NONE:
            print(f'selection lost or conversion to {target_type} failed')
            return ''

        if e.property != self.data_atom:
            print(f'SelectionNotify event does not match our request: {e}')

        # Get the data
        r = self.w.get_full_property(self.data_atom, X.AnyPropertyType,
                                    sizehint = 10000)

        # Can the data be used directly or read incrementally
        if r.property_type == self.d.get_atom('INCR'):
            print(f'reading data incrementally: at least {r.value[0]} bytes')
            return handle_incr(self.d, self.w, self.data_atom, target_type)
        else:
            return output_data(self.d, r, target_type)

    def cleanup(self):
        # Tell selection owner that we're done
        self.w.delete_property(self.data_atom)


def handle_incr(d, w, data_atom, target_name):
    # This works by us removing the data property, the selection owner
    # getting a notification of that, and then setting the property
    # again with more data.  To notice that, we must listen for
    # PropertyNotify events.
    w.change_attributes(event_mask = X.PropertyChangeMask)

    while True:
        # Delete data property to tell owner to give us more data
        w.delete_property(data_atom)

        # Wait for notification that we got data
        while True:
            e = d.next_event()
            if (e.type == X.PropertyNotify
                and e.state == X.PropertyNewValue
                and e.window == w
                and e.atom == data_atom):
                break

        r = w.get_full_property(data_atom, X.AnyPropertyType,
                                sizehint = 10000)

        # End of data
        if len(r.value) == 0:
            return

        return output_data(d, r, target_name)
        # loop around


def output_data(d, r, target_name):
    output = ''

    if r.format == 8:
        if r.property_type == Xatom.STRING:
            value = r.value.decode('ISO-8859-1')
        elif r.property_type == d.get_atom('UTF8_STRING'):
            value = r.value.decode('UTF-8')
        else:
            value = binascii.hexlify(r.value).decode('ascii')
        output += value

    elif r.format == 32 and r.property_type == Xatom.ATOM:
        for v in r.value:
            output += '{0}\n'.format(d.get_atom_name(v))

    else:
        for v in r.value:
            output += '{0}\n'.format(v)
    return output


if __name__ == '__main__':
    ClipboardMonitor(callback=lambda s: print(s))
