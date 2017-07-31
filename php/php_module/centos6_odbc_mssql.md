# Centos6 安装odbc 连接sqlserver

## 安装
使用微软提供的连接驱动，以下是安装包的repo

RedHat Enterprise Server 6

```
Copy
sudo su
curl https://packages.microsoft.com/config/rhel/6/prod.repo > /etc/yum.repos.d/mssql-release.repo
exit
sudo yum remove unixODBC-utf16 unixODBC-utf16-devel #to avoid conflicts
sudo ACCEPT_EULA=Y yum install msodbcsql
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y yum install mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo yum install unixODBC-devel
```

RedHat Enterprise Server 7

```
Copy
sudo su
curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo
exit
sudo yum remove unixODBC-utf16 unixODBC-utf16-devel #to avoid conflicts
sudo ACCEPT_EULA=Y yum install msodbcsql
# optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y yum install mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
# optional: for unixODBC development headers
sudo yum install unixODBC-devel
```


## 编译pdo-odbc

**重点是php的源码包里有一个ext文件夹，好多扩展其实已经放到里边了**

解压php-5.6.17.tar.gz源码。

```
tar zxf php-5.6.17.tar.gz
cd php-5.6.17
cd ext
cd pdo-odbc
#使用你现在所用的phpize
/usr/local/bin/phpize
./configure --with-pdo-odbc=unixODBC,/usr/ --with-php-config=/usr/local/bin/php-config
make
sudo make install
```

## 配置
在安装了某个数据库的连接驱动后，应该会在odbcinst.ini中增加这个驱动。例如，我们安装了
sql-server的连接驱动，可以在odbcinst.ini中看到它的相关配置。

查看/etc/odbcinst.ini中，应该有了sql server的连接驱动

```
[PostgreSQL]
Description=ODBC for PostgreSQL
Driver=/usr/lib/psqlodbcw.so
Setup=/usr/lib/libodbcpsqlS.so
Driver64=/usr/lib64/psqlodbcw.so
Setup64=/usr/lib64/libodbcpsqlS.so
FileUsage=1

[MySQL]
Description=ODBC for MySQL
Driver=/usr/lib/libmyodbc5.so
Setup=/usr/lib/libodbcmyS.so
Driver64=/usr/lib64/libmyodbc5.so
Setup64=/usr/lib64/libodbcmyS.so
FileUsage=1

[ODBC Driver 13 for SQL Server]
Description=Microsoft ODBC Driver 13 for SQL Server
Driver=/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.1.so.9.0
UsageCount=1
```
**注意这个配置文件中，方括号里边的就是驱动名称，用来在odbc.ini中选择驱动用的。**


有了驱动后，需要配置连接文件，也就是数据库的连接参数。这个一般都放置在/etc/odbc.ini中。
也可以自己定义位置，需要的时候指定好文件即可。


odbc.ini例子

```
[MyDSN]
Driver=ODBC Driver 13 for SQL Server
Description=My Test ODBC Database Connection
Trace=Yes
Server=192.168.0.122
Port=1433
Database=mytest

```

## 连接测试

```
isql MyDSN _username_ _passwod_

#以下是连接成功的输出信息
+---------------------------------------+
| Connected!                            |
|                                       |
| sql-statement                         |
| help [tablename]                      |
| quit                                  |
|                                       |
+---------------------------------------+
SQL> quit

```


使用php代码连接测试。

```
<?php

 putenv('ODBCSYSINI=/etc/');
 putenv('ODBCINI=/etc/odbc.ini');

    $username = "xxxx";
    $password = "xxxxxx";
    try {
      $dbh = new PDO("odbc:MyDSN",
                    "$username",
                    "$password"
                   );
    } catch (PDOException $exception) {
      echo $exception->getMessage();
      exit;
    }
    echo var_dump($dbh);
    unset($dbh);
?>

/usr/local/bin/php test.php 

object(PDO)#1 (0) {
}


```


