#define _disable_lto 1

%define api		1.0
%define major		51
%define oldlibname	%mklibname %{name} 1.0
%define devname		%mklibname %{name} -d
%define oldlibname	%mklibname %{name} %{api} 44

# BLAS lib
%global blaslib flexiblas

%bcond openmpi	1

Summary:	A tool for econometric analysis
Name:		gretl
Version:	2025a
Release:	1
Group:		Sciences/Mathematics
License:	GPLv3+ and BSD and MIT
Url:		https://gretl.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
#Licensing of plugins used in gretl
Source1:	gretl_plugins.txt
BuildRequires:	desktop-file-utils
BuildRequires:	fonts-ttf-bitstream-vera
BuildRequires:	fonts-ttf-freefont
BuildRequires:	gnuplot
BuildRequires:	R-base
BuildRequires:	gmp-devel
BuildRequires:	gettext
BuildRequires:	mpfr-devel
BuildRequires:	readline-devel
BuildRequires:	unixODBC-devel
BuildRequires:	pkgconfig(%{blaslib})
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	pkgconfig(lapack)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libgsf-1)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
%if %{with openmpi}
BuildRequires:	pkgconfig(ompi)
%endif
Requires:	fonts-ttf-bitstream-vera
Requires:	fonts-ttf-freefont
Requires:	gnuplot
Requires:	R-base

%patchlist
gretl-2016b-fix-desktop-file.patch

%description
A cross-platform software package for econometric analysis,
written in the C programming language.

%files -f %{name}.lang
%doc ChangeLog CompatLog README gretl_plugins.txt
%{_bindir}/gretl*
%{_libdir}/gretl-gtk3/
%{_datadir}/%{name}/
%{_datadir}/metainfo/%{name}.metainfo.xml
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/%{name}*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}*.png
%{_iconsdir}/hicolor/*/mimetypes/*%{name}*
%{_mandir}/man1/*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		Development/C
%rename		%{oldlibname}

%description -n %{libname}
This package contains the shared library files for %{name}.

%files -n %{libname}
%{_libdir}/libgretl-%{api}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C

%description -n %{devname}
This package contains the development files for %{name}.

%files -n %{devname}
%{_libdir}/pkgconfig/gretl.pc
%{_libdir}/libgretl-%{api}.so
%{_includedir}/%{name}/

#----------------------------------------------------------------------------

%prep
%autosetup -p1

# fix include path
sed -i -e 's:includedir=${prefix}/include:includedir=${prefix}/include/gretl:' gretl.pc.in

# plugins licensing notes
install -pm644 %{SOURCE1} .

%build
export CC=gcc
export CXX=g++
LDFLAGS="%ldflags `pkg-config --libs ompi`"
export LAPACK_LIBS="`pkg-config --libs %{blaslib}`"

%configure \
	--disable-static \
	--disable-rpath \
	--disable-avx \
%if %{with openmpi}
	--with-mpi \
	--with-mpi-lib=%{_libdir}/openmpi/lib/ \
%endif
	--enable-build-editor \
	--enable-build-addons \
	--enable-addons-doc \
	--with-libR \
	--with-odbc \
	--with-gsf
%make_build

%install
%make_install

# locales
%find_lang %{name}

#we don't want these
find %{buildroot} -name "*.la" -delete

