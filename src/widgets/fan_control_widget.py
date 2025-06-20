class FanControlWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # =====================================================================
        # Timer
        # =====================================================================

        self.timer_id = None

        # =====================================================================
        # Error Widget
        # =====================================================================

        self.error_label = Gtk.Label()
        self.error_label.set_hexpand(True)
        self.error_label.set_vexpand(True)
        self.append(self.error_label)

        # =====================================================================
        # Contents
        # =====================================================================

        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_vexpand(True)
        self.scrolled.set_hexpand(True)
        self.append(self.scrolled)

        self.widgets = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scrolled.set_child(self.widgets)

    # =========================================================================
    # Widget start / stop
    # =========================================================================

    def start(self):
        self.update()

        if self.timer_id is None:
            self.timer_id = GLib.timeout_add(500, self.update)

    def stop(self):
        if self.timer_id is not None:
            GLib.source_remove(self.timer_id)
            self.timer_id = None

    # =========================================================================
    # Helper functions
    # =========================================================================

    def update(self):
        try:
            status = GLOBALS.nbfc_client.get_status()
            self.scrolled.set_visible(True)
            self.error_label.set_visible(False)
        except Exception as e:
            self.scrolled.set_visible(False)
            self.error_label.set_visible(True)
            self.error_label.set_text(str(e))
            self.timer_id = None
            return False

        while len(get_children(self.widgets)) < len(status['Fans']):
            widget = FanWidget()
            self.widgets.append(widget)

        while len(get_children(self.widgets)) > len(status['Fans']):
            widget = get_children(self.widgets)[-1]
            self.widgets.remove(widget)

        for fan_index, fan_data in enumerate(status['Fans']):
            widget = get_children(self.widgets)[fan_index]
            widget.update(fan_index, fan_data)

        return True
