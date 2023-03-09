#!/usr/bin/env bash

# centos7由于gcc和openssl原因只能使用python3.9
my_python_version="3.9.16"
my_go_version="1.20.1"
my_mysql_pass="Mysql1235.."
my_redis_pass="Redis1235.."

yum -y install wget curl

function install_yum() {
  mv -f /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak
  wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.cloud.tencent.com/repo/centos7_base.repo
  #  wget -O /etc/yum.repos.d/epel.repo http://mirrors.cloud.tencent.com/repo/epel-7.repo
  yum clean all
  yum makecache
}

function install_locale() {
  timedatectl set-timezone Asia/Shanghai
  localectl set-locale LANG=zh_CN.UTF-8
  #  hostnamectl set-hostname ${my_hostname}
}

function install_dev() {
  yum groupinstall -y "Development Tools"
  yum install -y vim
  yum install -y make cmake curl wget p7zip lrzsz tree bind-utils
}

function install_vim() {

  grep "^set nocompatible" /etc/vimrc || echo "\
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
" >>/etc/vimrc
  # 大小写控制
  grep "^set completion-ignore-case on" /etc/inputrc || echo "set completion-ignore-case on" >>/etc/inputrc

}

function bashrc() {
  grep -E "^PS1" ~/.bashrc || print "PS1='\\[\\033[01;32m\\]\\u@\\h\\[\\033[00m\\]:\\[\\033[01;34m\\]\\w\\[\\033[00m\\]\\$ '" >>~/.bashrc
}

function install_mysql() {
  yum remove mariadb* -y
  curl -O 'https://repo.mysql.com/mysql80-community-release-el7-7.noarch.rpm'
  rpm -ivh ./mysql80-community-release-el7-7.noarch.rpm
  yum makecache fast
  yum install mysql-community-server -y
  systemctl restart mysqld
  tmp_mysql_pass=$(grep 'temporary password' /var/log/mysqld.log | awk '{print $NF}')
  mysql -uroot -p"${tmp_mysql_pass}" --connect-expired-password -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${my_mysql_pass}';FLUSH PRIVILEGES;"
  mysql -uroot -p"${my_mysql_pass}" --connect-expired-password -e "UPDATE mysql.user SET Host = '%' WHERE User = 'root';FLUSH PRIVILEGES;"
  systemctl restart mysqld
}

function install_python() {
  yum install gcc openssl-devel bzip2-devel libffi-devel -y
  test -f ./Python-${my_python_version}.tar || (curl -O https://repo.huaweicloud.com/python/${my_python_version}/Python-${my_python_version}.tar.xz && xz -d ./Python-${my_python_version}.tar.xz)
  tar -xvf ./Python-${my_python_version}.tar
  cd Python-${my_python_version} || exit
  # --enable-optimizations 安装会报错，
  ./configure --prefix=/usr/local/Python-${my_python_version}
  make && make install
  /usr/local/Python-${my_python_version}/bin/python3 -m venv /opt/venv
  source /opt/venv/bin/activate
  grep "source /opt/venv/bin/activate" ~/.profile || echo "source /opt/venv/bin/activate" >>~/.profile

  # pip 镜像源
  test -f ~/.config/pip/pip.conf || (mkdir -p ~/.config/pip/ && echo "\
[global]
index-url = https://mirrors.cloud.tencent.com/pypi/simple
timeout = 120
" >~/.config/pip/pip.conf)

}

function install_go() {
  test -f ./go${my_go_version}.linux-amd64.tar.gz || wget https://dl.google.com/go/go${my_go_version}.linux-amd64.tar.gz
  rm -rf /usr/local/go && tar -C /usr/local -xzf go${my_go_version}.linux-amd64.tar.gz

  grep "/usr/local/go/bin" ~/.profile || {
    echo "export PATH=\$PATH:/usr/local/go/bin"
    echo "export GO111MODULE=on"
    echo "export GOPROXY=https://goproxy.cn"
    echo "export PATH=\$PATH:/root/go/bin"
  } >>~/.profile
  source ~/.profile
}

function install_redis() {
  yum install -y redis
  sed -i '/^requirepass/d' /etc/redis.conf
  echo -e -n "\n" >>/etc/redis.conf
  echo "requirepass ${my_redis_pass}" >>/etc/redis.conf
  systemctl restart redis
}

function install_docker() {

  yum remove -y docker*
  yum install -y yum-utils device-mapper-persistent-data lvm2
  wget -O /etc/yum.repos.d/docker-ce.repo https://download.docker.com/linux/centos/docker-ce.repo
  sudo sed -i 's+download.docker.com+mirrors.cloud.tencent.com/docker-ce+' /etc/yum.repos.d/docker-ce.repo
  yum makecache fast
  yum -y install docker-ce
  # Step 4: 开启Docker服务
  systemctl restart docker
}


function install_jdk8(){


  wget https://package-1259804243.cos.ap-nanjing.myqcloud.com/jdk/jdk-8u181-linux-x64.tar.gz
  tar -zxvf jdk-8u181-linux-x64.tar.gz -C /usr/local/
  echo > /usr;
  export JAVA_HOME=/usr/local/java/jdk1.8.0_241

export PATH=$PATH:$JAVA_HOME/bin

export CLASSPATH=.:$JAVA_HIOME/jre/lib/rt.jar:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
————————————————
版权声明：本文为CSDN博主「老三笔记」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/debug1001/article/details/124791375
}

install_locale
install_dev
install_vim
install_go
install_mysql
install_python
install_redis
install_docker
