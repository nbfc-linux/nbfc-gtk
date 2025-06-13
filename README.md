NBFC-Gtk - GUI for NBFC-Linux
=============================

**nbfc-gtk** is a simple Gtk-based graphical user interface for [nbfc-linux](https://github.com/nbfc-linux/nbfc-linux).

Installation
------------

- Arch Linux:
  - Packages is available via the Arch User Repository:
    - `yay -S nbfc-gtk`
  - Or manually:
    - [Download Latest Version 0.2.1](https://github.com/nbfc-linux/nbfc-gtk/releases/download/0.2.1/nbfc-gtk-git-0.2.1-1-any.pkg.tar.zst)
    - Install package: `pacman -U ./nbfc-gtk-git-0.2.1-1-any.pkg.tar.zst`

- Debian / Ubuntu:
  - [Download Latest Version 0.2.1](https://github.com/nbfc-linux/nbfc-gtk/releases/download/0.2.1/nbfc-gtk_0.2.1_amd64.deb)
  - Install package: `apt install ./nbfc-gtk_0.2.1_amd64.deb`

- Fedora:
  - [Download Latest Version 0.2.1](https://github.com/nbfc-linux/nbfc-gtk/releases/download/0.2.1/fedora-nbfc-gtk-0.2.1-1.x86_64.rpm)
  - Install package: `dnf install ./fedora-nbfc-gtk-0.2.1-1.x86_64.rpm`

- OpenSuse (Tumbleweed)
  - [Download Latest Version 0.2.1](https://github.com/nbfc-linux/nbfc-gtk/releases/download/0.2.1/opensuse-nbfc-gtk-0.2.1-1.x86_64.rpm)
  - Install package: `zypper install ./opensuse-nbfc-gtk-0.2.1-1.x86_64.rpm`

- In general:
  - make && sudo make install

Usage
-----

For **configuring** and **starting** the NBFC service, run `sudo nbfc-gtk`.

For **controlling** the fans, no root privileges are needed.

Screenshots
-----------

![Screenshot NBFC-Gtk Service control](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-service.png)

![Screenshot NBFC-Gtk Fan Control](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-fans.png)

![Screenshot NBFC-Gtk Basic Configuration](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-basic.png)

![Screenshot NBFC-Gtk Sensor Configuration](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-sensors.png)

![Screenshot NBFC-Gtk Update](http://nbfc-linux.github.io/img/nbfc-gtk/nbfc-gtk-update.png)

