
```bash

#!/bin/bash

# 确保脚本以 root 身份运行
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# 检查操作系统类型和版本
if [[ -e /etc/redhat-release ]]; then
    OS_VERSION=$(cat /etc/redhat-release)
    if [[ $OS_VERSION == *"release 7."* ]]; then
        echo "System is Red Hat or CentOS 7"
        # 停止并禁用 firewalld
        systemctl stop firewalld
        systemctl disable firewalld
        echo "firewalld has been stopped and disabled"
    else
        echo "System is Red Hat or CentOS, but not version 7"
    fi
else
    echo "System is not Red Hat or CentOS"
fi

iptables -F
cd /usr/local/
yum install -y wget
wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.44-linux-glibc2.12-x86_64.tar

rpm -e --nodeps $(rpm -qa | grep mariadb)


# 此处需要一段时间
tar xf mysql-5.7.44-linux-glibc2.12-x86_64.tar         \
  && tar xf mysql-5.7.44-linux-glibc2.12-x86_64.tar.gz \
  && rm -f mysql-5.7.44-linux-glibc2.12-x86_64.tar     \
  mysql-test-5.7.44-linux-glibc2.12-x86_64.tar.gz

# 目录重命名(规范)  
mv mysql-5.7.44-linux-glibc2.12-x86_64 mysql  
  
# 创建一个 mysql 组和用户  
groupadd mysql  
useradd -r -g mysql mysql    
cd /usr/local/  
chown -R mysql:mysql mysql  
chmod -R 775 mysql  
  
# mysql/bin 目录下的全部命令创建“快捷方式”  
echo "export PATH=$PATH:/usr/local/mysql/bin" >> /etc/profile  
source /etc/profile  
# 生成mysql临时密码
cd /usr/local/mysql/  
yum install -y libaio*  
PASSWD=$(mysqld --user=mysql --initialize --datadir=/usr/local/mysql/data 2>&1 \
  | grep root                                                                  \
  | awk '{print $NF}')

# 复制启动文件到/etc/init.d/目录  
cp -ar /usr/local/mysql/support-files/mysql.server /etc/init.d/mysqld  
# 创建mysql的配置文件my.cnf，并授予执行权限
touch /etc/my.cnf 
chmod -R 775 /etc/my.cnf  

#启动mysql服务 
/etc/init.d/mysqld start  
# 添加服务为开机自启
chkconfig --add mysqld  
chkconfig –list

# 此处直接回车即可
mysql -uroot -p"$(echo $PASSWD)"

# 进入数据库后，执行如下语句，修改数据库root密码，并授权10网段主机远程登录权限
SET PASSWORD FOR root@localhost = PASSWORD('spzc1234');
GRANT ALL PRIVILEGES ON *.* TO 'root'@'10.%.%.%' IDENTIFIED BY 'spzc1234' WITH GRANT OPTION;
EXIT

```