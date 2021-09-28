@ECHO OFF
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm "lunabotics" --type headless
ssh -p 2222 lunabotics@127.0.0.1
PAUSE