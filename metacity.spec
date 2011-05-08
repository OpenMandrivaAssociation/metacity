%define lib_major 0
%define libname %mklibname %{name}-private %{lib_major}
%define libnamedev %mklibname -d %{name}-private
%define startup_notification_version 0.4

Summary: Metacity window manager
Name: metacity
Version: 2.34.0
Release: %mkrel 3
URL: http://ftp.gnome.org/pub/gnome/sources/metacity/
Source0: http://ftp.gnome.org/pub/GNOME/sources/metacity/%{name}-%{version}.tar.bz2
Patch0: metacity-2.34.0-link.patch
# (fwang) 2.34.0 use QtCurve as default theme
Patch2: metacity-2.34.0-defaulttheme.patch
# (fc) 2.21.3-2mdv enable compositor by default
Patch4: metacity-enable-compositor.patch
Patch5: metacity_low_resources.patch
# (fc) 2.30.1-2mdv ensure text is local encoded for Zenity (GNOME bug #617536)
Patch8: metacity-2.30.1-local-encoding-for-zenity.patch
License: GPLv2+
Group: Graphical desktop/GNOME
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: zenity
BuildRequires: libice-devel
BuildRequires: libsm-devel
BuildRequires: libx11-devel
BuildRequires: libxcomposite-devel
BuildRequires: libxcursor-devel
BuildRequires: libxdamage-devel
BuildRequires: libxext-devel
BuildRequires: libxfixes-devel
BuildRequires: libxinerama-devel
BuildRequires: libxrandr-devel
BuildRequires: libxrender-devel
BuildRequires: libcanberra-gtk-devel
BuildRequires: libGConf2-devel
BuildRequires: GConf2
BuildRequires: gtk+2-devel
BuildRequires: libgtop2.0-devel
BuildRequires: startup-notification-devel
BuildRequires: intltool gnome-doc-utils
BuildRequires: zenity
BuildRequires: gnome-common

%description
Metacity is a simple window manager that integrates nicely with 
GNOME 2.

%package -n %{libname}
Summary:        Libraries for Metacity
Group:          System/Libraries

%description -n %{libname}
This package contains libraries used by Metacity.

%package -n %{libnamedev}
Summary:        Libraries and include files with Metacity
Group:          Development/GNOME and GTK+
Requires:       %name = %{version}
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-private-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name}-private 0

%description -n %{libnamedev}
This package provides the necessary development libraries and include 
files to allow you to develop with Metacity.


%prep
%setup -q
%patch0 -p1 -b .link
%patch2 -p1 -b .defaulttheme
# don't enable compositor by default, too many drivers are buggy currently
#%patch4 -p1 -b .enable-compositor
%ifarch %mips
%patch5 -p1 -b .lowres
%endif
%patch8 -p1 -b .local-encoding

%build
NOCONFIGURE=yes gnome-autogen.sh
%configure2_5x --with-gtk=2.0 --disable-schemas-install --disable-scrollkeeper
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std

%find_lang %{name} 

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas metacity

# update default window theme on distribution upgrade
%triggerpostun -- metacity < 2.34.0
%{_bindir}/gconftool-2 --config-source=xml::/etc/gconf/gconf.xml.local-defaults/ --direct --type=string --set /apps/metacity/general/theme "Clearlooks" > /dev/null

%post
%{_bindir}/gconftool-2 --config-source=xml::/etc/gconf/gconf.xml.local-defaults/ --direct --type=string --set /apps/metacity/general/theme "Clearlooks" > /dev/null

%preun
%preun_uninstall_gconf_schemas %{schemas}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README COPYING NEWS HACKING 
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/gnome-control-center/keybindings/50-metacity*.xml
%{_datadir}/applications/metacity.desktop
%{_datadir}/gnome/wm-properties/metacity-wm.desktop
%{_datadir}/metacity
%dir %_datadir/gnome/help/creating-metacity-themes
%_datadir/gnome/help/creating-metacity-themes/C
%lang(de) %_datadir/gnome/help/creating-metacity-themes/de
%{_datadir}/themes/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{lib_major}*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc ChangeLog
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/*
