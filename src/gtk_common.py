def get_children(container):
    children = []
    child = container.get_first_child()
    while child is not None:
        children.append(child)
        child = child.get_next_sibling()
    return children

class ErrorWidget(Gtk.Window):
    def __init__(self, parent, title, message):
        super().__init__(title=title, transient_for=parent, modal=True)

        # =====================================================================
        # Box (Vertical)
        # =====================================================================

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.set_margin_start(12)
        vbox.set_margin_end(12)
        vbox.set_margin_top(12)
        vbox.set_margin_bottom(12)
        self.set_child(vbox)

        # =====================================================================
        # Markup
        # =====================================================================

        desc = Gtk.Label()
        desc.set_margin_start(12)
        desc.set_margin_end(12)
        desc.set_margin_top(12)
        desc.set_margin_bottom(12)
        desc.set_text(message)
        vbox.append(desc)

        # =====================================================================
        # OK Button
        # =====================================================================

        ok_button = Gtk.Button(label="OK")
        ok_button.connect("clicked", lambda *_: self.close())
        vbox.append(ok_button)

        self.present()

def show_error_message(widget, title, message):
    if widget is not None:
        toplevel = widget.get_ancestor(Gtk.Window)
    else:
        toplevel = None

    dialog = ErrorWidget(toplevel, title, message)

class FileDialogHelper:
    @staticmethod
    def get_open_filename(parent, title="Open File", filters=None):
        dialog = Gtk.FileDialog.new()
        dialog.set_title(title)

        if filters:
            filter_store = Gio.ListStore.new(Gtk.FileFilter)
            for name, pattern in filters:
                file_filter = Gtk.FileFilter()
                file_filter.set_name(name)
                file_filter.add_pattern(pattern)
                filter_store.append(file_filter)
            dialog.set_filters(filter_store)

        selected_file = {"path": None}
        loop = GLib.MainLoop()

        def on_open_ready(dialog, result):
            try:
                f = dialog.open_finish(result)
                selected_file["path"] = f.get_path()
            except GLib.Error:
                selected_file["path"] = None
            finally:
                loop.quit()

        #dialog.open(parent, None, on_open_ready)
        dialog.open(None, None, on_open_ready)
        loop.run()

        return selected_file["path"]

class SimpleItem(GObject.Object):
    __gtype_name__ = "SimpleItem"

    def __init__(self, key, value):
        super().__init__()
        self.k = key
        self.v = value

    @GObject.Property
    def key(self):
        return self.k

    @GObject.Property
    def value(self):
        return self.v

    def getKey(self):
        return self.k

    def getValue(self):
        return self.v

class SimpleDropDown(Gtk.DropDown):
    def __init__(self):
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._on_factory_setup)
        factory.connect("bind", self._on_factory_bind)

        self.model = Gio.ListStore(item_type=SimpleItem)

        super().__init__(model=self.model, factory=factory)

    def _on_factory_setup(self, factory, list_item):
        label = Gtk.Label()
        list_item.set_child(label)

    def _on_factory_bind(self, factory, list_item):
        label = list_item.get_child()
        item = list_item.get_item()
        label.set_text(item.getValue())

    def add(self, key, value):
        self.model.append(SimpleItem(key, value))

class SimpleListView(Gtk.Box):
    __gtype_name__ = 'SimpleListView'

    def __init__(self, orientation=Gtk.Orientation.VERTICAL, **kwargs):
        super().__init__(orientation=orientation, **kwargs)

        # 1) Model: ListStore for Item objects
        self.model = Gio.ListStore.new(SimpleItem)

        # 2) Selection model
        self.selection = Gtk.SingleSelection.new(self.model)

        # 3) Factory for rendering items
        self.factory = Gtk.SignalListItemFactory.new()
        self.factory.connect("setup", self._on_setup)
        self.factory.connect("bind",  self._on_bind)

        # 4) ListView creation
        self.list_view = Gtk.ListView.new(self.selection, self.factory)

        # 5) Wrap in ScrolledWindow
        scrolled = Gtk.ScrolledWindow.new()
        scrolled.set_child(self.list_view)
        self.append(scrolled)

    def _on_setup(self, factory, list_item):
        """Create the child widget (a left-aligned label)."""
        label = Gtk.Label.new()
        label.set_xalign(0)
        list_item.set_child(label)

    def _on_bind(self, factory, list_item):
        """Bind each Item.value to the label text."""
        item = list_item.get_item()
        label = list_item.get_child()
        label.set_text(item.value)

    def add(self, key, value):
        self.model.append(SimpleItem(key, value))

    def get_selected_idx(self):
        return self.selection.get_selected()

    def get_selected_id(self):
        """Return the id of the currently selected item, or None."""
        idx = self.selection.get_selected()
        if idx >= 0:
            return self.model.get_item(idx).getKey()
        return None

    def get_selected_value(self):
        """Return the display value of the currently selected item, or None."""
        idx = self.selection.get_selected()
        if idx >= 0:
            return self.model.get_item(idx).getValue()
        return None

    def select_id(self, id_to_select):
        """Programmatically select the item matching the given id."""
        for idx in range(self.model.get_n_items()):
            if self.model.get_item(idx).getKey() == id_to_select:
                self.selection.set_selected(idx)
                return

