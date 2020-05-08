%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define api		1.0
%define major		33
%define libname		%mklibname %{name} %{api} %{major}
%define devname		%mklibname -d %{name}

Summary:	A tool for econometric analysis
Name:		gretl
Version:	2020b
Release:	1
Group:		Sciences/Mathematics
License:	GPLv3+ and BSD and MIT
Url:		http://gretl.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
#Licensing of plugins used in gretl
Source1:	gretl_plugins.txt
#Patch1:		gretl-1.9.12-linking.patch
Patch2:		gretl-2016b-fix-desktop-file.patch

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
BuildRequires:	pkgconfig(blas)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	pkgconfig(lapack)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libgsf-1)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(ncurses)
Requires:	fonts-ttf-bitstream-vera
Requires:	fonts-ttf-freefont
Requires:	gnuplot
Requires:	R-base

%description
A cross-platform software package for econometric analysis,
written in the C programming language.

%files -f %{name}.lang
%doc ChangeLog CompatLog README.audio README gretl_plugins.txt
%{_bindir}/gretl*
%{_libdir}/gretl-gtk3/
%{_datadir}/%{name}/
%{_mandir}/man1/*

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		Development/C

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
%setup -q
%patch2 -p1 -b .desktop

# fix include path
sed -i -e 's:includedir=${prefix}/include:includedir=${prefix}/include/gretl:' gretl.pc.in

# plugins licensing notes
install -pm644 %{SOURCE1} .

%build
%configure2_5x \
	--disable-static \
	--disable-rpath \
	--with-libR \
	--with-odbc \
	--with-gsf
%make_build

%install
%make_install

%find_lang %{name}

#we don't want these
find %{buildroot} -name "*.la" -delete

%files -f %{name}.lang
%doc ChangeLog CompatLog README gretl_plugins.txt
%{_bindir}/gretl*
%{_libdir}/gretl-gtk3/
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/*/mimetypes/*.png
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libgretl-%{api}.so.%{major}
%{_libdir}/libgretl-%{api}.so.%{major}.*

%files -n %{devname}
%{_libdir}/pkgconfig/gretl.pc
%{_libdir}/libgretl-%{api}.so
%{_includedir}/%{name}/
