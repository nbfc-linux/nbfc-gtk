class ApplyButtonsWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # =====================================================================
        # Read-only checkbox
        # =====================================================================

        self.read_only_checkbox = Gtk.CheckButton(label="(Re-)start in read-only mode")
        self.read_only_checkbox.set_margin_start(6)
        self.read_only_checkbox.set_margin_end(6)
        self.read_only_checkbox.set_margin_top(6)
        #self.read_only_checkbox.set_margin_bottom(6)
        self.append(self.read_only_checkbox)

        # =====================================================================
        # Save and Apply buttons
        # =====================================================================

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(hbox)

        self.save_button = Gtk.Button(label="Save")
        self.save_button.set_margin_start(6)
        self.save_button.set_margin_end(6)
        self.save_button.set_margin_top(6)
        self.save_button.set_margin_bottom(6)
        self.save_button.set_hexpand(True)
        hbox.append(self.save_button)

        self.apply_button = Gtk.Button(label="Apply with (re-)start")
        self.apply_button.set_margin_start(6)
        self.apply_button.set_margin_end(6)
        self.apply_button.set_margin_top(6)
        self.apply_button.set_margin_bottom(6)
        self.apply_button.set_hexpand(True)
        hbox.append(self.apply_button)

        # =====================================================================
        # Error label
        # =====================================================================

        self.error_label = Gtk.Label()
        self.error_label.set_margin_start(6)
        self.error_label.set_margin_end(6)
        self.error_label.set_margin_top(6)
        self.error_label.set_margin_bottom(6)
        self.append(self.error_label)

    def enable(self):
        self.error_label.set_visible(False)
        self.read_only_checkbox.set_sensitive(True)
        self.save_button.set_sensitive(True)
        self.apply_button.set_sensitive(True)

    def disable(self, reason):
        self.error_label.set_text(reason)
        self.error_label.set_visible(True)
        self.read_only_checkbox.set_sensitive(False)
        self.save_button.set_sensitive(False)
        self.apply_button.set_sensitive(False)
