class UpdateWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # =====================================================================
        # Description
        # =====================================================================

        label = Gtk.Label(label="Fetch new configuration files from the internet")
        label.set_margin_start(6)
        label.set_margin_end(6)
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        self.append(label)

        # =====================================================================
        # Log
        # =====================================================================

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        self.append(scrolled)

        self.log = Gtk.TextView()
        self.log.set_editable(False)
        scrolled.set_child(self.log)

        # =====================================================================
        # Error message
        # =====================================================================

        self.error_label = Gtk.Label()
        self.error_label.set_margin_start(6)
        self.error_label.set_margin_end(6)
        self.error_label.set_margin_top(6)
        self.error_label.set_margin_bottom(6)
        self.append(self.error_label)

        # =====================================================================
        # Update button
        # =====================================================================

        self.update_button = Gtk.Button(label="Update")
        self.update_button.set_margin_start(6)
        self.update_button.set_margin_end(6)
        self.update_button.set_margin_top(6)
        self.update_button.set_margin_bottom(6)
        self.update_button.connect("clicked", self.update_button_clicked)
        self.append(self.update_button)

        # =====================================================================
        # Init code
        # =====================================================================

        if GLOBALS.is_root:
            self.error_label.set_visible(False)
        else:
            self.error_label.set_visible(True)
            self.error_label.set_text("You cannot update the configurations because you are not root")
            self.update_button.set_sensitive(False)

    # =========================================================================
    # Widget start / stop
    # =========================================================================

    def start(self):
        pass

    def stop(self):
        pass

    # =========================================================================
    # Signal functions
    # =========================================================================

    def handle_output(self, worker, line):
        buffer = self.log.get_buffer()
        end_iter = buffer.get_end_iter()
        buffer.insert(end_iter, '%s\n' % line.rstrip())

    def update_button_clicked(self, _):
        self.log.get_buffer().set_text("")
        self.update_button.set_sensitive(False)

        # We need to attach the worker thread to the class instance
        # because it would get destroyed otherwise
        self.worker = SubprocessWorker(['nbfc', 'update'])
        self.worker.connect("output_line", self.handle_output)
        self.worker.connect("error_line", self.handle_output)
        self.worker.connect("finished", self.command_finished)
        self.worker.start()

    def command_finished(self, worker, exitstatus):
        self.update_button.set_sensitive(True)
