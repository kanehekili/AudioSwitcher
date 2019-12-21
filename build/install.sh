#!/bin/bash
#check if sudo
if [ "$EUID" -ne 0 ] ; then
  echo "Sorry, but you are not root. Use sudo to run"
  exit 1
fi
#copy desktop to /usr/share applications
sudo cp AudioSwitcher.desktop /usr/share/applications;
sudo mkdir -p /usr/local/bin/AudioSwitcher;
sudo cp * /usr/local/bin/AudioSwitcher/;

echo "####################################################"
echo "#                                                  #"
echo "#                App installed                     #"                     
echo "#       Find the app in Video/Audio                #"
echo "#                                                  #"
echo "####################################################"

