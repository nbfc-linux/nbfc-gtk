class ServiceControlWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # =====================================================================
        # Timer
        # =====================================================================

        self.timer_id = None

        # =====================================================================
        # Service Status
        # =====================================================================

        self.status_label = Gtk.Label()
        self.status_label.set_margin_start(6)
        self.status_label.set_margin_end(6)
        self.status_label.set_margin_top(6)
        self.status_label.set_margin_bottom(6)
        self.append(self.status_label)

        # =====================================================================
        # Service Log
        # =====================================================================

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_margin_start(6)
        scrolled.set_margin_end(6)
        scrolled.set_margin_top(6)
        scrolled.set_margin_bottom(6)
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        self.append(scrolled)

        self.log = Gtk.TextView()
        self.log.set_editable(False)
        scrolled.set_child(self.log)

        # =====================================================================
        # Read-Only Checkbox
        # =====================================================================

        self.read_only_checkbox = Gtk.CheckButton(label="Start in read-only mode")
        self.read_only_checkbox.set_margin_start(6)
        self.read_only_checkbox.set_margin_end(6)
        self.read_only_checkbox.set_margin_top(6)
        self.read_only_checkbox.set_margin_bottom(6)
        self.append(self.read_only_checkbox)

        # =====================================================================
        # Buttons
        # =====================================================================

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(hbox)

        self.start_button = Gtk.Button(label="Start")
        self.start_button.set_margin_start(6)
        self.start_button.set_margin_end(6)
        self.start_button.set_margin_top(6)
        self.start_button.set_margin_bottom(6)
        self.start_button.set_hexpand(True)
        self.start_button.connect("clicked", self.start_button_clicked)
        hbox.append(self.start_button)

        self.stop_button = Gtk.Button(label="Stop")
        self.stop_button.set_margin_start(6)
        self.stop_button.set_margin_end(6)
        self.stop_button.set_margin_top(6)
        self.stop_button.set_margin_bottom(6)
        self.stop_button.set_hexpand(True)
        self.stop_button.connect("clicked", self.stop_button_clicked)
        hbox.append(self.stop_button)

        # =====================================================================
        # Message label
        # =====================================================================

        self.message = Gtk.Label()
        self.message.set_margin_start(6)
        self.message.set_margin_end(6)
        self.message.set_margin_top(6)
        self.message.set_margin_bottom(6)
        self.append(self.message)

        # =====================================================================
        # Init
        # =====================================================================

        GLOBALS.connect("restart_service", self.service_restart_signal)

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
            GLOBALS.nbfc_client.get_status()
            self.status_label.set_markup("<b>Running</b>")
            self.start_button.set_sensitive(False)
            self.stop_button.set_sensitive(True)
        except Exception as e:
            self.status_label.set_markup("<b>Stopped</b>")
            self.start_button.set_sensitive(True)
            self.stop_button.set_sensitive(False)

        if not GLOBALS.is_root:
            self.read_only_checkbox.set_sensitive(False)
            self.start_button.set_sensitive(False)
            self.stop_button.set_sensitive(False)
            self.message.set_visible(True)
            self.message.set_text(CANNOT_CONTROL_MSG)
        else:
            self.message.set_visible(False)

        return True

    def call_with_log(self, args):
        self.log.get_buffer().set_text("")

        # We need to attach the worker thread to the class instance
        # because it would get destroyed otherwise
        self.worker = SubprocessWorker(args)
        self.worker.connect("output_line", self.handle_output)
        self.worker.connect("error_line", self.handle_output)
        self.worker.start()

    def handle_output(self, _, line):
        buffer = self.log.get_buffer()
        buffer.insert(buffer.get_end_iter(), '%s\n' % line.rstrip())

    def service_start(self, readonly):
        args = ['nbfc', 'start']

        if readonly:
            args.append('-r')

        self.call_with_log(args)

    def service_restart(self, readonly):
        args = ['nbfc', 'restart']

        if readonly:
            args.append('-r')

        self.call_with_log(args)

    def service_stop(self):
        GLOBALS.nbfc_client.stop()

    # =========================================================================
    # Signal functions
    # =========================================================================

    def service_restart_signal(self, _, readonly):
        self.service_restart(readonly)

    def start_button_clicked(self, _):
        self.service_start(self.read_only_checkbox.get_active())

    def stop_button_clicked(self, _):
        self.service_stop()
