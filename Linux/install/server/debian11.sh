#!/usr/bin/env bash

my_hostname="light"
my_version_python="3.11.2"
my_version_go="1.18.3"
my_mysql_pass="Mysql1235.."

apt-get -y install wget curl

function install_apt() {
  sed -i -E 's/(deb|security).debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list
}

function install_locale() {
  timedatectl set-timezone Asia/Shanghai
  localectl set-locale LANG=zh_CN.UTF-8
  hostnamectl set-hostname ${my_hostname}
}

# vim
function install_vim() {
  apt-get -y purge vim*
  apt-get -y install vim

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
" >>/etc/vim/vimrc
  # 大小写控制
  grep "^set completion-ignore-case on" /etc/inputrc || echo "set completion-ignore-case on" >>/etc/inputrc

}

function install_dev() {
  # 开发软件包
  apt-get -y install build-essential

  # 通用安装
  apt-get -y install p7zip-full lrzsz tree curl wget

  # 汉化
  apt-get -y install -y manpages-zh
}

function install_ssh() {
  echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDkKrEPadsD+82e8w3Epegm51FGELj6QyvsAn6V5Dt1WWifnhN9Cnk7TyTTmfziPY/DAgiA9vkYGua+jzQl+m7N0V5oMMXxiTSjEGJeHsVa4Qi+yK99CuLYv7T5FlamXTa80BUybc7xG66si2AWrYln2PHuuZuclwzxXeUHy73oaIheYnpxqy7bFnBJR6ojLoTJImnR/2RjntLRAZoR4w9eA25maEL00KXI5cP6mVopy6WRQuqCv27UjkMId5ivIKWEochtA2NiBGji6gKV9RBDRrlZ1O6FA1Y2DOUZxwPHLa708VCBzdwJRQ4dbvthcZ4YPj8uxZXOhTFKU3vsWrcZ0M2dXnPe3ioLNUGXiPd4Nlx38cBVnuTI44KVDOVxWFD0yqzGjDgb6Bdb6/5e/v2ypIwOQGyFiU7h3hXIKyi/13lA+3LAc94oOjT1mm//SwF4D6eDWda3PUGxptHo8eyocIc5NIR2dLs6ofhzllF29aTnw81jAgmEmaVtrSW1wns= hypdncy@Hypdncy-Mac.local" >~/.ssh/authorized_keys
  grep "PasswordAuthentication no" /etc/ssh/sshd_config || (
    sed -i 's@^#*PermitRootLogin prohibit-password$@PermitRootLogin yes@g' /etc/ssh/sshd_config
    sed -i 's@^PasswordAuthentication yes$@PasswordAuthentication no@g' /etc/ssh/sshd_config
    sed -i '$a RSAAuthentication yes' /etc/ssh/sshd_config
    sed -i '$a PubkeyAuthentication yes' /etc/ssh/sshd_config
  )
}

function install_bashrc() {
  grep "^alias ls" ~/.bashrc || echo "\
# PS1='\${debian_chroot:+(\$debian_chroot)}\\h:\\w\\\$ '
PS1='\${debian_chroot:+(\$debian_chroot)}\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\\$ '
umask 022
export LS_OPTIONS='--color=auto'
eval \"\$(dircolors)\"
alias ls='ls \$LS_OPTIONS'
alias ll='ls \$LS_OPTIONS -l'
alias l='ls \$LS_OPTIONS -lA'
" >>~/.bashrc

}

function install_proxychains() {
  # proxychains4
  apt-get -y purge proxychains*
  apt-get -y install proxychains4
  sed -i 's/^socks/# &/g' /etc/proxychains4.conf
  grep "^socks" /etc/proxychains4.conf || sed -i '$ a socks5 127.0.0.1 10808' /etc/proxychains4.conf

}

# Python

function install_python() {
  apt-get -y install wget libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
  test -f ./Python-${my_version_python}.tar || wget https://repo.huaweicloud.com/python/${my_version_python}/Python-${my_version_python}.tar.xz
  xz -d ./Python-${my_version_python}.tar.xz
  tar -xvf ./Python-${my_version_python}.tar
  cd Python-${my_version_python} || exit
  ./configure --prefix=/usr/local/Python-${my_version_python} --enable-optimizations
  make -j $(nproc) && make install
  cd /opt || exit
  /usr/local/Python-${my_version_python}/bin/python3 -m venv venv
}

function install_pip() {
  # pip 镜像源
  test -f ~/.config/pip/pip.conf || (mkdir -p ~/.config/pip/ && echo "\
[global]
index-url = https://repo.huaweicloud.com/repository/pypi/simple
trusted-host = repo.huaweicloud.com
timeout = 120
" >~/.config/pip/pip.conf)
}

function install_go() {
  test -f go${my_version_go}.linux-amd64.tar.gz || wget https://mirrors.aliyun.com/golang/go${my_version_go}.linux-amd64.tar.gz
  rm -rf /usr/local/go && tar -C /usr/local -xzf go${my_version_go}.linux-amd64.tar.gz

  grep "/usr/local/go/bin" ~/.profile || {
    echo "export PATH=\$PATH:/usr/local/go/bin"
    echo "export GO111MODULE=on"
    echo "export GOPROXY=https://goproxy.cn"
    echo "export PATH=\$PATH:/root/go/bin"
  } >>~/.profile
  source "${HOME}/.profile"
}

function install_mysql() {
  # 安装
  apt-get update
  apt-get install mysql-server
  apt-get install mysql-client
  systemctl restart mysqld
  mysql -uroot -p --connect-expired-password -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${my_mysql_pass}';FLUSH PRIVILEGES;"
  mysql -uroot -p"${my_mysql_pass}" --connect-expired-password -e "UPDATE mysql.user SET Host = '%' WHERE User = 'root';FLUSH PRIVILEGES;"

  grep -E "^bind-address" /etc/mysql/mysql.conf.d/mysqld.cnf && sed -i 's/\(bind-address = 127.0.0.1\)/# \1/g' /etc/mysql/mysql.conf.d/mysqld.cnf

}

function install_docker() {
  # step 1: 安装必要的一些系统工具
  apt-get purge -y docker docker-engine docker.io
  apt-get update
  apt-get -y install apt-transport-https ca-certificates curl software-properties-common
  # step 2: 安装GPG证书
  curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/debian/gpg | apt-key add -
  # Step 3: 写入软件源信息
  add-apt-repository "deb [arch=amd64] https://mirrors.aliyun.com/docker-ce/linux/debian $(lsb_release -cs) stable"
  # Step 4: 更新并安装Docker-CE
  apt-get -y update
  apt-get -y install docker-ce

}

#install_apt
install_locale
install_vim
install_dev
install_ssh
install_bashrc
install_proxychains
install_python
install_pip
install_go
install_docker
install_mysql