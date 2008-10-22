%define lib_major 0
%define libname %mklibname %{name}-private %{lib_major}
%define libnamedev %mklibname -d %{name}-private
%define startup_notification_version 0.4

Summary: Metacity window manager
Name: metacity
Version: 2.25.2
Release: %mkrel 1
URL: http://ftp.gnome.org/pub/gnome/sources/metacity/
Source0: http://ftp.gnome.org/pub/GNOME/sources/metacity/%{name}-%{version}.tar.bz2
Patch0: metacity-2.25.2-missing.patch
Patch1: metacity-2.25.2-fix-linking.patch
# (fc) 2.3.987-2mdk use Ia Ora as default theme
Patch2: metacity-2.25.2-defaulttheme.patch
# (fc) 2.21.3-2mdv enable compositor by default
Patch4: metacity-enable-compositor.patch
# (fc) 2.23.144-2mdv don't move window across workspace when raising (Mdv bug #25009) (GNOME bug #482354)
Patch5: metacity-2.21.13-dont-move-windows.patch
License: GPLv2+
Group: Graphical desktop/GNOME
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libglade2.0-devel
BuildRequires: libGConf2-devel >= 1.1.9
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: libxinerama-devel
BuildRequires: libxcomposite-devel
BuildRequires: libxdamage-devel
BuildRequires: libxtst-devel
BuildRequires: libmesaglu-devel
BuildRequires: GConf2
BuildRequires: intltool

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
%patch -p1
%patch1 -p1
%patch2 -p1 -b .defaulttheme
# don't enable compositor by default, too many drivers are buggy currently
#%patch4 -p1 -b .enable-compositor
%patch5 -p1 -b .dont-move-windows
#gw patch1:
aclocal
autoconf
automake

%build

%configure2_5x 
%make

%install
rm -rf $RPM_BUILD_ROOT
GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas metacity

# update default window theme on distribution upgrade
%triggerpostun -- metacity < 2.23.144-3mdv
  %{_bindir}/gconftool-2 --config-source=xml::/etc/gconf/gconf.xml.local-defaults/ --direct --unset /apps/metacity/general/theme > /dev/null

%if %mdkversion < 200900
%post
%post_install_gconf_schemas %{schemas}
%endif

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
%{_libexecdir}/metacity-dialog
%{_datadir}/gnome-control-center/keybindings/50-metacity*.xml
%{_datadir}/applications/metacity.desktop
%{_datadir}/gnome/wm-properties/metacity-wm.desktop
%{_datadir}/metacity
%dir %_datadir/gnome/help/creating_metacity_themes
%_datadir/gnome/help/creating_metacity_themes/C
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
