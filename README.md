NBFC-Gtk - GUI for NBFC-Linux
=============================

**nbfc-gtk** is a simple Gtk-based graphical user interface for [nbfc-linux](https://github.com/nbfc-linux/nbfc-linux).

Installation
------------

- Arch Linux:
  - [Download Latest Version 0.2.0](https://github.com/nbfc-linux/nbfc-gtk/releases/download/0.2.0/nbfc-gtk-git-0.2.0-1-any.pkg.tar.zst)
  - Install the dependencies: `pacman -S python-gobject gtk4`
  - Install package: `pacman -U ./nbfc-gtk-git-0.2.0-1-any.pkg.tar.zst`

- Debian / Ubuntu:
  - [Download Latest Version 0.2.0](https://github.com/nbfc-linux/nbfc-gtk/releases/download/0.2.0/nbfc-gtk_0.2.0_amd64.deb)
  - Install the dependencies: `apt install python3-gi gir1.2-gtk-4.0 libgles2`
  - Install package: `dpkg -i ./nbfc-gtk_0.2.0_amd64.deb`

- Fedora:
  - [Download Latest Version 0.2.0](https://github.com/nbfc-linux/nbfc-gtk/releases/download/0.2.0/fedora-nbfc-gtk-0.2.0-1.x86_64.rpm)
  - Install the dependencies: `dnf install python3-gobject gtk4`
  - Install package: `dnf install ./fedora-nbfc-gtk-0.2.0-1.x86_64.rpm`

- OpenSuse (Tumbleweed)
  - [Download Latest Version 0.2.0](https://github.com/nbfc-linux/nbfc-gtk/releases/download/0.2.0/opensuse-nbfc-gtk-0.2.0-1.x86_64.rpm)
  - Install the dependencies: `dnf install python3-gobject gtk4 gtk4-devel`
  - Install package: `zypper install ./opensuse-nbfc-gtk-0.2.0-1.x86_64.rpm`

- In general:
  - make && sudo make install

Usage
-----

For **configuring** and **starting** the NBFC service, run `sudo nbfc-gtk`.

Screenshots
-----------

![Screenshot NBFC-Gtk Service control](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-service.png)

![Screenshot NBFC-Gtk Fan Control](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-fans.png)

![Screenshot NBFC-Gtk Basic Configuration](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-basic.png)

![Screenshot NBFC-Gtk Sensor Configuration](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-sensors.png)

![Screenshot NBFC-Gtk Update](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-update.png)

