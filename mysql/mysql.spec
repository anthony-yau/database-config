Name: percona-server
Version:5.6.19
Release: 67.0
License: GPL

Group: applications/database
URL: http://www.percona.com/redir/downloads/Percona-Server-5.6/LATEST/source/tarball/percona-server-5.6.19-67.0.tar.gz 
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root 
BuildRequires: cmake
Requires: coreutils,shadow-utils
Packager: q_yxian@163.com
Autoreq: no
Source: percona-server-5.6.19-67.0.tar.gz
prefix: /usr/local/%{name}-%{version}-%{release}
Summary: percona server 5.6.19-67.0

%description 
Percona Server is an enhanced, drop-in MySQL® replacement which has been downloaded more than 1,000,000 times.
A free open source solution, Percona Server is a MySQL alternative which offers breakthrough performance, scalability, features, and instrumentation. Self-tuning algorithms and support for extremely high-performance hardware make it the clear choice for organizations that demand excellent performance and reliability from their MySQL database server.

%define MYSQL_USER mysql
%define MYSQL_GROUP mysql
%define __os_install_post %{nil}

%prep
%setup -n %{name}-%{version}-%{release}

%build
CFLAGS="-O3 -g -fno-exceptions -static-libgcc -fno-omit-frame-pointer -fno-strict-aliasing"
CXX=g++
CXXFLAGS="-O3 -g -fno-exceptions -fno-rtti -static-libgcc -fno-omit-frame-pointer -fno-strict-aliasing"
export CFLAGS CXX CXXFLAGS

cmake .                                                  \
  -DSYSCONFDIR:PATH=%{prefix}                            \
  -DCMAKE_INSTALL_PREFIX:PATH=%{prefix}                  \
  -DCMAKE_BUILD_TYPE:STRING=Release                      \
  -DENABLE_PROFILING:BOOL=ON                             \
  -DWITH_DEBUG:BOOL=OFF                                  \
  -DWITH_VALGRIND:BOOL=OFF                               \
  -DENABLE_DEBUG_SYNC:BOOL=OFF                           \
  -DWITH_EXTRA_CHARSETS:STRING=all                       \
  -DWITH_SSL:STRING=bundled                              \
  -DWITH_UNIT_TESTS:BOOL=OFF                             \
  -DWITH_ZLIB:STRING=bundled                             \
  -DWITH_PARTITION_STORAGE_ENGINE:BOOL=ON                \
  -DWITH_INNOBASE_STORAGE_ENGINE:BOOL=ON                 \
  -DWITH_ARCHIVE_STORAGE_ENGINE:BOOL=ON                  \
  -DWITH_BLACKHOLE_STORAGE_ENGINE:BOOL=ON                \
  -DWITH_PERFSCHEMA_STORAGE_ENGINE:BOOL=ON               \
  -DDEFAULT_CHARSET=utf8                                 \
  -DDEFAULT_COLLATION=utf8_general_ci                    \
  -DENABLED_LOCAL_INFILE:BOOL=ON                         \
  -DWITH_EMBEDDED_SERVER=0                               \
  -DINSTALL_LAYOUT:STRING=STANDALONE                     \
  -DCOMMUNITY_BUILD:BOOL=ON                              \
  -DWITHOUT_EXAMPLE_STORAGE_ENGINE=1                     \
  -DWITHOUT_NDBCLUSTER_STORAGE_ENGINE=1                  \
  -DENABLED_PROFILING=1                                  \
  -DINNODB_PAGE_ATOMIC_REF_COUNT=1                       \
  -DWITH_INNODB_MEMCACHED=1;

make -j `cat /proc/cpuinfo | grep processor| wc -l`

%install
make DESTDIR=$RPM_BUILD_ROOT install
cp %{_sourcedir}/my.cnf $RPM_BUILD_ROOT%{prefix}/

%clean
#rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/*

%files
%defattr(-, %{MYSQL_USER}, %{MYSQL_GROUP})
%attr(755, %{MYSQL_USER}, %{MYSQL_GROUP}) %{prefix}/*

%pre
if ! id %{MYSQL_USER} > /dev/null 2>&1;then
useradd -M -s /sbin/nologin %{MYSQL_USER}
fi

%post
if [ -f %{prefix}/support-files/mysql.server > /dev/null 2>&1 ]  && [ ! -f %{_initddir}/mysql > /dev/null 2>&1 ];then
cp %{prefix}/support-files/mysql.server %{_initddir}/mysql
chmod +x %{_initddir}/mysql
chkconfig --level 2345 %{_initddir}/mysql on
fi

if [ ! -f %{_sysconfdir}/my.cnf ];then
cp %{prefix}/my.cnf %{_sysconfdir}/my.cnf
else
cp %{prefix}/my.cnf %{_sysconfdir}/my.cnf.rpmnew
fi

%preun
if [ -f %{_sysconfdir}/my.cnf ];then
mv %{_sysconfdir}/my.cnf %{_sysconfdir}/my.cnf.rpmold
fi

if [ -f %{_initddir}/mysql ];then
mv %{_initddir}/mysql %{_initddir}/mysql.rpmold
fi

%postun
rm -rf %{prefix}
userdel -r %{MYSQL_USER} >/dev/null 2>&1

%changelog
