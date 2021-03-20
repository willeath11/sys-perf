pwd
# Install FIO
sudo apt-get -y update
sudo apt-get install -y fio

# What are tweaks of file system ?

## Below is from google benchmarking

# install dependencies
sudo apt-get -y update
sudo apt-get install -y build-essential git libtool gettext autoconf libgconf2-dev libncurses5-dev python-dev autopoint

# blkdiscard
git clone git://git.kernel.org/pub/scm/utils/util-linux/util-linux.git
cd util-linux/
./autogen.sh
./configure --disable-libblkid
make
sudo mv blkdiscard /usr/bin/
# UPDATE
sudo blkdiscard /dev/disk/by-id/UPDATE-ME



