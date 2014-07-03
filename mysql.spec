Name: percona-server
Version:5.6.19
#Release: %(echo $RELEASE)%{?dist}
Release: 67.0
License: GPL
URL: http://www.percona.com/redir/downloads/Percona-Server-5.6/LATEST/source/tarball/percona-server-5.6.19-67.0.tar.gz 
Group: applications/database
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root 
BuildRequires: cmake
Packager: q_yxian@163.com
Autoreq: no
Source: percona-server-5.6.19-67.0.tar.gz
prefix: /usr/local/%{name}-%{version}-%{release}
Summary: percona server 5.6.19-67.0

%description 
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software.

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
  -DWITH_EXTRA_CHARSETS=all                              \
  -DENABLED_LOCAL_INFILE:BOOL=ON                         \
  -DWITH_EMBEDDED_SERVER=0                               \
  -DINSTALL_LAYOUT:STRING=STANDALONE                     \
  -DCOMMUNITY_BUILD:BOOL=ON                              \
  -DMYSQL_SERVER_SUFFIX='-r5436';

make -j `cat /proc/cpuinfo | grep processor| wc -l`

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, %{MYSQL_USER}, %{MYSQL_GROUP})
%attr(755, %{MYSQL_USER}, %{MYSQL_GROUP}) %{prefix}/*

%pre

%post
ln -s %{prefix}/lib %{prefix}/lib64

%preun

%changelog
