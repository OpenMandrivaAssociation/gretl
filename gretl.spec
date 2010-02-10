%define name	gretl
%define version	1.8.6
%define release	%mkrel 2

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
# Recent cputoolize cannot handle variables in AC_CONFIG_AUX_DIR: 
# patch removes the $srcdir variable from this setting in configure.in
# - AdamW 2007/11
Patch0:		gretl-1.6.5-cputoolize.patch
Patch2:		gretl-1.7.9-fix-libdir.patch
URL:		http://gretl.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libpng-devel
BuildRequires:	gtk+2-devel
BuildRequires:	glib2-devel
BuildRequires:	blas-devel
BuildRequires:	libfftw-devel
BuildRequires:	libxml2-devel
BuildRequires:	gtksourceview-devel
BuildRequires:	libgnomeprintui-devel
BuildRequires:	gnomeui2-devel
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
%patch2 -p0 -b .lib

%build
export CFLAGS="%{optflags} -fPIC"
%configure2_5x
%make LDFLAGS="%{?ldflags}"

%install
%__rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name}
 
%if %mdkversion < 200900
%post 
%{update_menus}
%endif

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
 
%if %mdkversion < 200900
%postun 
%{clean_menus}
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

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
%_libdir/*.la
%_libdir/*.so
%_libdir/pkgconfig/gretl.pc
