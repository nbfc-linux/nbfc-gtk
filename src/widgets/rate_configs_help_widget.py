RATE_CONFIG_USAGE_TEXT = """\
The rating feature analyzes whether a configuration can be applied safely on the current system. A positive rating does not necessarily mean that the configuration will work correctly, only that it appears reasonable and non-destructive.

Configurations that reference the same registers and ACPI methods are grouped together.

It is recommended to start by testing <b>one configuration from each group</b>. Within a group, <b>try to choose a configuration whose name closely matches your laptop model</b>, as it is more likely to work correctly.

If a configuration only works partially—for example, if the fan does not fully stop or does not reach its maximum speed—you can try other configurations from the same group.\
"""

RATE_CONFIG_INTERPRETING_RESULTS_TEXT = """\
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

If in doubt, it is recommended to dump the firmware using <b>sudo nbfc acpi-dump dsl</b> and manually analyze the registers used by the configuration file. This requires some technical knowledge.\
"""

class RateConfigsHelpTextWidget(Gtk.ScrolledWindow):
    def __init__(self, markup):
        super().__init__()

        self.set_hexpand(True)
        self.set_vexpand(True)

        label = Gtk.Label()
        label.set_wrap(True)
        label.set_max_width_chars(40)
        label.set_markup(markup)
        label.set_margin_start(6)
        label.set_margin_end(6)
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        self.set_child(label)

class RateConfigsHelpWindow(Gtk.Window):
    def __init__(self, parent):
        super().__init__(title="NBFC Rated Configs Help", modal=False)

        self.set_default_size(400, 400)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(box)

        self.usage = RateConfigsHelpTextWidget(RATE_CONFIG_USAGE_TEXT)
        self.interpreting = RateConfigsHelpTextWidget(RATE_CONFIG_INTERPRETING_RESULTS_TEXT)

        self.notebook = Gtk.Notebook()
        self.notebook.append_page(self.usage, Gtk.Label(label='Usage'))
        self.notebook.append_page(self.interpreting, Gtk.Label(label='Interpreting Results'))
        box.append(self.notebook)

        button = Gtk.Button(label="Close")
        button.set_margin_start(10)
        button.set_margin_end(10)
        button.set_margin_bottom(10)
        button.connect("clicked", lambda button: self.close())
        box.append(button)
