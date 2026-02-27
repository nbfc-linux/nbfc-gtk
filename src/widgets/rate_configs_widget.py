def RegisterType_To_HumanReadable(s):
    if s == 'FanReadRegister':
        return 'Fan read register'

    if s == 'FanWriteRegister':
        return 'Fan write register'

    if s == 'RegisterWriteConfigurationRegister':
        return 'Misc register'

    return '?'

def RegisterScore_To_HumanReadable(s):
    if s == 'FullMatch':
        return 'FULL MATCH'

    if s == 'PartialMatch':
        return 'PARTIAL MATCH'

    if s == 'MinimalMatch':
        return 'MINIMAL MATCH'

    if s == 'NoMatch':
        return 'NO MATCH'

    if s == 'NotFound':
        return 'NOT FOUND'

    if s == 'BadRegister':
        return 'BAD REGISTER'

    return '?'

def MethodScore_To_HumanReadable(s):
    if s == 'Found':
        return 'FOUND'

    if s == 'NotFound':
        return 'NOT FOUND'

    return '?'

class RegisterRating(Gtk.Grid):
    def __init__(self, data):
        super().__init__()
        self.set_column_homogeneous(True)
        self.set_margin_top(6)
        self.set_margin_bottom(6)

        # =====================================================================
        # Info
        # =====================================================================

        off = data['offset']
        self.attach(Gtk.Label(label="Register Offset"),        0, 0, 1, 1)
        self.attach(Gtk.Label(label="%d (0x%X)" % (off, off)), 1, 0, 1, 1)

        typ = RegisterType_To_HumanReadable(data['type'])
        self.attach(Gtk.Label(label="Type"),  0, 1, 1, 1)
        self.attach(Gtk.Label(label=typ),     1, 1, 1, 1)

        score = RegisterScore_To_HumanReadable(data['score'])
        self.attach(Gtk.Label(label="Score"), 0, 2, 1, 1)
        self.attach(Gtk.Label(label=score),   1, 2, 1, 1)

        if 'info' in data:
            name = data['info']['name']
            self.attach(Gtk.Label(label="Name"), 0, 3, 1, 1)
            self.attach(Gtk.Label(label=name),   1, 3, 1, 1)

class MethodRating(Gtk.Grid):
    def __init__(self, data):
        super().__init__()
        self.set_column_homogeneous(True)
        self.set_margin_top(6)
        self.set_margin_bottom(6)

        # =====================================================================
        # Info
        # =====================================================================

        call = data['call']
        self.attach(Gtk.Label(label="Method call"), 0, 0, 1, 1)
        self.attach(Gtk.Label(label=call),          1, 0, 1, 1)

        score = MethodScore_To_HumanReadable(data['score'])
        self.attach(Gtk.Label(label="Score"), 0, 1, 1, 1)
        self.attach(Gtk.Label(label=score),   1, 1, 1, 1)

class RateConfigDetails(Gtk.Box):
    def __init__(self, data):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        # =====================================================================
        # Register ratings
        # =====================================================================

        for rating in data['rating']['register_ratings']:
            self.append(RegisterRating(rating))

        # =====================================================================
        # Method ratings
        # =====================================================================

        for rating in data['rating']['method_ratings']:
            self.append(MethodRating(rating))

class RateConfigDetailsWindow(Gtk.Window):
    def __init__(self, data):
        super().__init__()

        # =====================================================================
        # Title and Geometry
        # =====================================================================

        self.set_title("Rating Details")
        self.set_default_size(400, 400)

        # =====================================================================
        # Box (vertical)
        # =====================================================================

        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(layout)

        # =====================================================================
        # Score
        # =====================================================================

        label = Gtk.Label(label="Score: %.2f / 10" % data['rating']['score'])
        label.set_margin_start(6)
        label.set_margin_end(6)
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        layout.append(label)
        
        # =====================================================================
        # Files
        # =====================================================================

        self.files_combobox = SimpleDropDown()
        self.files_combobox.set_margin_start(6)
        self.files_combobox.set_margin_end(6)
        self.files_combobox.set_margin_top(6)
        self.files_combobox.set_margin_bottom(6)
        layout.append(self.files_combobox)
        for file in data['files']:
            self.files_combobox.add(file, file)

        # =====================================================================
        # ScrollArea
        # =====================================================================

        self.scroll_area = Gtk.ScrolledWindow()
        self.scroll_area.set_hexpand(True)
        self.scroll_area.set_vexpand(True)
        layout.append(self.scroll_area)

        # =====================================================================
        # RateConfigDetails
        # =====================================================================

        self.rate_config_details = RateConfigDetails(data)
        self.rate_config_details.set_margin_start(6)
        self.rate_config_details.set_margin_end(6)
        self.rate_config_details.set_margin_top(6)
        self.rate_config_details.set_margin_bottom(6)
        self.scroll_area.set_child(self.rate_config_details)

        # =====================================================================
        # Apply buttons widget
        # =====================================================================

        self.apply_buttons_widget = ApplyButtonsWidget()
        self.apply_buttons_widget.save_button.connect("clicked", self.save_button_clicked)
        self.apply_buttons_widget.apply_button.connect("clicked", self.apply_button_clicked)
        self.apply_buttons_widget.enable()
        layout.append(self.apply_buttons_widget)

    # =========================================================================
    # Signal functions
    # =========================================================================

    def save_button_clicked(self, button):
        selected_config = self.files_combobox.get_selected_item().getKey()
        GLOBALS.set_model_config(selected_config)

    def apply_button_clicked(self, button):
        selected_config = self.files_combobox.get_selected_item().getKey()
        read_only = self.apply_buttons_widget.read_only_checkbox.get_active()
        GLOBALS.set_model_config_and_restart(selected_config, read_only)

class RateConfigsWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.configs = []

        # =====================================================================
        # Threshold spin box + Load button
        # =====================================================================

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_hexpand(True)
        self.append(hbox)

        label = Gtk.Label(label="Minimum score")
        label.set_margin_start(6)
        label.set_margin_end(6)
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        label.set_hexpand(True)

        self.threshold_spin = Gtk.SpinButton.new_with_range(0.0, 10.0, 0.1)
        self.threshold_spin.set_value(9.0)
        self.threshold_spin.connect("value-changed", self.threshold_spin_changed)
        self.threshold_spin.set_margin_start(6)
        self.threshold_spin.set_margin_end(6)
        self.threshold_spin.set_margin_top(6)
        self.threshold_spin.set_margin_bottom(6)

        self.load_button = Gtk.Button(label="Load configs")
        self.load_button.connect("clicked", self.load_button_clicked)
        self.load_button.set_margin_end(6)
        self.load_button.set_margin_top(6)
        self.load_button.set_margin_bottom(6)

        hbox.append(label)
        hbox.append(self.threshold_spin)
        hbox.append(self.load_button)

        # =====================================================================
        # Warning label
        # =====================================================================

        self.warning_label = Gtk.Label(label="Warning! Unsafe configurations are shown")
        self.warning_label.add_css_class("warning-label")
        css = """
            .warning-label {
                background-color: #cc0000;
                color: white;
                font-weight: bold;
                padding: 3px;
            }
        """

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css.encode('UTF-8'))

        Gtk.StyleContext.add_provider_for_display(
            self.get_display(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.warning_label.set_visible(False)
        self.append(self.warning_label)

        # =====================================================================
        # Rated Configs
        # =====================================================================

        self.rated_configs_list = SimpleListView()
        self.rated_configs_list.list_view.set_vexpand(True)
        self.rated_configs_list.list_view.connect("activate", self.rate_configs_on_activate)
        self.rated_configs_list.selection.connect("selection-changed", self.rate_configs_item_changed)
        self.append(self.rated_configs_list)

        # =====================================================================
        # Buttons
        # =====================================================================

        self.show_button = Gtk.Button(label="Show details")
        self.show_button.connect("clicked", self.show_button_clicked)
        self.show_button.set_margin_start(6)
        self.show_button.set_margin_end(6)
        self.show_button.set_margin_top(6)
        self.show_button.set_margin_bottom(6)
        self.show_button.set_sensitive(False)
        self.append(self.show_button)

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

    def load_rated_configs_list(self):
        try:
            configs = GLOBALS.nbfc_client.rate_configs()
        except NbfcClientError as e:
            show_error_message(self, "Error", str(e))
            return

        configs = sorted(configs, key=lambda o: o['rating']['priority'], reverse=True)
        configs = sorted(configs, key=lambda o: o['rating']['score'], reverse=True)
        self.configs = configs
        self.show_rated_configs_list()

    def show_rated_configs_list(self):
        self.rated_configs_list.model.remove_all()
        min_score = self.threshold_spin.get_value()

        for i, data in enumerate(self.configs):
            if data['rating']['score'] < min_score:
                continue

            text = '%s (%.2f / 10)' % (data['files'][0], data['rating']['score'])
            self.rated_configs_list.add(i, text)

        n_items = self.rated_configs_list.model.get_n_items()
        self.show_button.set_sensitive(n_items >= 1)

    def show_details(self, data):
        self.details_widget = RateConfigDetailsWindow(data)
        self.details_widget.present()

    # =========================================================================
    # Signal functions
    # =========================================================================

    def rate_configs_item_changed(self, selection, position, n_items):
        item = selection.get_selected_item()
        self.show_button.set_sensitive(item is not None)

    def rate_configs_on_activate(self, list_view, index):
        self.show_details(self.configs[index])

    def load_button_clicked(self, button):
        self.load_rated_configs_list()

    def threshold_spin_changed(self, spin):
        self.warning_label.set_visible(self.threshold_spin.get_value() < 9.0)
        self.show_rated_configs_list()

    def show_button_clicked(self, button):
        cur = self.rated_configs_list.get_selected_id()
        if cur is None:
            return

        self.show_details(self.configs[cur])
