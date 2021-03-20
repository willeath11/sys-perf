#!/bin/bash
set -x #echo on
pwd

# Assumes that /mnt/sda1, and each already exisit
sudo parted /dev/sda --script -- mklabel msdos
sudo parted /dev/sda --script -- mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F32 /dev/sda1
sudo mount -t vfat /dev/sda1 /mnt/sda1 -o uid=1000

sudo parted /dev/sdb --script -- mklabel msdos
sudo parted /dev/sdb --script -- mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F32 /dev/sdb1
sudo mount -t vfat /dev/sdb1 /mnt/sdb1 -o uid=1000

sudo parted /dev/sdc --script -- mklabel msdos
sudo parted /dev/sdc --script -- mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F32 /dev/sdc1
sudo mount -t vfat /dev/sdc1 /mnt/sdc1 -o uid=1000

sudo parted /dev/sdd --script -- mklabel msdos
sudo parted /dev/sdd --script -- mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F32 /dev/sdd1
sudo mount -t vfat /dev/sdd1 /mnt/sdd1 -o uid=1000

sudo parted /dev/sde --script -- mklabel msdos
sudo parted /dev/sde --script -- mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F32 /dev/sde1
sudo mount -t vfat /dev/sde1 /mnt/sde1 -o uid=1000

sudo parted /dev/sdf --script -- mklabel msdos
sudo parted /dev/sdf --script -- mkpart primary fat32 1MiB 100%
sudo mkfs.vfat -F32 /dev/sdf1
sudo mount -t vfat /dev/sdf1 /mnt/sdf1 -o uid=1000

lsblk



