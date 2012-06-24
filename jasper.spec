#
# Conditional build:
%bcond_without opengl  # Disable OpenGL
#
Summary:	JasPer - collection of software for coding and manipulation of images
Summary(pl):	JasPer - zestaw oprogramowania do obr�bki obrazk�w
Name:		jasper
Version:	1.701.0
Release:	3
Epoch:		0
License:	BSD-like
Group:		Libraries
Source0:	http://www.ece.uvic.ca/~mdadams/jasper/software/%{name}-%{version}.zip
# Source0-md5:	22a9f74fc880e38dd125c60aa4e4ce97
URL:		http://www.ece.uvic.ca/~mdadams/jasper/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	glut-devel >= 3.7-12
%{?with_opengl:BuildRequires:       glut-devel >= 3.7-12}
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	unzip
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JasPer is a collection of software (i.e., a library and application
programs) for the coding and manipulation of images. This software can
handle image data in a variety of formats. One such format supported
by JasPer is the JPEG-2000 code stream format defined in ISO/IEC
15444-1:2000 (but JasPer contains only partial implementation).

%description -l pl
JasPer to zestaw oprogramowania (biblioteka i aplikacje) do kodowania
i obr�bki obrazk�w w r�nych formatach. Jednym z nich jest JPEG-2000
zdefiniowany w ISO/IEC 15444-1:2000 (JasPer zawiera tylko cz�ciow�
implementacj� tego formatu).

%package libs
Summary:	JasPer library
Summary(pl):	Biblioteka JasPer
Group:		Libraries

%description libs
JasPer library.

%description libs -l pl
Biblioteka JasPer.

%package devel
Summary:	JasPer - header files
Summary(pl):	JasPer - pliki nag��wkowe
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	libjpeg-devel

%description devel
Header files needed to compile programs with libjasper.

%description devel -l pl
Pliki nag��wkowe potrzebne do konsolidacji z libjasper.

%package static
Summary:	JasPer - static library
Summary(pl):	JasPer - biblioteka statyczna
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static version of libjasper.

%description static -l pl
Statyczna biblioteka libjasper.

%package jiv
Summary:	JasPer Image Viewer
Summary(pl):	Przegl�darka obrazk�w JasPer
Group:		X11/Applications/Graphics
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description jiv
Simple JasPer Image Viewer. Basic pan and zoom functionality is
provided. Components of an image may be viewed individually. Color
components may also be viewed together as a composite image. At
present, the jiv image viewer has only trivial support for color. It
recognizes RGB and YCbCr color spaces, but does not use tone
reproduction curves and the like in order to accurately reproduce
color. For basic testing purposes, however, the color reproduction
should suffice.

%description jiv -l pl
Prosta przegl�darka obrazk�w JasPer. Ma podstawow� funkcjonalno��
przewijania i powi�kszania. Poszczeg�lne sk�adniki obrazka mog� by�
ogl�dane oddzielnie. Sk�adowe kolory mog� by� ogl�dane tak�e razem,
jako z�o�ony obraz. Aktualnie przegl�darka ma tylko prost� obs�ug�
koloru. Rozpoznaje przestrzenie RGB i YCbCr, ale nie u�ywa krzywych
reprodukcji tonalnej i podobnych rzeczy maj�cych za zadanie dok�adne
odwzorowanie koloru. Do podstawowych cel�w testowych taka obs�uga
kolor�w powinna jednak wystarczy�.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
        %{?without_opengl:--disable-opengl} \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS README doc/jasper*
%attr(755,root,root) %{_bindir}/img*
%attr(755,root,root) %{_bindir}/jasper

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/jasper

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%if %{with opengl}
%files jiv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jiv
%endif
