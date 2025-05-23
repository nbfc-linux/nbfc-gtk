class SensorWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.fan_index = None

        # =====================================================================
        # Algorithm type
        # =====================================================================

        label = Gtk.Label(label="Algorithm:")
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        self.append(label)

        algorithm_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.append(algorithm_box)

        self.default_radio = Gtk.CheckButton(label="Default")
        self.default_radio.set_margin_start(6)
        self.default_radio.set_margin_end(6)
        self.default_radio.set_margin_top(6)
        self.default_radio.set_margin_bottom(6)
        self.default_radio.set_group(None)
        self.default_radio.set_active(True)
        algorithm_box.append(self.default_radio)

        self.average_radio = Gtk.CheckButton(label="Average")
        self.average_radio.set_margin_start(6)
        self.average_radio.set_margin_end(6)
        self.average_radio.set_margin_top(6)
        self.average_radio.set_margin_bottom(6)
        self.average_radio.set_group(self.default_radio)
        algorithm_box.append(self.average_radio)

        self.max_radio = Gtk.CheckButton(label="Max")
        self.max_radio.set_margin_start(6)
        self.max_radio.set_margin_end(6)
        self.max_radio.set_margin_top(6)
        self.max_radio.set_margin_bottom(6)
        self.max_radio.set_group(self.default_radio)
        algorithm_box.append(self.max_radio)

        self.min_radio = Gtk.CheckButton(label="Min")
        self.min_radio.set_margin_start(6)
        self.min_radio.set_margin_end(6)
        self.min_radio.set_margin_top(6)
        self.min_radio.set_margin_bottom(6)
        self.min_radio.set_group(self.default_radio)
        algorithm_box.append(self.min_radio)

        # =====================================================================
        # Temperature Sources
        # =====================================================================

        label = Gtk.Label(label="Temperature Sources:")
        label.set_margin_start(6)
        label.set_margin_end(6)
        label.set_margin_top(6)
        label.set_margin_bottom(6)
        self.append(label)

        self.temperature_sources = SimpleListView()
        self.temperature_sources.set_vexpand(True)
        self.append(self.temperature_sources)

        # =====================================================================
        # Sensors
        # =====================================================================

        self.sensors = SimpleDropDown()
        self.sensors.set_margin_start(6)
        self.sensors.set_margin_end(6)
        self.sensors.set_margin_top(6)
        self.sensors.set_margin_bottom(6)
        self.sensors.connect("notify::selected-item", self.sensors_changed)
        self.append(self.sensors)

        # =====================================================================
        # Custom sensor
        # =====================================================================

        self.custom_sensor = Gtk.Entry()
        self.custom_sensor.set_margin_start(6)
        self.custom_sensor.set_margin_end(6)
        self.custom_sensor.set_margin_top(6)
        self.custom_sensor.set_margin_bottom(6)
        self.custom_sensor.set_visible(False)
        self.append(self.custom_sensor)

        # =====================================================================
        # Buttons
        # =====================================================================

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.set_hexpand(True)
        self.append(button_box)

        self.add_button = Gtk.Button(label="Add")
        self.add_button.set_hexpand(True)
        self.add_button.set_margin_start(6)
        self.add_button.set_margin_end(6)
        self.add_button.set_margin_top(6)
        self.add_button.set_margin_bottom(6)
        self.add_button.connect("clicked", self.add_button_clicked)
        button_box.append(self.add_button)

        self.del_button = Gtk.Button(label="Delete")
        self.del_button.set_hexpand(True)
        self.del_button.set_margin_start(6)
        self.del_button.set_margin_end(6)
        self.del_button.set_margin_top(6)
        self.del_button.set_margin_bottom(6)
        self.del_button.connect("clicked", self.del_button_clicked)
        button_box.append(self.del_button)

    def set_fan_index(self, index):
        self.fan_index = index

    def set_available_sensors(self, available_sensors):
        for sensor in available_sensors:
            self.sensors.add(sensor.name, "%s (%s)" % (sensor.name, sensor.description))

        self.sensors.add("<command>", "Custom Shell Command")
        self.sensors.add("<custom>", "Custom Sensor or File")

    def update(self, fan_temperature_source):
        {
            'Default': self.default_radio,
            'Average': self.average_radio,
            'Max':     self.max_radio,
            'Min':     self.min_radio
        }[fan_temperature_source.get('TemperatureAlgorithmType', 'Default')].set_active(True)

        self.temperature_sources.model.remove_all()

        for sensor in fan_temperature_source.get('Sensors', []):
            try:
                item = self.find_sensor_item(sensor)
                self.temperature_sources.add(item.getKey(), item.getValue())
            except Exception as e:
                print(e) # TODO
                self.temperature_sources.add(sensor, sensor)

    def find_sensor_item(self, sensor):
        for i in range(self.sensors.model.get_n_items()):
            item = self.sensors.model.get_item(i)
            if item.getKey() == sensor:
                return item

        raise Exception('No sensor found for %s' % sensor)

    def sensors_changed(self, *_):
        item = self.sensors.get_selected_item()

        if item.getKey() == '<custom>':
            self.custom_sensor.set_visible(True)
            self.custom_sensor.set_placeholder_text("Sensor Name or File")
        elif item.getKey() == '<command>':
            self.custom_sensor.set_visible(True)
            self.custom_sensor.set_placeholder_text("Shell Command")
        else:
            self.custom_sensor.set_visible(False)

    def add_button_clicked(self, _):
        item = self.sensors.get_selected_item()

        if item.getKey() == '<custom>':
            key = self.custom_sensor.get_text()
            val = key
        elif item.getKey() == '<command>':
            key = '$ %s' % self.custom_sensor.get_text()
            val = key
        else:
            key = item.getKey()
            val = item.getValue()

        self.temperature_sources.add(key, val)

    def del_button_clicked(self, _):
        idx = self.temperature_sources.get_selected_idx()
        if idx >= 0 and idx < self.temperature_sources.model.get_n_items():
            self.temperature_sources.model.remove(idx)

    def get_config(self):
        sensors = []
        for i in range(self.temperature_sources.model.get_n_items()):
            item = self.temperature_sources.model.get_item(i)
            sensors.append(item.getKey())

        algorithm = None
        if self.average_radio.get_active():
            algorithm = 'Average'
        elif self.max_radio.get_active():
            algorithm = 'Max'
        elif self.min_radio.get_active():
            algorithm = 'Min'

        cfg = {'FanIndex': self.fan_index}

        if algorithm:
            cfg['TemperatureAlgorithmType'] = algorithm

        if sensors:
            cfg['Sensors'] = sensors

        return cfg
