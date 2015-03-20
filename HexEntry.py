from gi.repository import Gtk, GObject, Gdk, GLib
import string

class HexEntry(Gtk.Entry):
    """A PyGTK text entry field which allows only Hex characters to be entered"""

    def __init__(self):
        Gtk.Entry.__init__(self)
        self.connect("insert_text", self.entryInsert)

    def entryInsert(self, entry, text, length, position):
        position = entry.get_position()
        result = ''.join([c for c in text if c in string.hexdigits]).upper()

        if result != '':
            # Insert the new text at cursor (and block the handler to avoid recursion).
            entry.handler_block_by_func(self.entryInsert)
            entry.insert_text(result, position)
            entry.handler_unblock_by_func(self.entryInsert)

            # Set the new cursor position immediately after the inserted text.
            new_pos = position + len(result)

            # Can't modify the cursor position from within this handler,
            # so we add it to be done at the end of the main loop:
            GObject.idle_add(entry.set_position, new_pos)

        # We handled the signal so stop it from being processed further.
        entry.stop_emission("insert_text")
