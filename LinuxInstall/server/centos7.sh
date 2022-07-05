mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
curl -o /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo
sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
yum clean all
yum groupinstall -y "Development Tools"
yum install -y vim
yum install -y make cmake curl wget p7zip-full lrzsz tree bind-utils

grep "^set completion-ignore-case on" /etc/inputrc || sudo echo "set completion-ignore-case on" >>/etc/inputrc

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

sed -i 's@^#*PermitRootLogin prohibit-password$@PermitRootLogin yes@g' /etc/ssh/sshd_config


yum -y install make zlib zlib-devel gcc-c++ libtool openssl openssl-devel
curl https://repo.huaweicloud.com/nginx/nginx-1.20.1.tar.gz -O
tar -zxvf nginx-1.20.1.tar.gz
cd nginx-1.20.1
./configure --prefix=/dbapp/nginx --with-http_ssl_module

curl -O https://repo.huaweicloud.com/redis/redis-6.2.4.tar.gz
tar -zxvf redis-6.2.4.tar.gz
cp -rf redis-6.2.4 /dbapp/redis
cd /dbapp/redis/
make

yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel
curl -O https://repo.huaweicloud.com/python/3.9.6/Python-3.9.6.tgz
tar -zxvf Python-3.9.6.tgz
cd Python-3.9.6
./configure --prefix /dbapp/python3.9 --enable-optimizations
make && make install

mkdir -p ~/.pip
echo "\
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com

" > ~/.pip/pip.conf


curl - O https://repo.mysql.com//mysql80-community-release-el7-3.noarch.rpm
rpm -ivh mysql80-community-release-el7-3.noarch.rpm

yum remove mariadb-libs -y
yum clean all
yum makecache
yum install mysql-community-server -y

grep 'temporary password' /var/log/mysqld.log
mysql -u root -p

ALTER USER 'root'@'localhost' IDENTIFIED BY 'Dbapp1235..';
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Dbapp1235..';
UPDATE mysql.user SET `Host`='%' WHERE User='root';
flush privileges;

SHOW VARIABLES LIKE 'validate_password%';



set global validate_password.length=1;
set global validate_password.policy=0;

create user 'root'@'%' identified by 'root123';
ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
grant all privileges on *.* to 'root'@'%' with grant option;

1、修改密码过期
ALTER USER'root'@'localhost' IDENTIFIED BY 'root' PASSWORD EXPIRE NEVER;
2、重新修改密码
ALTER USER'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
3、刷新权限（不做可能无法生效）
FLUSH PRIVILEGES;