#!/bin/bash
0;276;0cset -x #echo on
pwd

sudo apt-get update
sudo apt-get -y upgrade

sudo apt install python3-pip
#pip install platform
#pip install socket
#pip install re
pip install uuid
#pip install json
pip install psutil
pip install logging
#pip install subprocess
#pip install os
pip install py-cpuinfo
pip install py-dmidecode

sudo apt  install golang-go

#wget https://golang.org/dl/go1.16.5.linux-amd64.tar.gz
#sudo tar -xvf go1.16.5.linux-amd64.tar.gz
#sudo mv go /usr/local
export GOROOT=/usr/local/go
export GOPATH=$HOME/Projects/Proj1
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
/usr/bin/go version
/usr/bin/go env 
