#
# Conditional build:
%bcond_without	opengl	# (OpenGL-based) jiv viewer
%bcond_without	heif	# support for libheif and HEIC codec (experimental)
#
Summary:	JasPer - collection of software for coding and manipulation of images
Summary(pl.UTF-8):	JasPer - zestaw oprogramowania do obróbki obrazków
Name:		jasper
Version:	3.0.6
Release:	2
Epoch:		0
License:	JasPer v2.0 (BSD-like)
Group:		Libraries
#Source0Download: https://github.com/jasper-software/jasper/releases
Source0:	https://github.com/jasper-software/jasper/releases/download/version-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f9388d52a6220303141a42d4c2c81e62
Patch0:		parallel-doc-build.patch
URL:		https://www.ece.uvic.ca/~frodo/jasper/
%{?with_opengl:BuildRequires:	OpenGL-glut-devel}
BuildRequires:	cmake >= 3.12
BuildRequires:	doxygen
BuildRequires:	gcc >= 6:4.7
%{?with_heif:BuildRequires:	libheif-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tex-latex-adjustbox
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex-ams
BuildRequires:	texlive-latex-extend
BuildRequires:	texlive-latex-wasysym
BuildRequires:	texlive-tex-xkeyval
BuildRequires:	texlive-xetex
BuildRequires:	unzip
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JasPer is a collection of software (i.e., a library and application
programs) for the coding and manipulation of images. This software can
handle image data in a variety of formats. One such format supported
by JasPer is the JPEG-2000 code stream format defined in ISO/IEC
15444-1:2000 (but JasPer contains only partial implementation).

%description -l pl.UTF-8
JasPer to zestaw oprogramowania (biblioteka i aplikacje) do kodowania
i obróbki obrazków w różnych formatach. Jednym z nich jest JPEG-2000
zdefiniowany w ISO/IEC 15444-1:2000 (JasPer zawiera tylko częściową
implementację tego formatu).

%package libs
Summary:	JasPer library
Summary(pl.UTF-8):	Biblioteka JasPer
Group:		Libraries

%description libs
JasPer library.

%description libs -l pl.UTF-8
Biblioteka JasPer.

%package devel
Summary:	JasPer - header files
Summary(pl.UTF-8):	JasPer - pliki nagłówkowe
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	libjpeg-devel
Obsoletes:	jasper-static < 2

%description devel
Header files needed to compile programs with libjasper.

%description devel -l pl.UTF-8
Pliki nagłówkowe potrzebne do konsolidacji z libjasper.

%package jiv
Summary:	JasPer Image Viewer
Summary(pl.UTF-8):	Przeglądarka obrazków JasPer
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

%description jiv -l pl.UTF-8
Prosta przeglądarka obrazków JasPer. Ma podstawową funkcjonalność
przewijania i powiększania. Poszczególne składniki obrazka mogą być
oglądane oddzielnie. Składowe kolory mogą być oglądane także razem,
jako złożony obraz. Aktualnie przeglądarka ma tylko prostą obsługę
koloru. Rozpoznaje przestrzenie RGB i YCbCr, ale nie używa krzywych
reprodukcji tonalnej i podobnych rzeczy mających za zadanie dokładne
odwzorowanie koloru. Do podstawowych celów testowych taka obsługa
kolorów powinna jednak wystarczyć.

%prep
%setup -q
%patch -P0 -p1

%build
# there is upstream directory named "build", use different name
install -d builddir
cd builddir
# note: build/jasper.pc.in expects CMAKE_INSTALL_INCLUDEDIR and CMAKE_INSTALL_LIBDIR relative to CMAKE_INSTALL_PREFIX
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DJAS_ENABLE_AUTOMATIC_DEPENDENCIES=OFF \
	%{!?with_opengl:-DJAS_ENABLE_OPENGL=OFF} \
	%{!?with_heif:-DJAS_ENABLE_LIBHEIF=OFF} \
	%{!?with_heif:-DJAS_INCLUDE_HEIC_CODEC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# PDFs packaged as %doc, HTML redundant
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/{html,*.pdf,README.md}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/imgcmp
%attr(755,root,root) %{_bindir}/imginfo
%attr(755,root,root) %{_bindir}/jasper
%{_mandir}/man1/imgcmp.1*
%{_mandir}/man1/imginfo.1*
%{_mandir}/man1/jasper.1*

%files libs
%defattr(644,root,root,755)
%doc ChangeLog LICENSE.txt NEWS.txt README.md doc/jpeg2000.pdf
%attr(755,root,root) %{_libdir}/libjasper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjasper.so.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjasper.so
%{_includedir}/jasper
%{_pkgconfigdir}/jasper.pc

%if %{with opengl}
%files jiv
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jiv
%{_mandir}/man1/jiv.1*
%endif
