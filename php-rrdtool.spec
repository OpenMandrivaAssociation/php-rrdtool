%define realname RRDtool
%define modname rrdtool
%define dirname %{modname}
%define soname %{modname}.so
%define inifile 61_%{modname}.ini

%define mod_src rrdtool.c
%define mod_lib "-lrrd -lpng -lz -lm"
%define mod_def "-DHAVE_RRDTOOL -DCOMPILE_DL_RRDTOOL"

Summary:	The %{realname} module for PHP
Name:		php-%{modname}
Version:	0
Release:	%mkrel 34
Group:		Development/PHP
License:	GPL
URL:		http://ee-staff.ethz.ch/~oetiker/webtools/rrdtool/
Source0:	http://people.ee.ethz.ch/~oetiker/webtools/rrdtool/pub/contrib/php_rrdtool.tar.bz2
BuildRequires:	gettext-devel
BuildRequires:	rrdtool-devel >= 1.2.7
BuildRequires:	png-devel
BuildRequires:	zlib-devel
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The php-rrdtool package is a dynamic shared object (DSO) that adds RRDtool
support to PHP.

%prep

%setup -q -n rrdtool

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

#%{_usrsrc}/php-devel/buildext %{modname} %{mod_src} %{mod_lib} %{mod_def}

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%{__cat} > README.%{modname} << EOF
The php-rrdtool package contains a dynamic shared object (DSO) for PHP.
To activate it, make sure a file /etc/php.d/%{inifile} is present and
contains the line 'extension = %{soname}'.
EOF

%{__cat} > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
