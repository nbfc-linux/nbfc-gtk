class EarlyErrorWindow(Gtk.ApplicationWindow):
    def __init__(self, app, title, message):
        super().__init__(application=app)

        # =====================================================================
        # Title
        # =====================================================================

        self.set_title(title)

        # =====================================================================
        # Box (Vertical)
        # =====================================================================

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_margin_start(12)
        vbox.set_margin_end(12)
        vbox.set_margin_top(12)
        vbox.set_margin_bottom(12)
        self.set_child(vbox)

        # =====================================================================
        # Markup
        # =====================================================================

        self.desc = Gtk.Label()
        self.desc.set_margin_start(12)
        self.desc.set_margin_end(12)
        self.desc.set_margin_top(12)
        self.desc.set_margin_bottom(12)
        self.desc.set_text(message)
        vbox.append(self.desc)

        # =====================================================================
        # OK Button
        # =====================================================================

        ok_button = Gtk.Button(label="OK")
        ok_button.connect("clicked", lambda *_: self.close())
        vbox.append(ok_button)
