class FanWidget(Gtk.Frame):
    def __init__(self):
        super().__init__()

        self.fan_index = None

        # =====================================================================
        # Layout
        # =====================================================================

        self.set_margin_start(6)
        self.set_margin_end(6)
        self.set_margin_top(6)
        self.set_margin_bottom(6)

        # =====================================================================
        # Grid box
        # =====================================================================

        grid_box = Gtk.Grid()
        grid_box.set_margin_top(6)
        grid_box.set_margin_bottom(6)
        grid_box.set_halign(Gtk.Align.CENTER)
        grid_box.set_column_homogeneous(True)
        self.set_child(grid_box)

        # =====================================================================
        # Grid content
        # =====================================================================

        label = Gtk.Label(label="Fan name")
        self.name_label = Gtk.Label()
        grid_box.attach(label, 0, 0, 1, 1)
        grid_box.attach(self.name_label, 1, 0, 1, 1)

        label = Gtk.Label(label="Temperature")
        self.temperature_label = Gtk.Label()
        grid_box.attach(label, 0, 1, 1, 1)
        grid_box.attach(self.temperature_label, 1, 1, 1, 1)

        label = Gtk.Label(label="Auto mode")
        self.auto_mode_label = Gtk.Label()
        grid_box.attach(label, 0, 2, 1, 1)
        grid_box.attach(self.auto_mode_label, 1, 2, 1, 1)

        label = Gtk.Label(label="Critical")
        self.critical_label = Gtk.Label()
        grid_box.attach(label, 0, 3, 1, 1)
        grid_box.attach(self.critical_label, 1, 3, 1, 1)

        label = Gtk.Label(label="Current speed")
        self.current_speed_label = Gtk.Label()
        grid_box.attach(label, 0, 4, 1, 1)
        grid_box.attach(self.current_speed_label, 1, 4, 1, 1)

        label = Gtk.Label(label="Target speed")
        self.target_speed_label = Gtk.Label()
        grid_box.attach(label, 0, 5, 1, 1)
        grid_box.attach(self.target_speed_label, 1, 5, 1, 1)

        label = Gtk.Label(label="Speed steps")
        self.speed_steps_label = Gtk.Label()
        grid_box.attach(label, 0, 6, 1, 1)
        grid_box.attach(self.speed_steps_label, 1, 6, 1, 1)

        # =====================================================================
        # Auto mode checkbox
        # =====================================================================

        self.auto_mode_checkbox = Gtk.CheckButton(label="Auto mode")
        self.auto_mode_checkbox.connect("toggled", self.update_fan_speed)
        grid_box.attach(self.auto_mode_checkbox, 0, 7, 2, 1)
        
        # =====================================================================
        # Speed slider
        # =====================================================================

        adjustment = Gtk.Adjustment(value=0, lower=0, upper=100, step_increment=1, page_increment=10, page_size=0)
        self.speed_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        self.speed_scale.set_hexpand(True)
        self.speed_scale.set_value_pos(Gtk.PositionType.RIGHT)
        self.speed_scale.set_digits(0)
        self.speed_scale.connect("value-changed", self.update_fan_speed)
        grid_box.attach(self.speed_scale, 0, 8, 2, 1)

    # =========================================================================
    # Helper functions
    # =========================================================================

    def update(self, fan_index, fan_data):
        self.fan_index = fan_index
        self.name_label.set_text(fan_data['Name'])
        self.temperature_label.set_text(str(fan_data['Temperature']))
        self.auto_mode_label.set_text(str(fan_data['AutoMode']))
        self.critical_label.set_text(str(fan_data['Critical']))
        self.current_speed_label.set_text(str(fan_data['CurrentSpeed']))
        self.target_speed_label.set_text(str(fan_data['TargetSpeed']))
        self.speed_steps_label.set_text(str(fan_data['SpeedSteps']))

        # Block signals to avoid triggering during update
        self.auto_mode_checkbox.handler_block_by_func(self.update_fan_speed)
        self.speed_scale.handler_block_by_func(self.update_fan_speed)

        self.auto_mode_checkbox.set_active(fan_data['AutoMode'])
        self.speed_scale.set_value(int(fan_data['RequestedSpeed']))

        # Unblock signals after update
        self.auto_mode_checkbox.handler_unblock_by_func(self.update_fan_speed)
        self.speed_scale.handler_unblock_by_func(self.update_fan_speed)

    # =========================================================================
    # Signal functions
    # =========================================================================

    def update_fan_speed(self, *_):
        auto_mode = self.auto_mode_checkbox.get_active()

        if auto_mode:
            GLOBALS.nbfc_client.set_fan_speed('auto', self.fan_index)
        else:
            GLOBALS.nbfc_client.set_fan_speed(self.speed_scale.get_value(), self.fan_index)

        self.speed_scale.set_sensitive(not auto_mode)
