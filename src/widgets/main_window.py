class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        # =====================================================================
        # Title and Geometry
        # =====================================================================

        self.set_title("NBFC Client")
        self.set_default_size(400, 600)

        # =====================================================================
        # Box (vertical)
        # =====================================================================

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(vbox)

        # =====================================================================
        # Menu
        # =====================================================================

        # Menu model
        menu_model = Gio.Menu()
        
        # Application menu
        app_menu = Gio.Menu()

        # About
        about_entry = app_menu.append("About", "win.about")
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", lambda *_: self.showAbout())
        self.add_action(about_action)

        # Quit
        quit_entry = app_menu.append("Quit", "win.quit")
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", lambda *_: self.close())
        self.add_action(quit_action)

        menu_model.append_submenu("Application", app_menu)

        # Menu bar
        menubar = Gtk.PopoverMenuBar.new_from_model(menu_model)
        vbox.append(menubar)

        # =====================================================================
        # Tab widget
        # =====================================================================

        self.notebook = Gtk.Notebook()
        self.notebook.set_margin_start(12)
        self.notebook.set_margin_end(12)
        self.notebook.set_margin_top(12)
        self.notebook.set_margin_bottom(12)
        self.notebook.connect('switch-page', self.notebook_tab_changed)
        vbox.append(self.notebook)

        # =====================================================================
        # Tabs
        # =====================================================================

        self.widgets = {}
        self.widgets['service'] = ServiceControlWidget()
        self.widgets['fans']    = FanControlWidget()
        self.widgets['basic']   = BasicConfigWidget()
        self.widgets['sensors'] = SensorsWidget()
        self.widgets['update']  = UpdateWidget()

        self.notebook.append_page(self.widgets['service'], Gtk.Label(label='Service'))
        self.notebook.append_page(self.widgets['fans'],    Gtk.Label(label='Fans'))
        self.notebook.append_page(self.widgets['basic'],   Gtk.Label(label='Basic Configuration'))
        self.notebook.append_page(self.widgets['sensors'], Gtk.Label(label='Sensors'))
        self.notebook.append_page(self.widgets['update'],  Gtk.Label(label='Update'))

    # =========================================================================
    # Public functions
    # =========================================================================

    def setTabById(self, id_):
        widget = self.widgets[id_]
        page_num = self.notebook.page_num(widget)
        self.notebook.set_current_page(page_num)

    # =========================================================================
    # Signal functions
    # =========================================================================

    def notebook_tab_changed(self, notebook, page, page_num):
        for i in range(self.notebook.get_n_pages()):
            widget = self.notebook.get_nth_page(i)
            
            if i == page_num:
                widget.start()
            else:
                widget.stop()

    def showAbout(self, *_):
        dialog = AboutWidget(self)
        dialog.present()
