#!/usr/bin/env bash

# 镜像
grep "ustc.edu.cn" /etc/apt/sources.list || echo "\
# deb http://security.debian.org/debian-security bullseye-security main contrib
# deb-src http://security.debian.org/debian-security bullseye-security main contrib

deb http://mirrors.ustc.edu.cn/debian/ bullseye main contrib non-free
deb-src http://mirrors.ustc.edu.cn/debian/ bullseye main contrib non-free

deb http://mirrors.ustc.edu.cn/debian/ bullseye-updates main contrib non-free
deb-src http://mirrors.ustc.edu.cn/debian/ bullseye-updates main contrib non-free

deb http://mirrors.ustc.edu.cn/debian/ bullseye-backports main contrib non-free
deb-src http://mirrors.ustc.edu.cn/debian/ bullseye-backports main contrib non-free

deb http://mirrors.ustc.edu.cn/debian-security/ bullseye-security main contrib non-free
deb-src http://mirrors.ustc.edu.cn/debian-security/ bullseye-security main contrib non-free
" > /etc/apt/sources.list

timedatectl set-timezone Asia/Shanghai
localectl set-locale LANG=zh_CN.UTF-8

apt clean all
apt update

# vim
apt -y purge vim*
apt -y install vim

grep "^set nocompatible" /etc/vim/vimrc || echo "\
set nocompatible
set nosmartindent
set noautoindent
set expandtab
set number
set backspace=2
set mouse-=a
set shiftwidth=4
set tabstop=4
set softtabstop=4
syntax on
" >> /etc/vim/vimrc

# 大小写控制
grep "^set completion-ignore-case on" /etc/inputrc || echo "set completion-ignore-case on" >>/etc/inputrc

# pip 镜像源
test -f ~/.config/pip/pip.conf || (mkdir -p ~/.config/pip/ && echo "\
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
" > ~/.config/pip/pip.conf)

# 自动清理
apt -y autopurge

# 配置ssh
sed -i 's@^#*PermitRootLogin prohibit-password$@PermitRootLogin yes@g' /etc/ssh/sshd_config

# 配置bashrc
# grep "^alias ls" ~/.bashrc || echo "\
# # PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
# umask 022
# export LS_OPTIONS='--color=auto'
# eval "$(dircolors)"
# alias ls='ls $LS_OPTIONS'
# alias ll='ls $LS_OPTIONS -l'
# alias l='ls $LS_OPTIONS -lA'
# " >> ~/.bashrc


# proxychains4
apt -y purge proxychains*
apt -y install proxychains4
sed -i 's/^socks/# &/g' /etc/proxychains4.conf
grep "^socks" /etc/proxychains4.conf || sed -i '$ a socks5 127.0.0.1 10808' /etc/proxychains4.conf

# 开发软件包
apt -y install build-essential

# 通用安装
apt -y install p7zip-full lrzsz tree

# 汉化
# apt -y install -y manpages-zh

# Python
apt -y install wget libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
wget https://repo.huaweicloud.com/python/3.10.5/Python-3.10.5.tar.xz
xz -d ./Python-3.10.5.tar.xz
tar -xvf ./Python-3.10.5.tar
cd Python-3.10.5
./configure --prefix=/usr/local/Python-3.10.5 --enable-optimizations
make -j `nproc`
make install
cd /opt
/usr/local/Python-3.10.5/bin/python3 -m venv venv