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
Patch0:		php_rrdtool-php54x.diff
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
%patch0 -p0

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


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 0-34mdv2012.0
+ Revision: 797034
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 0-33
+ Revision: 761286
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0-32
+ Revision: 696463
- rebuilt for php-5.3.8

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 0-31
+ Revision: 646679
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 0-30mdv2011.0
+ Revision: 629865
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 0-29mdv2011.0
+ Revision: 628179
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0-28mdv2011.0
+ Revision: 600525
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0-27mdv2011.0
+ Revision: 588863
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 0-26mdv2010.1
+ Revision: 514647
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0-25mdv2010.1
+ Revision: 485461
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 0-24mdv2010.1
+ Revision: 468247
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 0-23mdv2010.0
+ Revision: 451353
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 0-22mdv2010.0
+ Revision: 397591
- Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 0-21mdv2010.0
+ Revision: 377023
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0-20mdv2009.1
+ Revision: 346602
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 0-19mdv2009.1
+ Revision: 341793
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0-18mdv2009.1
+ Revision: 323047
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0-17mdv2009.1
+ Revision: 310302
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 0-16mdv2009.0
+ Revision: 238426
- rebuild

* Tue Jun 17 2008 Oden Eriksson <oeriksson@mandriva.com> 0-15mdv2009.0
+ Revision: 222532
- fix deps
- rebuilt against new rrdtool-devel

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 0-14mdv2009.0
+ Revision: 200263
- rebuilt for php-5.2.6

* Tue Feb 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0-13mdv2008.1
+ Revision: 162767
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 0-12mdv2008.1
+ Revision: 107713
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0-11mdv2008.0
+ Revision: 77571
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0-10mdv2008.0
+ Revision: 39519
- use distro conditional -fstack-protector

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 0-9mdv2008.0
+ Revision: 33872
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 0-8mdv2008.0
+ Revision: 21352
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0-7mdv2007.0
+ Revision: 117617
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 0-6mdv2007.0
+ Revision: 78100
- rebuilt for php-5.2.0
- Import php-rrdtool

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 0-5
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 0-4mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0-3mdk
- rebuilt for php-5.1.4

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0-2mdk
- rebuilt for php-5.1.3

* Thu Apr 27 2006 Oden Eriksson <oeriksson@mandriva.com> 0-1mdk
- reintroduced into contrib

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11_1.0.49-1mdk
- 4.3.11

* Mon Mar 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0.49-5mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0.49-4mdk
- rebuilt against a non hardened-php aware php lib

* Sun Jan 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0.49-3mdk
- cleanups

* Sat Jan 15 2005 Pascal Terjan <pterjan@mandrake.org> 4.3.10_1.0.49-2mdk
- rebuild

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.0.49-1mdk
- rebuild for 4.3.10

* Wed Nov 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_1.0.49-1mdk
- cosmetic rebuild

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_1.0.48-1mdk
- rebuild for php 4.3.9

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_1.0.48-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.0.48-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.0.48-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_1.0.48-1mdk
- initial cooker contrib

