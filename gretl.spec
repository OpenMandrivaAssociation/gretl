%define name	gretl
%define version	1.6.5
%define release	%mkrel 2

%define major	1.0

%define libname		%mklibname %name %major
%define develname	%mklibname %name -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Econometric analysis tool
License:	GPLv2+
Group:		Sciences/Other
Source0:	http://prdownloads.sourceforge.net/gretl/%{name}-%{version}.tar.bz2
# Recent cputoolize cannot handle variables in AC_CONFIG_AUX_DIR: 
# patch removes the $srcdir variable from this setting in configure.in
# - AdamW 2007/11
Patch0:		gretl-1.6.5-cputoolize.patch
URL:		http://gretl.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libpng-devel
BuildRequires:	gtk+2-devel
BuildRequires:	glib2-devel
BuildRequires:	blas-devel
BuildRequires:	libfftw-devel
BuildRequires:	libxml2-devel
BuildRequires:	lapack-devel
BuildRequires:	libreadline-devel
BuildRequires:	termcap-devel
BuildRequires:	libgmp-devel
BuildRequires:	libmpfr-devel
BuildRequires:	gnuplot

%description
Gretl is a software package for econometric analysis, written in the 
C programming language. 

%package -n %{libname}
Summary: Shared library for gretl
License: GPLv2+
Group: System/Libraries

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
rm -rf %{buildroot}
%setup -q
%patch0 -p1 -b .cputoolize

%build
autoreconf
CFLAGS="$RPM_OPT_FLAGS -fPIC" %configure2_5x
%make
%make doc

%install
%__rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Gretl
Comment=Econometric analysis tool
Exec=%{_bindir}/%{name} 
Icon=mathematics_section
Terminal=false
Type=Application
StartupNotify=true
Categories=Education;Science;DataVisualization;
EOF

%find_lang %{name}
 
%post 
%{update_menus}

%post -n %{libname} -p /sbin/ldconfig
 
%postun 
%{clean_menus}

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root)
%doc README ChangeLog EXTENDING
%doc doc/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_mandir}/man1/*
%{_libdir}/gretl-gtk2

%files -n %{libname}
%defattr (-,root,root)
%_libdir/*.so.*

%files -n %{develname}
%defattr (-,root,root)
%{_includedir}/*
%_libdir/*.la
%_libdir/*.so
%_libdir/pkgconfig/gretl.pc
