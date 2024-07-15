#!/bin/bash
systemctl disable --now powersync
mkdir -p /etc/powersync/log

cp service.py /etc/powersync/
cp powersync.service /etc/systemd/system/

systemctl daemon-reload

systemctl enable --now powersync

echo 'install sucess'
