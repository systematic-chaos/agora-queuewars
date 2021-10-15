#!/bin/bash
set -eou pipefail
export DEBIAN_FRONTEND=noninteractive

echo deb http://ftp.debian.org/debian stretch-backports main contrib > /etc/apt/sources.list.d/stretch-backports.list
apt-get update
apt-get upgrade -y
apt-get install -y build-essential virtualbox-guest-dkms virtualbox-guest-x11 linux-headers-$(uname -r) tmux curl wget git vim python3-software-properties python3-pip python3-venv unzip htop strace sysstat linux-perf redis-server redis-tools

curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt-get install -y nodejs gcc g++ make
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
apt-get update
apt-get install -y yarn

wget https://github.com/nats-io/gnatsd/releases/download/v1.1.0/gnatsd-v1.1.0-linux-amd64.zip
unzip gnatsd-v1.1.0-linux-amd64.zip
mv gnatsd-v1.1.0-linux-amd64 /opt/gnatsd

pip3 install -r requirements.txt

echo -e "\nalias la='ls -lah'" >> .bashrc
