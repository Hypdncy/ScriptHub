#!/usr/bin/env bash

my_dir=$(pwd)
my_hostname="light"
my_python_version="3.11.2"
my_go_version="1.20.1"
my_mysql_pass="Mysql1235.."
my_mirrors_domain="mirrors.tencentyun.com"
my_mirrors_url="http://${my_mirrors_domain}"
apt-get -y install wget curl

function install_apt() {
  sed -i -E "s/(deb|security).debian.org/${my_mirrors_domain}/g" /etc/apt/sources.list
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
  sed -i 's/filetype plugin indent on/filetype plugin indent off/g' /usr/share/vim/vim82/defaults.vim

  grep "^set nocompatible" /etc/vim/vimrc || echo "\
set nocompatible
set expandtab
set number
set backspace=2
set mouse-=a
set shiftwidth=4
set tabstop=4
set softtabstop=4

set noautoindent
set nocindent
set nosmartindent
set indentexpr=
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
  cd "${my_dir}" || exit

  echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDkKrEPadsD+82e8w3Epegm51FGELj6QyvsAn6V5Dt1WWifnhN9Cnk7TyTTmfziPY/DAgiA9vkYGua+jzQl+m7N0V5oMMXxiTSjEGJeHsVa4Qi+yK99CuLYv7T5FlamXTa80BUybc7xG66si2AWrYln2PHuuZuclwzxXeUHy73oaIheYnpxqy7bFnBJR6ojLoTJImnR/2RjntLRAZoR4w9eA25maEL00KXI5cP6mVopy6WRQuqCv27UjkMId5ivIKWEochtA2NiBGji6gKV9RBDRrlZ1O6FA1Y2DOUZxwPHLa708VCBzdwJRQ4dbvthcZ4YPj8uxZXOhTFKU3vsWrcZ0M2dXnPe3ioLNUGXiPd4Nlx38cBVnuTI44KVDOVxWFD0yqzGjDgb6Bdb6/5e/v2ypIwOQGyFiU7h3hXIKyi/13lA+3LAc94oOjT1mm//SwF4D6eDWda3PUGxptHo8eyocIc5NIR2dLs6ofhzllF29aTnw81jAgmEmaVtrSW1wns= hypdncy@Hypdncy-Mac.local" >~/.ssh/authorized_keys
  grep "PasswordAuthentication no" /etc/ssh/sshd_config || (
    sed -i 's@^#*PermitRootLogin prohibit-password$@PermitRootLogin yes@g' /etc/ssh/sshd_config
    sed -i 's@^PasswordAuthentication yes$@PasswordAuthentication no@g' /etc/ssh/sshd_config
    sed -i '$a RSAAuthentication yes' /etc/ssh/sshd_config
    sed -i '$a PubkeyAuthentication yes' /etc/ssh/sshd_config
  )
}

function install_proxychains() {
  cd "${my_dir}" || exit
  # proxychains4
  apt-get -y purge proxychains*
  apt-get -y install proxychains4
  sed -i 's/^socks/# &/g' /etc/proxychains4.conf
  grep "^socks" /etc/proxychains4.conf || sed -i '$ a socks5 127.0.0.1 10808' /etc/proxychains4.conf

}

# Python

function install_python() {
  cd "${my_dir}" || exit
  apt-get -y install wget libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
  test -f ./Python-${my_python_version}.tar ||
    wget https://cdn.npmmirror.com/binaries/python/${my_python_version}/Python-${my_python_version}.tar.xz
  xz -d ./Python-${my_python_version}.tar.xz
  tar -xvf ./Python-${my_python_version}.tar
  cd Python-${my_python_version} || exit
  ./configure --prefix=/usr/local/Python-${my_python_version} --enable-optimizations
  make -j $(nproc) && make install
  /usr/local/Python-${my_python_version}/bin/pip3 config set global.index-url https://${my_mirrors_domain}/pypi/simple
  mkdir -p /opt/venv/
  /usr/local/Python-${my_python_version}/bin/python3 -m venv /opt/venv/venv

  echo -e "\nsource /opt/venv/venv/bin/activate\n" >~/.profile
}

function install_go() {
  cd "${my_dir}" || exit

  test -f ./go${my_go_version}.linux-amd64.tar.gz || wget https://dl.google.com/go/go${my_go_version}.linux-amd64.tar.gz
  rm -rf /usr/local/go && tar -C /usr/local -xzf go${my_go_version}.linux-amd64.tar.gz

  grep "/usr/local/go/bin" ~/.profile || {
    echo "export PATH=\$PATH:/usr/local/go/bin"
    echo "export GO111MODULE=on"
    echo "export GOPROXY=https://goproxy.cn"
    echo "export PATH=\$PATH:/root/go/bin"
  } >>~/.profile
  source "${HOME}/.profile"
}

function install_mysql() {
  cd "${my_dir}" || exit

  # 安装
  wget https://repo.mysql.com//mysql-apt-config_0.8.24-1_all.deb
  apt install ./mysql-apt-config_0.8.24-1_all.deb -y
  apt-get update

  apt-get install mysql-server
  systemctl restart mysql
  mysql -uroot -p --connect-expired-password -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${my_mysql_pass}';FLUSH PRIVILEGES;"
  mysql -uroot -p"${my_mysql_pass}" --connect-expired-password -e "UPDATE mysql.user SET Host = '%' WHERE User = 'root';FLUSH PRIVILEGES;"

  grep -E "^bind-address" /etc/mysql/mysql.conf.d/mysqld.cnf && sed -i 's/\(bind-address = 127.0.0.1\)/# \1/g' /etc/mysql/mysql.conf.d/mysqld.cnf

}

function install_docker() {
  cd "${my_dir}" || exit

  # step 1: 安装必要的一些系统工具
  apt-get purge -y docker docker-engine docker.io
  apt-get update
  apt-get -y install apt-transport-https ca-certificates curl software-properties-common
  # step 2: 安装GPG证书
  curl -fsSL ${my_mirrors_url}/docker-ce/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg --yes
  # Step 3: 写入软件源信息
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] ${my_mirrors_url}/docker-ce/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list >/dev/null

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
install_go
install_docker
