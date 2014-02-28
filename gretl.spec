%define api		1.0
%define major		9
%define libname		%mklibname %{name} %{api} %{major}
%define devname		%mklibname -d %{name}

Summary:	A tool for econometric analysis
Name:		gretl
Version:	1.9.14
Release:	1
Group:		Sciences/Mathematics
License:	GPLv3+ and BSD and MIT
Url:		http://gretl.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz
#Licensing of plugins used in gretl
Source1:	gretl_plugins.txt
Patch1:		gretl-1.9.12-linking.patch
BuildRequires:	desktop-file-utils
BuildRequires:	fonts-ttf-bitstream-vera
BuildRequires:	fonts-ttf-freefont
BuildRequires:	gnuplot
BuildRequires:	R-base
BuildRequires:	gmp-devel
BuildRequires:	mpfr-devel
BuildRequires:	readline-devel
BuildRequires:	unixODBC-devel
BuildRequires:	pkgconfig(blas)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	pkgconfig(lapack)
BuildRequires:	pkgconfig(libcurl)
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
%apply_patches

# fix flite detection
# FIXME: edit macros/flite.m4 and fix failing autoreconf
sed -i -e 's:register_cmu_us_kal:register_cmu_us_kal16:' configure

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
	--with-audio
%make

%install
%makeinstall includedir=%{buildroot}%{_includedir}/%{name}

chmod 0644 %{buildroot}%{_datadir}/%{name}/data/misc/galton.gdt

%find_lang %{name}

#font installation
rm -rf %{buildroot}/%{_datadir}/%{name}/fonts/*
ln -s %{_datadir}/fonts/TTF/Vera.ttf %{buildroot}/%{_datadir}/%{name}/fonts/Vera.ttf
ln -s %{_datadir}/fonts/TTF/VeraMono.ttf %{buildroot}/%{_datadir}/%{name}/fonts/VeraMono.ttf
ln -s %{_datadir}/fonts/TTF/FreeSans.ttf %{buildroot}/%{_datadir}/%{name}/fonts/FreeSans.ttf

