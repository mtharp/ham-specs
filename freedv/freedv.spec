#global svnrev 2167

%{!?_iconsbasedir: %global _iconsbasedir %{_datadir}/icons/hicolor}

Name:           freedv
Version:        1.0
Release:        1%{?dist}
Summary:        FreeDV Digital Voice
License:        GPLv2+

URL:            http://freedv.org

# svn co https://svn.code.sf.net/p/freetel/code/ freetel
# cd freetel; svn export fdmdv2
Source0:        freedv-%{version}%{?svnrev:.svn%{svnrev}}.tar.gz

BuildRequires:  cmake
BuildRequires:  wxGTK3-devel
BuildRequires:  codec2-devel
BuildRequires:  desktop-file-utils 
BuildRequires:  portaudio-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  speex-devel
BuildRequires:  hamlib-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libao-devel
BuildRequires:  gsm-devel
# For codec2 checkout
BuildRequires:  subversion

#BuildRequires:  sox-devel


%description
FreeDV is a GUI application for Windows and Linux that allows any SSB radio to
be used for low bit rate digital voice.

Speech is compressed down to 1400 bit/s then modulated onto a 1100 Hz wide QPSK
signal which is sent to the Mic input of a SSB radio. On receive, the signal is
received by the SSB radio, then demodulated and decoded by FreeDV.

FreeDV was built by an international team of Radio Amateurs working together on
coding, design, user interface and testing. FreeDV is open source software,
released under the GNU Public License version 2.1. The FDMDV modem and Codec 2
Speech codec used in FreeDV are also open source.


%prep
%setup -q -n freedv-%{version}%{?svnrev:.svn%{svnrev}}


%build
rm -rf build_linux && mkdir build_linux && pushd build_linux
export LDFLAGS="-Wl,--as-needed"
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DWXCONFIG="%{_bindir}/wx-config-3.0" \
       -DWXRC="%{_bindir}/wxrc-3.0" \
       -DUSE_STATIC_SOX=TRUE \
       -DUSE_STATIC_CODEC2=TRUE \
       ../

make %{?_smp_mflags}


%install
pushd build_linux
%make_install

# Install desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc credits.txt README.txt
%if 0%{?rhel} < 7 || 0%{?fedora} < 21
%doc COPYING
%else
%license COPYING
%endif
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsbasedir}/*/apps/%{name}.png


%changelog
* Tue Aug 25 2015 Richard Shaw <hobbes1069@gmail.com> - 1.0-1
- Update to latest upstream release.

* Sat Jul  4 2015 Richard Shaw <hobbes1069@gmail.com> - 0.98.0-1
- Update to latest upstream release.

* Sun May 31 2015 Richard Shaw <hobbes1069@gmail.com> - 0.97.0-3
- Update to latest svn checkout.

* Tue Jun 17 2014 Richard Shaw <hobbes1069@gmail.com> - 0.97.0-1
- Update to latest upstream release.

* Sat May 24 2014 Richard Shaw <hobbes1069@gmail.com> - 0.96.7-1
- Latest release.

* Fri Mar 28 2014 Richard Shaw <hobbes1069@gmail.com> - 0.96.5-5
- Update to later svn checkout, 1481.

* Sun Mar 23 2014 Richard Shaw <hobbes1069@gmail.com> - 0.96.5-4
- Try test build with patch to remove libctb dependence.

* Sun Sep 15 2013 Richard Shaw <hobbes1069@gmail.com> - 0.96.5-3
- Update to latest checkout.

* Fri Apr 12 2013 Richard Shaw <hobbes1069@gmail.com> - 0.96-1
- Updated to lastest svn checkout (rev 1231).
- Updated spec to meet Fedora Packaging Guidelines.
- Created new icon and desktop files
- Implemented cmake based build configuration.

* Sun Dec 23 2012 Mike Heitmann <mheitmann@n0so.net> 0.91-3
- Made libctb, wxWidgets, codec2 separate rpm packages

* Sat Dec 22 2012 Mike Heitmann <mheitmann@n0so.net> 0.91-2
- Updated spec to use %{_libdir} and %{_bindir} macros

* Sun Dec 16 2012 Mike Heitmann <mheitmann@n0so.net> 0.91-1
- Initial SPEC

