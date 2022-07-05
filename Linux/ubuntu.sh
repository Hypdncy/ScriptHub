#!/usr/bin/bash
# File: ubuntu.sh
# Created Date: Thursday, May 21st 2020, 2:28:36 am
# Author: Hypdncy
# -----
# Last Modified: Thu May 21 2020
# Modified By: Hypdncy
# -----
# Copyright (c) 2020 Hypdncy
#
# 佛祖保佑，永无BUG
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------






function apt_install_tools(){
    apt-get purge vim*
    apt-get autoremove --purge
    apt-get install curl wget dnsutils lrzsz tree vim unzip
    
    # config vim
    echo "set nocompatible" >> /etc/vim/vimrc
    echo "set backspace=2" >> /etc/vim/vimrc
    echo "set mouse-=a" >> /etc/vim/vimrc
    echo "set number" >> /etc/vim/vimrc
    
    # config inputrc
    echo "set completion-ignore-case on" >> /etc/inputrc
    
    # config bahrc
}


function apt_install_language(){
    
    apt-get install language-pack-zh-hans language-pack-zh-hans-base manpages-zh
    timedatectl set-timezone Asia/Shanghai
    update-locale LANG=zh_CN.UTF-8
    
    # :> /etc/default/locale
    # echo "LANG=zh_CN.UTF-8" > /etc/default/locale
    
}

function apt_install_lamp(){
    apt install apache2 php mysql-server php-mysql
    echo -e "[mysqld]\nbind-address = 0.0.0.0\n\n\n\n[mysql]\nauto-rehash\n" >> /etc/mysql/my.cnf
    # php extension=mysqli
}

