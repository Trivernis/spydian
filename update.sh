#!/usr/bin/env bash
cd ..
if [ -d "spydian/" ];then
    sudo git clone https://bitbucket.org/trivernis/spydian.git spydian_update
    sudo rsync -a ./spydian_update/ ./spydian/
    sudo rm -r ./spydian_update/
    sudo chmod -R u+rw ./spydian/
    exit 0
else
    sudo git clone https://bitbucket.org/trivernis/spydian.git spydian
    sudo chmod -R u+rw ./spydian/
    exit 0
fi