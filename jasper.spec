Summary:	JasPer - collection of software for coding and manipulation of images
Summary(pl):	JasPer - zestaw oprogramowania do obróbki obrazków
Name:		jasper
Version:	1.500.3
Release:	1
License:	BSD-like
Group:		Libraries
Group(de):	Libraries
Group(es):	Bibliotecas
Group(fr):	Librairies
Group(pl):	Biblioteki
Source0:	http://www.ece.ubc.ca/~mdadams/jasper/software/%{name}-%{version}.zip
URL:		http://www.ece.ubc.ca/~mdadams/jasper/
BuildRequires:	autoconf
BuildRequires:	libjpeg-devel
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JasPer is a collection of software (i.e., a library and application
programs) for the coding and manipulation of images. This software can
handle image data in a variety of formats. One such format supported
by JasPer is the JPEG-2000 code stream format defined in ISO/IEC
15444-1:2000 (but JasPer contains only partial implementation).

%description -l pl
JasPer to zestaw oprogramowania (biblioteka i aplikacje) do kodowania
i obróbki obrazków w ró¿nych formatach. Jednym z nich jest JPEG-2000
zdefiniowany w ISO/IEC 15444-1:2000 (JasPer zawiera tylko czê¶ciow±
implementacjê tego formatu).

%package devel
Summary:	JasPer - header files
Summary(pl):	JasPer - pliki nag³ówkowe
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
Header files needed to compile programs with libjasper.

%description devel -l pl
Pliki nag³ówkowe potrzebne do linkowana z libjasper.

%package static
Summary:	JasPer - static library
Summary(pl):	JasPer - biblioteka statyczna
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Static version of libjasper..

%description static -l pl
Statyczna biblioteka libjasper.

%prep
%setup -q

%build
autoconf
%configure \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf LICENSE NEWS README

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc *.gz doc/jasper*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%attr(755,root,root) %{_libdir}/lib*.la
%{_includedir}/jasper

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
