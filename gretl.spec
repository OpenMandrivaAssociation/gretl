%define name gretl
%define version 1.6.5
%define release %mkrel 1

%define major 1.0

%define libname %mklibname %name %major
%define libnamedev %mklibname %name %major -d

Version: %{version}
Summary: Econometric analysis tool
Name: %{name}
Release: %{release}
License: GPL
Group: Sciences/Other
Source: http://prdownloads.sourceforge.net/gretl/%{name}-%{version}.tar.bz2
URL: http://gretl.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: libpng-devel gtk+2-devel glib2-devel libblas-devel libfftw-devel libxml2-devel lapack-devel libreadline-devel termcap-devel libgmp-devel libmpfr-devel
BuildRequires: gnuplot

%description
Gretl is a software package for econometric analysis, written in the 
C programming language. 

%package -n %libname
Summary: Shared library for gretl
License: GPL
Group: System/Libraries

%description -n %libname
Gretl is a software package for econometric analysis, written in the 
C programming language.

%package -n %libname-devel
Summary: Development headers for gretl library
License: GPL
Group: Development/C
Provides: libgretl-devel
Requires: %libname = %version

%description -n %libname-devel
Gretl is a software package for econometric analysis, written in the 
C programming language.

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC" ./configure --prefix=%_prefix --datadir=%_datadir --mandir=%_mandir --libdir=%_libdir
%make
%make doc

%install
%__rm -rf $RPM_BUILD_ROOT
%makeinstall

mkdir -p %{buildroot}/%{_menudir}
cat > %{buildroot}/%{_menudir}/%{name} <<EOF
?package(%{name}):\
command="/usr/bin/gretl"\
title="Gretl"\
longtitle="Econometric analysis"\
needs="x11"\
icon="mathematics_section.png"\
section="Applications/Sciences/Mathematics" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Gretl
Comment=Econometric analysis tool
Exec=%{_bindir}/%{name} 
Icon=%{_iconsdir}/mathematics_section.png
Terminal=false
Type=Application
StartupNotify=true
Categories=Education;Science;DataVisualization;X-MandrivaLinux-MoreApplications-Sciences-NumericalAnalysis
EOF

%find_lang %name
 
%post 
%update_menus

%post -n %libname -p /sbin/ldconfig
 
%postun 
%clean_menus

%postun -n %libname -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc README ChangeLog EXTENDING
%doc doc/*
%{_bindir}/*
%{_datadir}/%{name}/
%{_menudir}/*
%{_datadir}/applications/mandriva-%{name}.desktop
%_mandir/man1/*
%_libdir/gretl-gtk2

%files -n %libname
%defattr (-,root,root)
%_libdir/*.so.*

%files -n %libname-devel
%defattr (-,root,root)
%{_includedir}/*
%_libdir/*.la
%_libdir/*.so
%_libdir/pkgconfig/gretl.pc
