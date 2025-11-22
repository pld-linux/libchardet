Summary:	Mozilla's universal character set detector
Name:		libchardet
Version:	1.0.5
Release:	1
License:	MPL
URL:		http://ftp.oops.org/pub/oops/libchardet/
Source0:	https://github.com/Joungkyun/libchardet/archive/%{version}.tar.gz
# Source0-md5:	218efba7ae9789202d40fe8133311729
Patch0:		%{name}-1.0.4-pc.in.patch
BuildRequires:	coreutils
BuildRequires:	libstdc++-devel

%description
libchardet provides an interface to Mozilla's universal charset
detector, which detects the charset used to encode data.

%package devel
Summary:	Header and object files for development using libchardet
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The libchardet-devel package contains the header and object files
necessary for developing programs which use the libchardet libraries.

%prep
%setup -q
%patch -P0 -p1

# Fix rpmlint file-not-utf8
cd man/en
for i in detect_init.3 detect_obj_free.3 detect_obj_init.3 detect_reset.3 ; do
  iconv --from=ISO-8859-1 --to=UTF-8 $i > $i.conv
  mv $i.conv $i
done
cd ../..

%build
%configure \
	--disable-static \
	--enable-shared \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# remove all '*.la' files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# remove LICENSE file from %%_docdir
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/{LICENSE,Changelog}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog README.md
%doc LICENSE
%{_libdir}/%{name}.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chardet-config
%{_libdir}/*.so
%{_pkgconfigdir}/chardet.pc
%{_includedir}/chardet/*.h
%{_mandir}/man3/*
%lang(ko) %{_mandir}/ko/man3/detect*.3*
