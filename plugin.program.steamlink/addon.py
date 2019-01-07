"""Steamlink Launcher for OSMC"""
import os
import xbmc
import xbmcgui
import xbmcaddon

__plugin__ = "steamlink"
__author__ = "toast"
__url__ = "https://github.com/swetoast/steamlink-launcher/"
__git_url__ = "https://github.com/swetoast/steamlink-launcher/"
__credits__ = "toast"
__version__ = "0.0.3"

dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon(id='plugin.program.steamlink')


def main():
    """Main operations of this plugin."""
    if os.path.isfile("/tmp/steamlink-launcher.sh"):
        output = os.popen("sh /tmp/steamlink-launcher.sh").read()
    else:
        create_files()
        output = os.popen("sh /tmp/steamlink-launcher.sh").read()
    dialog.ok("Starting Steamlink", output)


def create_files():
    """Creates bash files to be used for this plugin."""
    with open('/tmp/steamlink-launcher.sh', 'w') as outfile:
        outfile.write('''#!/bin/bash
sudo openvt -c 7 -s -f clear
sudo su osmc -c "sh /tmp/steamlink-watchdog.sh &" &
sudo chown osmc:osmc /usr/bin/steamlink
sudo su osmc -c "nohup openvt -c 7 -f -s steamlink >/dev/null 2>&1 &" &
sudo openvt -c 7 -s -f clear
sleep 0.5
sudo su -c "/home/osmc/.steamlink-start-hook &" &
sudo su -c "systemctl stop mediacenter &" &
exit''')
        outfile.close()
    with open('/tmp/steamlink-watchdog.sh', 'w') as outfile:
        outfile.write('''#!/bin/bash
sleep 8
while true; do 
    VAR1="$(pgrep steamlink)"
    if [ ! "$VAR1" ]; then
        sudo openvt -c 7 -s -f clear
        sudo su -c "/home/osmc/.steamlink-stop-hook &" &
        sudo su -c "sudo systemctl restart mediacenter &" &
        exit
    else 
        sleep 2
    fi
done
exit''')
        outfile.close()

main()
