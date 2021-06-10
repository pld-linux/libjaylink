#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
#
Summary:	Library to access J-Link devices
Summary(pl.UTF-8):	Biblioteka dostępu do urządzeń J-Link
Name:		libjaylink
Version:	0.2.0
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://gitlab.zapb.de/libjaylink/libjaylink/-/tags
Source0:	https://gitlab.zapb.de/libjaylink/libjaylink/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	613d3e71dca289e997ee2773ca6a0d26
URL:		https://gitlab.zapb.de/libjaylink/libjaylink
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gcc >= 6:4.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-devel >= 1.0.16
BuildRequires:	pkgconfig >= 1:0.23
Requires:	libusb >= 1.0.16
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libjaylink is a shared library written in C to access SEGGER J-Link
and compatible devices.

%description -l pl.UTF-8
libjaylink to biblioteka współdzielona w C, służąca do dostępu do
urządzeń SEGGER J-Link i kompatybilnych z nimi.

%package devel
Summary:	Header files for libjaylink library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libjaylink
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libusb-devel >= 1.0.16

%description devel
Header files for libjaylink library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libjaylink.

%package static
Summary:	Static libjaylink library
Summary(pl.UTF-8):	Statyczna biblioteka libjaylink
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libjaylink library.

%description static -l pl.UTF-8
Statyczna biblioteka libjaylink.

%package apidocs
Summary:	API documentation for libjaylink library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libjaylink
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libjaylink library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libjaylink.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with apidocs}
doxygen
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libjaylink.la

install -d $RPM_BUILD_ROOT/lib/udev/rules.d
%{__sed} -e 's/MODE="664", GROUP="plugdev"/TAG+="uaccess"/g' contrib/99-libjaylink.rules >$RPM_BUILD_ROOT/lib/udev/rules.d/60-libjaylink.rules

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libjaylink.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjaylink.so.0
/lib/udev/rules.d/60-libjaylink.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjaylink.so
%{_includedir}/libjaylink
%{_pkgconfigdir}/libjaylink.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libjaylink.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doxy/html/{search,*.css,*.html,*.js,*.png}
%endif
