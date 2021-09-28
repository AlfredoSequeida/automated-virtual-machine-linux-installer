# Automated Virtual Machine Linux Installer for Long Beach Lunabotics (AVMLILBL)

![demo](https://i.imgur.com/ih0ze0n.png)

The purpose of this program is to facilitate the installation process for those that want to use a Linux virtual machine on their Microsoft Windows systems compared to dual-booting or single booting Linux.

To use, Grab the latest release [here](https://github.com/AlfredoSequeida/automated-virtual-machine-linux-installer/releases/latest/download/installer.exe) and just run the installer.exe file by double-clicking on it. This is a CLI program, which means that you cannot use your mouse to navigate it. Instead, you need to use your keyboard. Options are selected by typing the number or letter associated with that option/instruction and pressing the ENTER key on your keyboard.

If you want to build your own executable, you can do so using [pyinstaller](https://www.pyinstaller.org/)


First, install pyinstaller using pip

```
py -m pip install pyinstaller
```

Then run the following command to build the executable:

```
pyinstaller installer.py --add-data "lunabotics.bat;." --uac-admin --onefile
```
