Summary:	Mozilla's universal character set detector
Summary(pl.UTF-8):	Uniwersalny wykrywacz zestawu znaków Mozilli
Name:		libchardet
Version:	1.0.6
Release:	1
License:	MPL v1.1
Group:		Libraries
#Source0Download: https://github.com/Joungkyun/libchardet/releases
Source0:	https://github.com/Joungkyun/libchardet/releases/download/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	0c5b054e20a1c6de1a9b59df77ae715d
Patch0:		%{name}-1.0.4-pc.in.patch
URL:		http://ftp.oops.org/pub/oops/libchardet/
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libchardet provides an interface to Mozilla's universal charset
detector, which detects the charset used to encode data.

%description -l pl.UTF-8
libchardet udostępnia interfejs do uniwersalnego narzędzia Mozilli do
wykrywania zestawu znaków, wykrywającego zestaw znaków użyty do
kodowania danych.

%package devel
Summary:	Header files for development using libchardet
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libchardet
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files necessary for developing
programs which use the libchardet library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
wykorzystujących bibliotekę libchardet.

%prep
%setup -q
%patch -P0 -p1

# Fix rpmlint file-not-utf8
cd man/en
for i in detect_init.3 detect_obj_free.3 detect_obj_init.3 detect_reset.3 ; do
	iconv --from=ISO-8859-1 --to=UTF-8 $i > $i.conv
	%{__mv} $i.conv $i
done

%build
%configure \
	--disable-static \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libchardet.la

# remove LICENSE file from %%_docdir
%{__rm} $RPM_BUILD_ROOT%{_docdir}/%{name}/{LICENSE,Changelog}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changelog
%{_libdir}/libchardet.so.*.*.*
%ghost %{_libdir}/libchardet.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chardet-config
%{_libdir}/libchardet.so
%{_pkgconfigdir}/chardet.pc
%{_includedir}/chardet
%{_mandir}/man3/detect*.3*
%lang(ko) %{_mandir}/ko/man3/detect*.3*
