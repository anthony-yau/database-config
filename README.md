## 说明
本仓库存放的是一些服务参考配置, 互联网常用存储服务如: MySQL、Redis;

大数据常用服务如: HDFS、Yarn、Kafka、Zookeeper

---
## 使用帮助
### 1、mysql.spec，用于构建mysql rpm包的spec描述文件

用法：
```
yum -y install rpm-build redhat-rpm-config gcc gcc-c++ cmake make zlib-devel openssl-devel

# 创建rpmbuild构建目录：

mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

cp percona-server-5.6.19-67.0.tar.gz ~/rpmbuild/SOURCES/

cp my.cnf ~/rpmbuild/SOURCES/

rpmbuild -bb mysql.spec
```
