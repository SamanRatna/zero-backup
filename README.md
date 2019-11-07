# Setup instructions for RaspberryPi:

## A. Prepare the RPi.
    1. Setup ssh and/or serial port communications in RPi. And, make sure you can remote login into the RPi.
    2. Update and upgrade RPi.
        $ sudo apt update
        $ sudo apt upgrade

## B. Copy the program to RPi or, clone it to RPi using git, and checkout to rpi4 branch.
    $ git clone git clone git@github.com:suwalkanishka/yatri-project-zero.git
    $ git checkout rpi4

## C. Start the python backend.
    1. Install events and eel python modules
        $ sudo pip3 install events
        $ sudo pip3 install eel
    2. Copy vmgr.service unit file from service_files folder to /lib/systemd/system folder in RPi.
    3. Enable the python backend.
        $ sudo systemctl enable vmgr.service
        $ sudo systemctl start vmgr.service
    4. Check if the python backend is up and running.
        $ systemctl status vmgr.service

## D. Make changes to start chromium kiosk automatically on boot.
    1. Install matchbox-window-manager.
        $ sudo apt install matchbox-window-manager
    2. Copy mini-x-sesson file to /usr/bin folder in RPi.
    3. Make the file executable.
        $ sudo chmod a+x /usr/bin/mini-x-sesson
    4. Change the window manager from LXDE to Matchbox.
        $ sudo rm /etc/alternatives/x-session-manager
        $ sudo ln -s /usr/bin/mini-x-session /etc/alternatives/x-session-manager

## E. Remove the mouse cursor.
    1. Set the following parameter in the file /etc/lightdm/lightdm.conf
        xserver-command=X -nocursor
            under the [Seat section]

## F. Remove unneccesary programs from RPi.
   1. Remove the default LXDE window manager.
        $ sudo apt-get remove lxappearance lxde lxde-* lxinput lxmenu-data lxpanel lxpolkit lxrandr lxsession* lxsession lxshortcut    lxtask lxterminal

    2. Remove preinstalled softwares.
        $ sudo apt remove qpdfview* vlc* alsa* galculator thonny geany gpicview* xarchiver
        $ sudo apt autoremove
        $ sudo apt purge

## G. Taking care of Splash Screen and boot logs.
    1. Add the following line at the end of the line in /boot/config.txt file.
        disable_splash=1
    2. Add the following line at the end of the line in /boot/cmdline.txt.
        splash quiet plymouth.ignore-serial-consoles logo.nologo vt.global_cursor_default=0

# References:
Splash Screen and Boot Logs
    https://yingtongli.me/blog/2016/12/21/splash.html
    https://scribles.net/customizing-boot-up-screen-on-raspberry-pi/
Mouse cursor
    https://raspberrypi.stackexchange.com/questions/53127/how-to-permanently-hide-mouse-pointer-or-cursor-on-raspberry-pi
Chromium Kiosk
    https://pimylifeup.com/raspberry-pi-kiosk/
    https://www.sylvaindurand.org/launch-chromium-in-kiosk-mode/
    https://github.com/lukaskubis/raspbian-jesse-kiosk
Window Manager
    https://wiki.embeddedarm.com/wiki/TS-7970#Debian_Starting_Automatically

