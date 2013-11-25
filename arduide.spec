Summary:	IDE for Arduino
Name:		arduide
Version:	20131121
Release:	1
License:	GPL v2
Group:		X11/Applications
# git clone git://gitorious.org/arduide/arduide.git
# cd arduide
# git archive --format=tar --prefix=arduide-20121215/ HEAD | xz -c > arduide-20121215.tar.xz
Source0:	%{name}-%{version}.tar.xz
# Source0-md5:	3215b662adc3c655c23ecb9dafd2a860
Patch0:		%{name}-toolchain.patch
URL:		http://mupuf.org/project/arduide/
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtWebKit-devel
BuildRequires:	cmake
BuildRequires:	grantlee-devel
BuildRequires:	libstdc++-devel
BuildRequires:	qscintilla-devel
BuildRequires:	udev-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ArduIDE is a Qt-based IDE for the open-source Arduino electronics
prototyping platform.

%prep
%setup -q
%patch0 -p1

# fix non-standard paths
%{__sed} -i "s|/arduino-ide/translations|/qt/translations|" CMakeLists.txt
%{__sed} -i "s|/share/arduino-ide/plugins|/%{_lib}/arduino-ide/plugins|" CMakeLists.txt
%{__sed} -i "s|/share/icons/|/share/pixmaps/|" CMakeLists.txt

%build
install -d build
cd build
%cmake .. \
	-DUSE_FHS_PATHS=ON
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --without-mo --with-qm

mv $RPM_BUILD_ROOT%{_desktopdir}/{arduino-ide,arduide}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/arduino-ide

%dir %{_libdir}/arduino-ide
%dir %{_libdir}/arduino-ide/plugins
%attr(755,root,root) %{_libdir}/arduino-ide/plugins/*.so

%dir %{_datadir}/arduino-ide
%{_datadir}/arduino-ide/libraries
%{_desktopdir}/arduide.desktop
%{_pixmapsdir}/arduide.png

