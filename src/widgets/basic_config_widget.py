CONFIRMATION_TEXT = """\
You are about to view configurations with names similar to your laptop model.

Please note that similar model names do not guarantee compatibility. The register configuration may be completely different.

Using a configuration that does <b>not exactly match</b> your laptop model can be <b>very dangerous and may cause hardware damage.</b>

Please use the <b>Rated Configs</b> tab to find verified configuration recommendations for your device."""

class ConfirmationDialog(Gtk.Window):
    def __init__(self, callback, parent):
        super().__init__(title="Warning", transient_for=parent, modal=True)
        self.callback = callback

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(box)

        label = Gtk.Label()
        label.set_wrap(True)
        label.set_max_width_chars(40)
        label.set_markup(CONFIRMATION_TEXT)
        label.set_margin_start(6)
        label.set_margin_end(6)
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        box.append(label)

        self.checkbox = Gtk.CheckButton(label="I understand the risks")
        self.checkbox.set_margin_start(6)
        self.checkbox.set_margin_end(6)
        self.checkbox.set_margin_top(6)
        self.checkbox.set_margin_bottom(6)
        box.append(self.checkbox)

        button = Gtk.Button(label="Close")
        button.set_margin_start(6)
        button.set_margin_end(6)
        button.set_margin_top(6)
        button.set_margin_bottom(6)
        button.connect("clicked", self.close_clicked)
        box.append(button)

    def close_clicked(self, button):
        self.callback(self.checkbox.get_active())
        self.close()

class BasicConfigWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.confirmed_risks = False

        # =====================================================================
        # Model label
        # =====================================================================

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(hbox)

        label = Gtk.Label(label="Your laptop model:")
        label.set_hexpand(True)
        label.set_margin_start(6)
        label.set_margin_end(6)
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        hbox.append(label)

        self.model_name_label = Gtk.Label()
        self.model_name_label.set_hexpand(True)
        self.model_name_label.set_margin_start(6)
        self.model_name_label.set_margin_end(6)
        self.model_name_label.set_margin_top(6)
        self.model_name_label.set_margin_bottom(6)
        hbox.append(self.model_name_label)

        # =====================================================================
        # Selected config input + Reset
        # =====================================================================

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(hbox)

        self.selected_config_input = Gtk.Entry()
        self.selected_config_input.set_placeholder_text("Configuration File")
        self.selected_config_input.set_hexpand(True)
        self.selected_config_input.set_margin_start(6)
        self.selected_config_input.set_margin_end(6)
        self.selected_config_input.set_margin_top(6)
        self.selected_config_input.set_margin_bottom(6)
        self.selected_config_input.connect("changed", self.update_apply_buttons)
        hbox.append(self.selected_config_input)

        self.reset_button = Gtk.Button(label="Reset")
        self.reset_button.set_margin_start(6)
        self.reset_button.set_margin_end(6)
        self.reset_button.set_margin_top(6)
        self.reset_button.set_margin_bottom(6)
        self.reset_button.connect("clicked", self.reset_button_clicked)
        hbox.append(self.reset_button)

        # =====================================================================
        # Radio Buttons
        # =====================================================================

        self.list_all_radio = Gtk.CheckButton(label="List all configurations")
        self.list_all_radio.set_margin_start(6)
        self.list_all_radio.set_margin_end(6)
        self.list_all_radio.set_margin_top(6)
        self.list_all_radio.set_margin_bottom(6)
        self.list_all_radio.set_group(None)
        self.list_all_radio.set_active(True)
        self.list_all_radio.connect("toggled", self.list_all_radio_checked)
        self.append(self.list_all_radio)

        self.list_recommended_radio = Gtk.CheckButton(label="List similar named configurations")
        self.list_recommended_radio.set_margin_start(6)
        self.list_recommended_radio.set_margin_end(6)
        self.list_recommended_radio.set_margin_top(6)
        self.list_recommended_radio.set_margin_bottom(6)
        self.list_recommended_radio.set_group(self.list_all_radio)
        self.list_recommended_radio.connect("toggled", self.list_recommended_radio_checked)
        self.append(self.list_recommended_radio)

        self.custom_file_radio = Gtk.CheckButton(label="Custom file")
        self.custom_file_radio.set_margin_start(6)
        self.custom_file_radio.set_margin_end(6)
        self.custom_file_radio.set_margin_top(6)
        self.custom_file_radio.set_margin_bottom(6)
        self.custom_file_radio.set_group(self.list_all_radio)
        self.custom_file_radio.connect("toggled", self.custom_file_radio_checked)
        self.append(self.custom_file_radio)

        # =====================================================================
        # Model selection combo box + Set button
        # =====================================================================

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(hbox)

        self.configurations_dropdown = SimpleDropDown()
        self.configurations_dropdown.set_margin_start(6)
        self.configurations_dropdown.set_margin_end(6)
        self.configurations_dropdown.set_margin_top(6)
        self.configurations_dropdown.set_margin_bottom(6)
        self.configurations_dropdown.set_hexpand(True)
        hbox.append(self.configurations_dropdown)

        self.set_button = Gtk.Button(label="Set")
        self.set_button.set_margin_start(6)
        self.set_button.set_margin_end(6)
        self.set_button.set_margin_top(6)
        self.set_button.set_margin_bottom(6)
        self.set_button.connect("clicked", self.set_button_clicked)
        hbox.append(self.set_button)

        # =====================================================================
        # File selection
        # =====================================================================

        self.select_file_button = Gtk.Button(label="Select file ...")
        self.select_file_button.set_margin_start(6)
        self.select_file_button.set_margin_end(6)
        self.select_file_button.set_margin_top(6)
        self.select_file_button.set_margin_bottom(6)
        self.select_file_button.set_hexpand(True)
        self.select_file_button.connect("clicked", self.select_file_button_clicked)
        self.append(self.select_file_button)

        # =====================================================================
        # Stretch
        # =====================================================================

        stretch = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        stretch.set_vexpand(True)
        self.append(stretch)

        # =====================================================================
        # Apply buttons
        # =====================================================================

        self.apply_buttons_widget = ApplyButtonsWidget()
        self.apply_buttons_widget.save_button.connect("clicked", self.save_button_clicked)
        self.apply_buttons_widget.apply_button.connect("clicked", self.apply_button_clicked)
        self.append(self.apply_buttons_widget)

        # =====================================================================
        # Initialization
        # =====================================================================

        self.list_all_radio_checked(None)
        self.update_apply_buttons()

        try:
            self.reset_config()
        except:
            pass

        try:
            model = GLOBALS.nbfc_client.get_model_name()
            self.model_name_label.set_markup(f"<b>{model}</b>")
        except:
            self.model_name_label.set_markupText("<b>Could not get model name</b>")

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

    def update_apply_buttons(self, *_):
        if not GLOBALS.is_root:
            self.apply_buttons_widget.disable(CANNOT_CONFIGURE_MSG)
        elif not self.selected_config_input.get_text():
            self.apply_buttons_widget.disable("No model configuration selected")
        else:
            self.apply_buttons_widget.enable()

    def reset_config(self):
        '''
        Reset the `SelectedConfigId` field to its original value.

        This may raise an exception.
        '''

        config = GLOBALS.nbfc_client.get_service_config()

        SelectedConfigId = config.get('SelectedConfigId', '')

        self.selected_config_input.set_text(SelectedConfigId)

    def update_configuration_combobox(self, available_configs):
        self.configurations_dropdown.model.remove_all()

        for config in available_configs:
            self.configurations_dropdown.add(config, config)

        if self.configurations_dropdown.model.get_n_items():
            self.set_button.set_sensitive(True)
        else:
            self.set_button.set_sensitive(False)

    # =========================================================================
    # Signal functions
    # =========================================================================

    def reset_button_clicked(self, _):
        try:
            self.reset_config()
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def save_button_clicked(self, _):
        model_config = self.selected_config_input.get_text()

        try:
            GLOBALS.set_model_config(model_config)
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def apply_button_clicked(self, _):
        model_config = self.selected_config_input.get_text()
        read_only = self.apply_buttons_widget.read_only_checkbox.get_active()

        try:
            GLOBALS.set_model_config_and_restart(model_config, read_only)
        except Exception as e:
            show_error_message(self, "Error", str(e))

    def list_all_radio_checked(self, _):
        if not self.list_all_radio.get_active():
            return

        self.select_file_button.set_visible(False)
        self.configurations_dropdown.set_visible(True)
        self.set_button.set_visible(True)

        configs = GLOBALS.nbfc_client.list_configs()
        self.update_configuration_combobox(configs)

    def list_recommended_radio_checked(self, _):
        if not self.list_recommended_radio.get_active():
            return

        if not self.confirmed_risks:
            def confirmation_dialog_exited(confirmed):
                if confirmed:
                    self.confirmed_risks = True
                    self.list_recommended_radio_checked(None)
                else:
                    self.list_all_radio.set_active(True)

            toplevel_window = self.get_ancestor(Gtk.Window)
            dialog = ConfirmationDialog(confirmation_dialog_exited, toplevel_window)
            dialog.present()
            return

        self.select_file_button.set_visible(False)
        self.configurations_dropdown.set_visible(True)
        self.set_button.set_visible(True)

        configs = GLOBALS.nbfc_client.recommended_configs()
        self.update_configuration_combobox(configs)

    def custom_file_radio_checked(self, _):
        if not self.custom_file_radio.get_active():
            return

        self.select_file_button.set_visible(True)
        self.set_button.set_visible(False)
        self.configurations_dropdown.set_visible(False)

    def set_button_clicked(self, _):
        item = self.configurations_dropdown.get_selected_item()
        if item:
            self.selected_config_input.set_text(item.getKey())

    def select_file_button_clicked(self, _):
        path = FileDialogHelper.get_open_filename(self, "Choose Configuration File", filters=[("JSON Files", "*.json")])
        if path:
            self.selected_config_input.set_text(path)
