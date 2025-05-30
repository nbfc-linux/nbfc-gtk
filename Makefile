bindir = /usr/bin

all: nbfc-gtk.py

nbfc-gtk.py: \
	src/main.py \
	src/errors.py \
	src/nbfc_client.py \
	src/subprocess_worker.py \
	src/gtk_common.py \
	src/common.py \
	src/version.py \
	src/widgets/apply_buttons_widget.py \
	src/widgets/about_widget.py \
	src/widgets/service_control_widget.py \
	src/widgets/basic_config_widget.py \
	src/widgets/fan_widget.py \
	src/widgets/fan_control_widget.py \
	src/widgets/sensor_widget.py \
	src/widgets/sensors_widget.py \
	src/widgets/update_widget.py \
	src/widgets/early_error_window.py \
	src/widgets/main_window.py
	(cd ./src; python3 ./include_files.py main.py > ../nbfc-gtk.py)
	chmod +x nbfc-gtk.py

README.md: .force
	./tools/update_readme.py README.md.in > README.md

pkgbuilds/nbfc-gtk/PKGBUILD: .force
	./tools/update_pkgbuild.py pkgbuilds/nbfc-gtk/PKGBUILD.in > pkgbuilds/nbfc-gtk/PKGBUILD

install:
	install -Dm 755 nbfc-gtk.py $(DESTDIR)$(bindir)/nbfc-gtk

uninstall:
	rm -f $(DESTDIR)$(bindir)/nbfc-gtk
	
clean:
	rm -rf __pycache__
	rm -f  nbfc-gtk.py
	rm -f  src/ico.py

.force:
	@true
