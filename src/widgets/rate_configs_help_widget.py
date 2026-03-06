RATE_CONFIG_HELP_TEXT = """\
The rating feature analyzes whether a configuration can be executed safely on the current system. A positive rating does not necessarily mean that the configuration will work correctly, only that it appears reasonable and non-destructive.

Configurations that reference the same registers and ACPI methods are grouped together.

<b>FULL MATCH</b>
Indicates that the register is a known fan register.

<b>PARTIAL MATCH</b>
Indicates that the register name contains <b>FAN</b>, <b>RPM</b>, or <b>PWM</b>.

<b>MINIMAL MATCH</b>
Indicates that the register name starts with the letter '<b>F</b>'.

<b>BAD REGISTER</b>
Indicates that the register name is a known bad register (likely a battery-related register).

<b>NO MATCH</b>
Indicates that none of the matching rules apply.

<b>NOT FOUND</b>
Indicates that the register is not named in the firmware and additional information could not be retrieved.

For fan registers, at least a <b>MINIMAL MATCH</b> is required to consider a configuration usable.

For RegisterWriteConfiguration registers, some registers may not yet be present in the rule database. In these cases, a <b>NO MATCH</b> result may still be acceptable.

If in doubt, it is recommended to dump the firmware using <b>sudo nbfc acpi-dump dsl</b> and manually analyze the registers used by the configuration file. This requires some technical knowledge."""

class RateConfigsHelpWindow(Gtk.Window):
    def __init__(self, parent):
        super().__init__(title="NBFC Rated Configs Help", modal=False)

        self.set_default_size(400, 400)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(box)

        scroll_area = Gtk.ScrolledWindow()
        scroll_area.set_hexpand(True)
        scroll_area.set_vexpand(True)
        box.append(scroll_area)

        label = Gtk.Label()
        label.set_wrap(True)
        label.set_max_width_chars(40)
        label.set_markup(RATE_CONFIG_HELP_TEXT)
        label.set_margin_start(6)
        label.set_margin_end(6)
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        scroll_area.set_child(label)

        button = Gtk.Button(label="Close")
        button.set_margin_start(6)
        button.set_margin_end(6)
        button.set_margin_top(6)
        button.set_margin_bottom(6)
        button.connect("clicked", self.close_clicked)
        box.append(button)

    def close_clicked(self, button):
        self.close()
