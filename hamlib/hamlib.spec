%global __provides_exclude_from ^%{_libdir}/hamlib/.*\\.so$

Name:           hamlib
Version:        dummy
Release:        20%{?dist}
Summary:        Run-time library to control radio transceivers and receivers

Group:          System Environment/Libraries
License:        GPLv2+ and LGPLv2+
URL:            http://hamlib.sourceforge.net
Source0:        hamlib-dummy.tar.gz
Patch0:         hamlib-bindings.patch
BuildRequires:  python-devel, swig, gd-devel, libxml2-devel, tcl-devel
BuildRequires:  libusb-devel, pkgconfig, boost-devel, libtool-ltdl-devel
BuildRequires:  doxygen, texinfo
BuildRequires:  autoconf, automake, libtool
#for perl
BuildRequires:  perl(ExtUtils::MakeMaker)


%description
Hamlib provides a standardized programming interface that applications
can use to send the appropriate commands to a radio.

Also included in the package is a simple radio control program 'rigctl',
which lets one control a radio transceiver or receiver, either from
command line interface or in a text-oriented interactive interface.

%package devel
Summary: Development library to control radio transceivers and receivers
Group: Development/Libraries
Requires: hamlib%{?_isa} = %{version}-%{release}

%description devel
Hamlib radio control library C development headers and libraries
for building C applications with Hamlib.

%package doc
Summary: Documentation for the hamlib radio control library
Group: Documentation
BuildArch: noarch

%description doc
This package provides the developers documentation for the hamlib radio
control library API.

%package c++
Summary: Hamlib radio control library C++ binding
Group: Development/Libraries
Requires: hamlib%{?_isa} = %{version}-%{release}

%description c++
Hamlib radio control library C++ language binding.

%package c++-devel
Summary: Hamlib radio control library C++ binding development headers and libraries
Group: Development/Libraries
Requires: hamlib-devel%{?_isa} = %{version}-%{release}
Requires: hamlib-c++%{?_isa} = %{version}-%{release}

%description c++-devel
Hamlib radio control library C++ binding development headers and libraries
for building C++ applications with Hamlib.


%package perl
Summary: Hamlib radio control library Perl binding
Group: Development/Libraries
Requires: hamlib%{?_isa} = %{version}-%{release}

%description perl
Hamlib PERL Language bindings to allow radio control from PERL scripts.

%package python
Summary: Hamlib radio control library Python binding
Group: Development/Libraries
Requires: hamlib%{?_isa} = %{version}-%{release}, python

%description python
Hamlib Python Language bindings to allow radio control from Python scripts.

%package tcl
Summary: Hamlib radio control library TCL binding
Group: Development/Libraries
Requires: hamlib%{?_isa} = %{version}-%{release}

%description tcl
Hamlib TCL Language bindings to allow radio control from TCL scripts.

%prep
%setup -q
%patch0 -p1 -b .bindings

%build
autoreconf -i
%configure \
        --disable-static \
        --enable-html-matrix \
        --with-xml-support \
        --with-tcl-binding \
        --with-perl-binding \
        --with-python-binding \
#	usrp depreciated
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# Build libs, drivers, and programs, won't build with smpflags
make
# Build Documentation
make -C doc doc

%install
make DESTDIR=$RPM_BUILD_ROOT install
#install documentation
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}/html/search
for f in `find doc/html/ -type f -maxdepth 1`
        do install -D -m 0644 $f $RPM_BUILD_ROOT%{_docdir}/%{name}/`echo $f | cut -d '/' -f2`
done
for f in `find doc/html/search -type f -maxdepth 1`
        do install -D -m 0644 $f $RPM_BUILD_ROOT%{_docdir}/%{name}/html/`echo $f | cut -d '/' -f3`
 done
