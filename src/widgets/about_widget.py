ABOUT_NBFC_LINUX = """\
<b>NBFC-Linux</b> is a fan control utility designed for Linux systems.

<b>Author</b>: <a href="https://github.com/braph">Benjamin Abendroth</a>

<b>License</b>: GPL-3.0

<b>Project Homepage</b>: <a href="https://github.com/nbfc-linux/nbfc-linux">GitHub.com/NBFC-Linux/NBFC-Linux</a>

<b>Donation Link</b>: <a href="https://paypal.me/BenjaminAbendroth">PayPal.me/BenjaminAbendroth</a>
"""

class AboutWidget(Gtk.Window):
    def __init__(self, parent):
        super().__init__(title="About NBFC-Gtk", transient_for=parent, modal=True)

        # =====================================================================
        # Geometry
        # =====================================================================

        self.set_default_size(300, 200)

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

        desc = Gtk.Label()
        desc.set_markup(ABOUT_NBFC_LINUX)
        vbox.append(desc)

        # =====================================================================
        # OK Button
        # =====================================================================

        ok_button = Gtk.Button(label="OK")
        ok_button.connect("clicked", lambda *_: self.close())
        vbox.append(ok_button)
