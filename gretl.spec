%define name	gretl
%define version	1.9.4
%define release	1

%define api	1.0
%define major 	0

%define libname		%mklibname %name %api %major
%define develname	%mklibname %name -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Econometric analysis tool
License:	GPLv2+
Group:		Sciences/Other
Source0:	http://prdownloads.sourceforge.net/gretl/%{name}-%{version}.tar.bz2
Source1:	.abf.yml
# Recent cputoolize cannot handle variables in AC_CONFIG_AUX_DIR: 
# patch removes the $srcdir variable from this setting in configure.in
# - AdamW 2007/11
Patch0:		gretl-1.6.5-cputoolize.patch
URL:		http://gretl.sourceforge.net/
BuildRequires:	libpng-devel
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	blas-devel
BuildRequires:	libfftw-devel
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(gtksourceview-2.0)
BuildRequires:	libgnomeprintui-devel
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	lapack-devel
BuildRequires:	libreadline-devel
BuildRequires:	termcap-devel
BuildRequires:	libmpfr-devel
BuildRequires:	gnuplot

%description
Gretl is a software package for econometric analysis, written in the 
C programming language. 

%package -n %{libname}
Summary: Shared library for gretl
License: GPLv2+
Group: System/Libraries
Obsoletes: %mklibname %name 1.0

%description -n %{libname}
Gretl is a software package for econometric analysis, written in the 
C programming language.

%package -n %{develname}
Summary: Development headers for gretl library
License: GPLv2+
Group: Development/C
Provides:	lib%{name}-devel
Provides:	%{name}-devel
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname gretl 1.0 -d}

%description -n %{develname}
Gretl is a software package for econometric analysis, written in the 
C programming language.

%prep
%setup -q
%patch0 -p1 -b .cputoolize

%build
export CFLAGS="%{optflags} -fPIC"
%configure2_5x
%make LDFLAGS="%{?ldflags}"

%install
%makeinstall_std
mv doc/tex/extract_scripts %{buildroot}%{_bindir}/%{name}_extract_scripts

%find_lang %{name}
 
%files -f %name.lang
%defattr(-,root,root)
%doc README ChangeLog
%doc doc/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/gtksourceview-2.0/language-specs/*.lang
%{_datadir}/mime-info/*
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_mandir}/man1/*
%{_libdir}/gretl-gtk2

%files -n %{libname}
%defattr (-,root,root)
%_libdir/*%{api}.so.%{major}*

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/*
%_libdir/*.so
%_libdir/pkgconfig/gretl.pc


%changelog
* Wed Mar 16 2011 Stéphane Téletchéa <steletch@mandriva.org> 1.9.4-1mdv2011.0
+ Revision: 645214
- update to new version 1.9.4

* Wed Dec 01 2010 Sandro Cazzaniga <kharec@mandriva.org> 1.9.3-1mdv2011.0
+ Revision: 604518
- new bugfixe release
- Update to 1.8.7
- Remove Patch2, now useless

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 1.8.6-2mdv2010.1
+ Revision: 503556
- rebuild for new gmp

* Wed Dec 16 2009 Frederik Himpe <fhimpe@mandriva.org> 1.8.6-1mdv2010.1
+ Revision: 479589
- update to new version 1.8.6

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 1.8.5-1mdv2010.1
+ Revision: 462397
- update to new version 1.8.5

* Sat Aug 29 2009 Frederik Himpe <fhimpe@mandriva.org> 1.8.4-1mdv2010.0
+ Revision: 422264
- Update to new version 1.8.4
- Remove ldflags and string format patch: integrated upstream

* Wed Aug 12 2009 Frederik Himpe <fhimpe@mandriva.org> 1.8.3-1mdv2010.0
+ Revision: 415767
- Update to new version 1.8.3
- Update string format patch
- Update link patch and rename it to ldflags to make it more obvious
  what it does

* Thu Mar 12 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.7.9-2mdv2009.1
+ Revision: 354332
- rebuild for latest readline

* Wed Jan 21 2009 Funda Wang <fwang@mandriva.org> 1.7.9-1mdv2009.1
+ Revision: 332259
- add BRs
- add BR
- New version 1.7.9

* Sat Jul 12 2008 Funda Wang <fwang@mandriva.org> 1.7.5-1mdv2009.0
+ Revision: 234126
- New version 1.7.5
- drop patch1, it is not needed anymore
- fix libname

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Nov 12 2007 Adam Williamson <awilliamson@mandriva.org> 1.6.5-2mdv2008.1
+ Revision: 108322
- add gfortran.patch to fix gfortran detection test (from FreeBSD)
- oops - didn't meant to put autoreconf in there.
- add cputoolize.patch to fix a problem with configure.in that stops cputoolize working
- buildrequires blas-devel, not libblas-devel
- rebuild for new lapack
- new devel policy
- new license policy
- spec clean

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'

* Sun May 20 2007 Adam Williamson <awilliamson@mandriva.org> 1.6.5-1mdv2008.0
+ Revision: 28753
- add termcap to BuildRequires to fix readline support and hence build (thanks per oyvind)
- move pkgconfig file out of main package to devel package
- move non-library stuff out of lib package to main package
- build with -fPIC to fix x86-64 build
- add XDG menu
- correct groups for lib / devel packages
- improve description
- fix BuildRequires
- rebuild to fix #26200
- 1.6.5


* Thu Apr 13 2006 Jerome Soyer <saispo@mandriva.org> 1.5.1-1mdk
- New release 1.5.1

* Thu Jul 21 2005 Nicolas L�cureuil <neoclust@mandriva.org> 1.4.1-1mdk
- New release 1.4.1

* Wed Feb 23 2005 Lenny Cartier <lenny@mandrakesoft.com> 1.3.2-1mdk
- 1.3.2

* Thu Jan 13 2005 Lenny Cartier <lenny@mandrakesoft.com> 1.3.0-1mdk
- 1.3.0

* Sat Dec 27 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.2.0-1mdk
- 1.2.0

