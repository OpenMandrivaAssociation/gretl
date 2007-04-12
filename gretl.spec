%define name gretl
%define version 1.5.1
%define release 1mdk

%define major 1.0

%define libname %mklibname %name %major
%define libnamedev %mklibname %name %major -d

Version: %{version}
Summary: Econometric analysis
Name: %{name}
Release: %{release}
License: GPL
Group: Sciences/Other
Source: %{name}-%{version}.tar.bz2
URL: http://gretl.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: libgtk+extra-devel libblas-devel
BuildRequires: gnuplot


%description
Is a software package for econometric analysis, written in the 
C programming language. 

Is free software. You may redistribute it and/or modify it under
the terms of the GNU General Public License (GPL) as published by the
Free Software Foundation. 

Comprises a shared library, a command-line client program, and a
graphical client built using GTK+. The library and command-line 
client should compile and run on any platform that supports ANSI C;
the command-line client uses the GNU readline library if available.
The graphical client should compile and run on any platform that in
addition offers GTK+ version 1.2.3 or higher.

%package -n %libname
Summary: Econometric analysis
License: GPL
Group: Sciences/Other

%description -n %libname
Is a software package for econometric analysis, written in the
C programming language.

Is free software. You may redistribute it and/or modify it under
the terms of the GNU General Public License (GPL) as published by the
Free Software Foundation.

Comprises a shared library, a command-line client program, and a
graphical client built using GTK+. The library and command-line
client should compile and run on any platform that supports ANSI C;
the command-line client uses the GNU readline library if available.
The graphical client should compile and run on any platform that in
addition offers GTK+ version 1.2.3 or higher.

%package -n %libname-devel
Summary: Econometric analysis
License: GPL
Group: Sciences/Other
Provides: libgretl-devel
Requires: %libname = %version

%description -n %libname-devel
Is a software package for econometric analysis, written in the
C programming language.

Is free software. You may redistribute it and/or modify it under
the terms of the GNU General Public License (GPL) as published by the
Free Software Foundation.

Comprises a shared library, a command-line client program, and a
graphical client built using GTK+. The library and command-line
client should compile and run on any platform that supports ANSI C;
the command-line client uses the GNU readline library if available.
The graphical client should compile and run on any platform that in
addition offers GTK+ version 1.2.3 or higher.

%prep
rm -rf $RPM_BUILD_ROOT

%setup 

%build

./configure --prefix=%_prefix --datadir=%_datadir --mandir=%_mandir --libdir=%_libdir

make

%make doc

%install

%makeinstall


(cd $RPM_BUILD_ROOT
mkdir -p ./usr/lib/menu
cat > ./usr/lib/menu/%{name} <<EOF
?package(%{name}):\
command="/usr/bin/gretl"\
title="Gretl"\
longtitle="Econometric analysis"\
needs="x11"\
icon="mathematics_section.png"\
section="Applications/Sciences/Mathematics"
EOF
)
 
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
%doc README COPYING INSTALL ChangeLog EXTENDING
%doc doc/*
%{_bindir}/*
%{_datadir}/%{name}/
%{_menudir}/*
%_mandir/man1/*
%_libdir/pkgconfig/gretl.pc

%files -n %libname
%defattr (-,root,root)
%_libdir/*.so.*
%_libdir/gretl-gtk2

%files -n %libname-devel
%defattr (-,root,root)
%{_includedir}/*
%_libdir/*.la
%_libdir/*.so

