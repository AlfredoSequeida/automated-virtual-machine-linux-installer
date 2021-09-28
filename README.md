# Automated Virtual Machine Linux Installer for Long Beach Lunabotics (AVMLILBL)

![demo](https://i.imgur.com/ih0ze0n.png)

The purpose of this program is to facilitate the installation process for those that want to use a Linux virtual machine on their Microsoft Windows systems compared to dual-booting or single booting Linux.

To use, Grab the latest release [here](https://github.com/AlfredoSequeida/automated-virtual-machine-linux-installer/releases/latest/download/installer.exe).

![installericon](https://i.imgur.com/7XcxGID.png)

Just run the installer.exe file by double-clicking on it.

![protected](https://i.imgur.com/MZ0RsbZ.png)
![protectedmoreinfo](https://i.imgur.com/geSEyd8.png)

If you get a "Windows protected your PC" message, click on "more info" and then select "Run anyway".

![admin](https://i.imgur.com/H2vrg8l.png)

Since we need admin permission to install software, select "Yes" when prompted for "Do you want to allow this app from an unknown publisher to make changes to your device".

This is a CLI program, which means that you cannot use your mouse to navigate it. Instead, you need to use your keyboard. Options are selected by typing the number or letter associated with that option/instruction and pressing the ENTER key on your keyboard.

![lunaboticsicon](https://i.imgur.com/tFRSpD7.png)

After selecting option 1, and letting the program finish, you will see a file on your desktop called "lunabotics.bat". This file is used to launch the virtual machine process and initiate an ssh session.

![sshfingerprint](https://i.imgur.com/PPg2p2k.png)
When launching the virtual machine for the first time, you will be asked if you want to continue connecting. Type "yes" without quotes and press the ENTER key.

![sshpassword](https://i.imgur.com/tQE4r4P.png)
Then you will be asked for a password. Type `lunabotics` and hit the ENTER key. Note that you will not see the password as you type it. But as long as you are focused on the window, the window is listening to your keypresses.

![poweroff](https://i.imgur.com/fiTIL1P.png)
If you ever want to power off the virtual machine, type `sudo poweroff` followed by the `ENTER` key, then type in the password `lunabotics`. Note that you will not see the password as you type it.

If you want to build your own executable, you can do so using [pyinstaller](https://www.pyinstaller.org/)


First, install pyinstaller using pip

```
py -m pip install pyinstaller
```

Then run the following command to build the executable:

```
pyinstaller installer.py --add-data "lunabotics.bat;." --uac-admin --onefile
```
