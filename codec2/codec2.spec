Name:           codec2
Version:        0.5
Release:        1%{?dist}
Summary:        Next-Generation Digital Voice for Two-Way Radio
License:        LGPLv2 

URL:            http://rowetel.com/codec2.html
Source0:        codec2-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  speex-devel
%if 0%{?fedora} >= 22
BuildRequires:  speexdsp-devel
%endif


%description
Codec 2 is an open source (LGPL licensed) speech codec for 2400 bit/s
and below. This is the runtime library package.


%package devel
Summary:        Development files for Codec 2 
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Codec 2 is an open source (LGPL licensed) speech codec for 2400 bit/s
and below. This package contains the development files required to 
compile programs that use codec2.


%package devel-examples
Summary:        Example code for Codec 2
Requires:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch

%description devel-examples
Example code for Codec 2


%prep
%setup -q -n codec2-%{version}


%build
rm -rf build_linux && mkdir build_linux && pushd build_linux
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       ../

make %{?_smp_mflags}


%install
pushd build_linux
%make_install
popd

# Create and install pkgconfig file
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat > %{buildroot}%{_libdir}/pkgconfig/codec2.pc << EOF
prefix=%{_prefix}
exec_prefix=\${prefix}
includedir=\${prefix}/include/%{name}
libdir=\${exec_prefix}/%{_lib}

Name: codec2
Description: Next-Generation Digital Voice for Two-Way Radio
Version: %{version}
Cflags: -I\${includedir}
Libs: -L\${libdir} -l%{name}
EOF


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{!?_licensedir:%global license %doc}
%license COPYING
%doc README
%{_libdir}/*.so.*

%files devel
%{_bindir}/*
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Oct 29 2015 Richard Shaw <hobbes1069@gmail.com> - 0.5-1
- Update to latest upstream release.

* Sat Aug  8 2015 Richard Shaw <hobbes1069@gmail.com> - 0.4-2
- Update to latest bugfix release.

* Thu Jul  2 2015 Richard Shaw <hobbes1069@gmail.com> - 0.4-1
- Update to latest upstream release.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-6.20150317svn2080
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 17 2015 Richard Shaw <hobbes1069@gmail.com> - 0.3-5.svn2080
- Update to later checkout.

* Mon Mar 16 2015 Richard Shaw <hobbes1069@gmail.com> - 0.3-4.svn1914
- Fixup spec file per review request comments.

* Sun Jul 27 2014 Richard Shaw <hobbes1069@gmail.com> - 0.3-2.svn1771
- Fix executable permissions on scripts.
- Move example package to devel-examples.
- Move binaries to devel package as they are not useful elsewere.
- Fix package name to include svn checkout date.

* Mon Jun 16 2014 Richard Shaw <hobbes1069@gmail.com> - 0.3-1.svn1657
- Updated for ABI incompatible change in freedv.

* Mon Jun 16 2014 Richard Shaw <hobbes1069@gmail.com> - 0.2-9
- Update to newer svn checkout.

* Mon May  5 2014 Richard Shaw <hobbes1069@gmail.com> - 0.2-8
- Update to newer checkout.

* Fri Mar 28 2014 Richard Shaw <hobbes1069@gmail.com> - 0.2-6
- Update to newer checkout.

* Wed Mar 27 2013 Richard Shaw <hobbes1069@gmail.com> - 0.2.0-5
- Make the package more Fedora compliant.
- Add patch to make sure fdmdv.h is installed.
- Strip rpath from binaries.
- Create pkgconfig file to deal with non-standard header location.
- Move examples to a separate sub-package.

* Sun Dec 30 2012 Mike Heitmann <mheitmann@n0so.net> 0.2.0-2
- Fixed ldconfig path error

* Sun Dec 30 2012 Mike Heitmann <mheitmann@n0so.net> 0.2.0-1
- Fixed ldconfig errors, corrected version number

* Sun Dec 23 2012 Mike Heitmann <mheitmann@n0so.net> 0.0.1-1
- Initial SPEC
- Split out from FreeDV to compile separately
