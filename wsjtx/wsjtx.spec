Name:           wsjtx
Version:        20150910.5885
Release:        22%{?dist}
Summary:        Weak-signal digital mode for amateur radio

Group:          System Environment/Libraries
License:        GPLv3
URL:            http://physics.princeton.edu/pulsar/k1jt/wsjtx.html
Source0:        wsjtx-%{version}.tar.gz
BuildRequires:  hamlib-devel, cmake, asciidoc, rubygem-asciidoctor, gcc-gfortran, fftw-devel
BuildRequires:  qt5-qtbase-devel, qt5-qtmultimedia-devel
BuildRequires:  qt5-qtserialport-devel, qt5-qtdeclarative-devel

%description
WSJT facilitates basic digital communication using protocols explicitly optimized for a number of different propagation modes.

%prep
%setup -q

%build
mkdir build
cd build
cmake -D CMAKE_INSTALL_PREFIX=%{_prefix}/ ..
make

%install
cd build
make DESTDIR=$RPM_BUILD_ROOT install

%files
%doc AUTHORS BUGS COPYING README THANKS
%{_bindir}/*
%{_mandir}/man*/*
%{_mandir}/man*/.*
/usr/share/pixmaps/wsjtx_icon.png
/usr/share/applications/wsjtx.desktop
/usr/share/wsjtx/JPLEPH