# move installed docs to include them in subpackage via %%doc magic
rm -rf __tmp_doc ; mkdir __tmp_doc
mv ${RPM_BUILD_ROOT}%{_docdir}/%{name}/* __tmp_doc

rm -f $RPM_BUILD_ROOT%{_libdir}/hamlib-*.a $RPM_BUILD_ROOT%{_libdir}/hamlib-*.la

find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;

/sbin/ldconfig -N -n $RPM_BUILDROOT%{_libdir}

#fix permissions
find $RPM_BUILD_ROOT -type f -name Hamlib.so -exec chmod 0755 {} ';'

#remove this, not needed
find $RPM_BUILD_ROOT -type f -name pkgIndex.tcl -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name Hamlib.bs -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name perltest.pl -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_infodir}/dir


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig

%post tcl -p /sbin/ldconfig

%postun tcl -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog PLAN COPYING.LIB COPYING README THANKS TODO
%{_bindir}/*
%{_libdir}/libhamlib.so.*
%{_mandir}/man?/*
%{_infodir}/hamlib.info.gz

%files devel
%doc README.developer
%{_libdir}/libhamlib.so
%{_datadir}/aclocal/hamlib.m4
%dir %{_includedir}/hamlib
%{_includedir}/hamlib/rig.h
%{_includedir}/hamlib/riglist.h
%{_includedir}/hamlib/rig_dll.h
%{_includedir}/hamlib/rotator.h
%{_includedir}/hamlib/rotlist.h
%{_libdir}/pkgconfig/hamlib.pc

%files doc
%doc COPYING.LIB
%doc __tmp_doc/*

%files c++
%{_libdir}/libhamlib++.so.*

%files c++-devel
%{_libdir}/libhamlib++.so
%{_includedir}/hamlib/rigclass.h
%{_includedir}/hamlib/rotclass.h

%files perl
%{perl_vendorarch}/*

%files python
%{python_sitearch}/*.py*
%{python_sitearch}/_Hamlib.so

%files tcl
%{_libdir}/tcl/Hamlib/*

%changelog
* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.2.15.3-20
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15.3-19
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.2.15.3-18
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.15.3-16
- Perl 5.22 rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.2.15.3-15
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 1.2.15.3-14
- Rebuild for boost 1.57.0

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.2.15.3-13
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  1 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.15.3-11
- Moved arch python module to sitearch dir, resolved multilib conflict
  Resolves: rhbz#1030768

* Tue Jun 24 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.15.3-10
- Switched to recent dependency filtering system,
  it should resolve most of the multilib conflicts

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.2.15.3-8
- Rebuild for boost 1.55.0

* Tue May 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.15.3-7
- Rebuilt for tcl/tk8.6

* Sat Dec 14 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2.15.3-6
- Fix duplicate documentation (#1001257)
- License included only in base package, subpackages that depend on
  base package don't need to include it again
- Build noarch HTML -doc subpackage
- Include %%_libdir/hamlib directory
- Drop obsolete spec buildroot definition/removal and %%clean
- Add %%?_isa to explicit package deps
- Remove %%defattr

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 1.2.15.3-4
- Rebuild for boost 1.54.0

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.2.15.3-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.2.15.3-1
- New version
  Resolves: rhbz#846438

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Lucian Langa <cooly@gnome.eu.org> - 1.2.15.1-1
- remove gnuradio dependency as we do not require it
- drop temporary patch
- new upstream release

* Sun Feb 05 2012 Lucian Langa <cooly@gnome.eu.org> - 1.2.15-1
- add temporary patch to fix usrmove issues
- drop patch 1 - no longer building with usrp
- drop patch 2 - fixed upstream
- new upstream release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011 Randall "Randy" Berry <dp67@fedoraproject.org> - 1.2.14-4
- Rebuild to fix broken deps libusrp

* Wed Dec 07 2011 Randall "Randy" Berry <dp67@fedoraproject.org> - 1.2.14-3
- Rebuild to fix broken deps libusrp

* Wed Dec 07 2011 Randall "Randy" Berry <dp67@fedoraproject.org> - 1.2.14-2
- Rebuild to fix broken deps libusrp
- Apply --without-usrp

* Sun Jul 31 2011 Lucian Langa <cooly@gnome.eu.org> - 1.2.14-1
- new upstream release

* Mon Jul 04 2011 Lucian Langa <cooly@gnome.eu.org> - 1.2.13.1-2
- add patch to fix building with latest gnuradio

* Thu Jun 16 2011 Lucian Langa <cooly@gnome.eu.org> - 1.2.13.1-1
- new upstream release

* Sun Apr 24 2011 Lucian Langa <cooly@gnome.eu.org> - 1.2.13-1
- setup filter provides for libdir/hamlib
- update bindings patch
- new upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 2 2011 Randall "Randy" Berry N3LRX <dp67@fedoraproject.org> - 1.2.12-3
- Rebuild to fix broken deps libxml2

* Fri Nov 05 2010 Lucian Langa <cooly@gnome.eu.org> - 1.2.12-2
- update bindings patch
- rebuild against newer libxml2

* Mon Sep 6 2010 Randall "Randy" Berry <dp67@fedoraproject.org> - 1.2.12-1
- New upstream release
- Apply patches to new source
- Removed patch1 applied upstream (usrp.patch)
- Upstream-release-monitoring bz 630702
- Upstream changes:
- New models: PCR-2500, RX331, TRP 8255 S R
- New rotator backends: DF9GR's ERC
- Fixes and features: Paragon, TS-690S, FT-920, FT-990, FT-2000,
- Elektor SDR-USB, IC-7000, IC-7700, AR-8200, AR-8600

* Mon Aug 2 2010 Randall "Randy" Berry <dp67@fedoraproject.org> - 1.2.11-5
- Rebuild

* Mon Aug 2 2010 Randall "Randy" Berry <dp67@fedoraproject.org> - 1.2.11-4
- Build against Python 2.7
- Fix broken dep python2.7

* Sat Jul 31 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.11-3
- Rebuild for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 01 2010 Lucian Langa <cooly@gnome.eu.org> - 1.2.11-1
- update bindings patch
- drop patch2 - fixed upstream
- new upstream release

* Sun May 09 2010 Lucian Langa <cooly@gnome.eu.org> - 1.2.10-4
- description cleanup
- add patch2 - fix double-free in cleanup in dummy module (#587701)

* Sun Nov 08 2009 Lucian Langa <cooly@gnome.eu.org> - 1.2.10-3
- various cleanups
- disable rpath
- rebuild using system libltdl

* Sat Nov 07 2009 Lucian Langa <cooly@gnome.eu.org> - 1.2.10-2
- build with usrp backend

* Sat Nov 07 2009 Lucian Langa <cooly@gnome.eu.org> - 1.2.10-1
- new upstream release

* Sun Aug 23 2009 Lucian Langa <cooly@gnome.eu.org> - 1.2.9-1
- new install rule for docs for new doxygen
- misc cleanups
- patch0 update
- new upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 1.2.8-3
- Add hackish fix for python binding issue

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 1.2.8-1
- New upstream release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2.7-3
- Rebuild for Python 2.6

* Tue Aug 26 2008 Steve Conklin <fedora@conklinhouse.com> - 1.2.7-2
- New patch to fix hamlib-perl

* Fri Feb 15 2008 Steve Conklin <sconklin@redhat.com> - 1.2.7-1
- New upstream released

* Thu Feb 14 2008 Steve Conklin <sconklin@redhat.com> - 1.2.6.2-7
- Rebuild against new gcc4.3

* Thu Jan 03 2008 Alex Lancaster <alexlan[AT]fedoraproject.org> - 1.2.6.2-6
- Rebuild against new Tcl 8.5

* Sun Dec 09 2007 Sindre Pedersen Bjørdal - 1.2.6.2-5
- use sitearch not sitelib for perl package
- Make sure it builds on all arches

* Sat Dec 08 2007 Sindre Pedersen Bjørdal - 1.2.6.2-3
- Clean up BuildRequires
- Remove obsolete swig patch

* Sat Dec 08 2007 Sindre Pedersen Bjørdal - 1.2.6.2-2
- Spec file cleanups
- Use make install instead of depriciated %%makeinstall
- Replace make trickery with patched upstream makefiles
- enable perl bindings
- Patch bindings makefile to install perl to vendor, not site
- Merge swig patch with bindings patch
- enable tcl bindings
- Create doc subpackage, solves #341481
- Remove 2nd bindings patch, not needed as we don't rely on make trickery for bindings anymore
- Add patch to install python bindings in proper python dirs
- Clean up %%files list
- Depend on version-release, not just version

* Tue Sep 25 2007 Denis Leroy <denis@poolshark.org> - 1.2.6.2-1
- Update to new upstream 1.2.6.2
- Added rigsmtr binary

* Mon Sep  3 2007 Denis Leroy <denis@poolshark.org> - 1.2.5-6
- Rebuild, License tag update
- Added net-tools BR

* Wed May  9 2007 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 1.2.5-5
- Move HTML devel documentation to the proper subpackage (#228364)

* Thu Dec 14 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.2.5-4
- Rebuild for new Python

* Sat Sep 30 2006 Dennis Gilmore <dennis@ausil.us> 1.2.5-3
- fix Requires for hamlib-devel  its pkgconfig not pkg-config

* Sat Sep 30 2006 Dennis Gilmore <dennis@ausil.us> 1.2.5-2
- Fix BuildRequires added libxml2-devel, tcl-devel
- libusb-devel, pkgconfig  pkgconfig is required for fc5  as 
- libusb-devel doesnt require it there  but it wont hurt other 
- releases

* Sat Jul 29 2006 Robert 'Bob' Jensen <bob@bobjensen.com> 1.2.5-1
- Upstream update
- Spec file cleanups

* Sun Feb 19 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.4-3
- Fix bindings problems
- Remove static libs
- Remove .la files

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Apr  6 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.4-1
- Upstream update
- Spec file cleanups

* Wed Mar 23 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-9
- Python binding cleanup
- soname/ldconfig cleanup
- Added %%{_includedir}/hamlib to -devel
- Removed %%{_libdir}/hamlib-*.a and hamlib-*.la
- %%doc cleanups

* Wed Mar 23 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-8
- Added -q to %%setup
- Fixed Python binding build and Requires

* Mon Mar 21 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-7
- Removed spurious period and spelling mistake in Summary

* Sat Mar 19 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-6
- %%

* Thu Mar 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-5
- Removed spurious Requires(...)

* Thu Mar 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-4
- Fixed %%post and %%postun along with Requires(...)

* Wed Mar 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-3
- Spell-corrected %%description

* Wed Mar 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-2
- Removed/fixed explicit Requires

* Tue Mar 15 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.3-1
- Bump release to 1
- Fixed BuildRoot

* Thu Feb 10 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:1.2.3-0.iva.1
- Fixed error with automake in -devel (#26)

* Mon Jan 31 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:1.2.3-0.iva.0
- Upstream update

* Sun Jan  9 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:1.2.2-0.iva.1
- Fixed %%files %%defattr

* Sun Jan  9 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:1.2.2-0.iva.0
- Ported to FC3
- Upgraded to 1.2.2

* Sun Apr 18 2004 David L Norris <dave@webaugur.com>
- Enable disabled script bindings.
- Touch up descriptions.

* Tue Jan 20 2004 Tomi Manninen
- Fix for 1.1.5pre2
- Better use of rpm macros
- Disable all bindings

* Wed Oct 08 2003 Joop Stakenborg
- Fix 'make rpm' again by disabling c++ bindings.
- rotclass.h and rigclass.h go into the devel package for now (FIXME)

* Wed Jan 15 2003 Joop Stakenborg
- Fix the spec file for 1.1.4CVS
- 'make rpm' should work now

* Mon Jun 17 2002 Stephane Fillod
- Added rotator support
- Added RPC daemon, hamlib.m4
- Upstream version 1.1.3

* Wed Jul 18 2001 Stephane Fillod
- Made initial "working" SPEC file

