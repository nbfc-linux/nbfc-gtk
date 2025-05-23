class SensorsWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        #GLOBALS.model_config_changed.connect(self.setup_ui) TODO

        # =====================================================================
        # Error Widget
        # =====================================================================

        self.error_widget = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append(self.error_widget)

        self.error_label = Gtk.Label()
        self.error_widget.append(self.error_label)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.error_widget.append(button_box)

        self.retry_button = Gtk.Button(label="Retry")
        self.retry_button.connect("clicked", self.retry_button_clicked)
        button_box.append(self.retry_button)

        self.fix_button = Gtk.Button(label="Fix errors automatically")
        self.fix_button.connect("clicked", self.fix_button_clicked)
        button_box.append(self.fix_button)

        # =====================================================================
        # Main Widget
        # =====================================================================

        self.main_widget = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append(self.main_widget)

        self.notebook = Gtk.Notebook()
        self.main_widget.append(self.notebook)

        self.apply_buttons_widget = ApplyButtonsWidget()
        self.apply_buttons_widget.save_button.connect("clicked", self.save_button_clicked)
        self.apply_buttons_widget.apply_button.connect("clicked", self.apply_button_clicked)
        self.main_widget.append(self.apply_buttons_widget)

        self.setup_ui()

    # =========================================================================
    # Widget start / stop
    # =========================================================================

    def start(self):
        pass

    def stop(self):
        pass

    # =========================================================================
    # Helper functions
    # =========================================================================

    def save(self):
        config = GLOBALS.nbfc_client.get_service_config()
        config['FanTemperatureSources'] = self.get_fan_temperature_sources()
        if not len(config['FanTemperatureSources']):
            del config['FanTemperatureSources']
        GLOBALS.nbfc_client.set_service_config(config)

    def setup_ui(self, fix_errors=False):
        if not GLOBALS.is_root:
            self.apply_buttons_widget.disable(CANNOT_CONFIGURE_MSG)
        else:
            self.apply_buttons_widget.enable()

        # =====================================================================
        # Get model configuration
        # =====================================================================

        try:
            config = GLOBALS.nbfc_client.get_service_config()
            fan_temperature_sources = config.get('FanTemperatureSources', [])
            model_config = GLOBALS.nbfc_client.get_model_configuration()
            self.error_widget.set_visible(False)
            self.main_widget.set_visible(True)
        except Exception as e:
            self.error_widget.set_visible(True)
            self.main_widget.set_visible(False)
            self.error_label.set_text(str(e))
            self.fix_button.set_sensitive(False)
            self.retry_button.set_sensitive(True)
            self.apply_buttons_widget.disable("")
            return

        # =====================================================================
        # Get available temperature sensors
        # =====================================================================

        available_sensors = GLOBALS.nbfc_client.get_available_sensors()

        # =====================================================================
        # Ensure that the FanTemperatureSources in the config are valid.
        # Give the user the chance to fix it or fix it automatically.
        # =====================================================================

        errors = validate_fan_temperature_sources(
            fan_temperature_sources,
            len(model_config['FanConfigurations']))

        if errors and not fix_errors:
            self.error_widget.set_visible(True) # TODO make function for this
            self.main_widget.set_visible(False)
            self.error_label.set_text('\n\n'.join(errors))
            self.fix_button.set_sensitive(True)
            self.retry_button.set_sensitive(True)
            self.apply_buttons_widget.disable("")
            return
        elif errors and fix_errors:
            fan_temperature_sources = fix_fan_temperature_sources(
                fan_temperature_sources,
                len(model_config['FanConfigurations']))

        self.error_widget.set_visible(False)
        self.main_widget.set_visible(True)

        # =====================================================================
        # Add widgets to self.tab_widget
        # =====================================================================

        while self.notebook.get_n_pages() < len(model_config['FanConfigurations']):
            widget = SensorWidget()
            self.notebook.append_page(widget, Gtk.Label())

        # TODO test this
        while self.notebook.get_n_pages() > len(model_config['FanConfigurations']):
            last = self.notebook.get_n_pages() - 1
            widget = self.notebook.get_nth_page(last)
            self.notebook.remove(widget)

        # =====================================================================
        # Set fan names to tabs
        # =====================================================================

        for i, fan_config in enumerate(model_config['FanConfigurations']):
            widget = self.notebook.get_nth_page(i)
            self.notebook.set_tab_label(widget, Gtk.Label(label=fan_config.get('FanDisplayName', 'Fan #%d' % i)))
            widget.set_available_sensors(available_sensors)
            widget.set_fan_index(i)

        # =====================================================================
        # Update TemperatureSourceWidget 
        # =====================================================================

        for fan_temperature_source in fan_temperature_sources:
            fan_index = fan_temperature_source['FanIndex']
            widget = self.notebook.get_nth_page(fan_index)
            widget.update(fan_temperature_source)

    def get_fan_temperature_sources(self):
        fan_temperature_sources = []

        for i in range(self.notebook.get_n_pages()):
            widget = self.notebook.get_nth_page(i)
            config = widget.get_config()

            # If FanTemperatureSource only has 'FanIndex', don't add it
            if len(config) > 1:
                fan_temperature_sources.append(config)

        return fan_temperature_sources

    # =========================================================================
    # Signal functions
    # =========================================================================

    def save_button_clicked(self, _):
        try:
            self.save()
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def apply_button_clicked(self, _):
        try:
            self.save()
            read_only = self.apply_buttons_widget.read_only_checkbox.get_active()
            GLib.idle_add(GLOBALS.emit, "restart_service", read_only)
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def fix_button_clicked(self, _):
        self.setup_ui(fix_errors=True)

    def retry_button_clicked(self, _):
        self.setup_ui(fix_errors=False)
