%define lib_major 0
%define libname %mklibname %{name}-private %{lib_major}
%define libnamedev %mklibname -d %{name}-private
%define startup_notification_version 0.4

Summary: Metacity window manager
Name: metacity
Version: 2.27.0
Release: %mkrel 1
URL: http://ftp.gnome.org/pub/gnome/sources/metacity/
Source0: http://ftp.gnome.org/pub/GNOME/sources/metacity/%{name}-%{version}.tar.bz2
#gw http://bugzilla.gnome.org/show_bug.cgi?id=562106
Patch0: metacity-2.25.55-disable-werror.patch
# (fc) 2.3.987-2mdk use Ia Ora as default theme
Patch2: metacity-2.25.2-defaulttheme.patch
# (fc) 2.21.3-2mdv enable compositor by default
Patch4: metacity-enable-compositor.patch
License: GPLv2+
Group: Graphical desktop/GNOME
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: zenity
BuildRequires: libglade2.0-devel
BuildRequires: libGConf2-devel >= 1.1.9
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: libcanberra-devel
BuildRequires: libgtop2.0-devel
BuildRequires: libxinerama-devel
BuildRequires: libxcomposite-devel
BuildRequires: libxdamage-devel
BuildRequires: libxtst-devel
BuildRequires: libmesaglu-devel
BuildRequires: GConf2
BuildRequires: zenity
BuildRequires: intltool
BuildRequires: gnome-doc-utils
BuildRequires: libcanberra-devel
#gw libtool dep:
BuildRequires: dbus-glib-devel


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
Requires:		%{libname} = %{version}
Provides:		%{name}-devel = %{version}-%{release}
Provides:		lib%{name}-private-devel = %{version}-%{release}
Obsoletes: %mklibname -d %{name}-private 0

%description -n %{libnamedev}
This package provides the necessary development libraries and include 
files to allow you to develop with Metacity.


%prep
%setup -q
%patch0 -p1 -b .werror
%patch2 -p1 -b .defaulttheme
# don't enable compositor by default, too many drivers are buggy currently
#%patch4 -p1 -b .enable-compositor

#needed by patch 0
autoconf

%build

%configure2_5x 
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%find_lang %{name} 

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas metacity

# update default window theme on distribution upgrade
%triggerpostun -- metacity < 2.26.0-3mdv
if [ "x$META_CLASS" != "x" ]; then
 case "$META_CLASS" in
  *server) METACITY_THEME="Ia Ora Gray" ;;
  *desktop) METACITY_THEME="Ia Ora Arctic" ;;
  *download) METACITY_THEME="Ia Ora Blue";;
 esac

  if [ "x$METACITY_THEME" != "x" ]; then
  %{_bindir}/gconftool-2 --config-source=xml::/etc/gconf/gconf.xml.local-defaults/ --direct --type=string --set /apps/metacity/general/theme "$METACITY_THEME" > /dev/null
  fi
fi

%post
%if %mdkversion < 200900
%post_install_gconf_schemas %{schemas}
%endif
if [ ! -d %{_sysconfdir}/gconf/gconf.xml.local-defaults/apps/metacity/general -a "x$META_CLASS" != "x" ]; then
 case "$META_CLASS" in
  *server) METACITY_THEME="Ia Ora Gray" ;;
  *desktop) METACITY_THEME="Ia Ora Arctic" ;;
  *download) METACITY_THEME="Ia Ora Blue";;
 esac

  if [ "x$METACITY_THEME" != "x" ]; then 
  %{_bindir}/gconftool-2 --config-source=xml::/etc/gconf/gconf.xml.local-defaults/ --direct --type=string --set /apps/metacity/general/theme "$METACITY_THEME" > /dev/null
  fi
fi


%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

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
