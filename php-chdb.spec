%define modname chdb
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B15_%{modname}.ini

Summary:	A fast database for constant data with memory sharing across processes
Name:		php-%{modname}
Version:	1.0.2
Release:	4
Group:		Development/PHP
License:	BSD
URL:		https://pecl.php.net/package/chdb
Source0:	http://pecl.php.net/get/chdb-%{version}.tgz
Source1:	B15_chdb.ini
BuildRequires:	pkgconfig
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	cmph-devel

%description
CHDB (constant hash database) is a fast key-value database for constant data,
realized by using a memory-mapped file and thus providing the following
functionalities:
- Extremely fast initial load, regardless of the size of the database.
- Only the pages of the file which are actually used are loaded from the disk.
- Once a page is loaded it is shared across multiple processes.
- Loaded pages are cached across multiple requests and even process recycling.
A typical use of CHDB is as a faster alternative to defining many PHP
constants. 
CHDB is internally implemented as a hash-table using a perfect hashing
function, thus guaranteeing worst case O(1) lookup time.

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

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
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-2mdv2012.0
+ Revision: 795408
- rebuild for php-5.4.x

* Thu Apr 19 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.2-1
+ Revision: 791877
- 1.0.2

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-4
+ Revision: 761207
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-3
+ Revision: 696400
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-2
+ Revision: 695373
- rebuilt for php-5.3.7

* Tue May 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1
+ Revision: 675425
- import php-chdb


* Tue May 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.1-1mdv2010.2
- initial Mandriva package
