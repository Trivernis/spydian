#!/usr/bin/env bash
sudo apt update
sudo apt upgrade
sudo apt dist-upgrade
sudo pip3 install pygame
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
sudo pip install adafruit-pca9685
sudo apt install vsftpd
sudo apt install vlc
sudo modprobe bcm2835-v4l2
if hash pip3; then
    pip install pygame
    exit 0
fi
if hash pip;then
    pip install pygame
    exit 0
fi
exit 1