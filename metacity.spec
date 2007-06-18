%define lib_major 0
%define lib_name %mklibname %{name}-private %{lib_major}
%define startup_notification_version 0.4

%define libcm_version 0.1.1

Summary: Metacity window manager
Name: metacity
Version: 2.19.21
Release: %mkrel 1
URL: http://ftp.gnome.org/pub/gnome/sources/metacity/
Source0: http://ftp.gnome.org/pub/GNOME/sources/metacity/%{name}-%{version}.tar.bz2
Source1: Wonderland-metacity-0.47.tar.bz2
Source2: http://download.gnome.org/sources/libcm/libcm-%{libcm_version}.tar.bz2
# (fc) 2.3.987-2mdk use Ia Ora as default theme
Patch2: metacity-2.15.21-defaulttheme.patch
# (fc) 2.15.3-1mdv build with static libcm (Fedora)
Patch3: metacity-2.15.3-static-cm.patch

License: GPL
Group: Graphical desktop/GNOME
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libglade2.0-devel
BuildRequires: libGConf2-devel >= 1.1.9
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: libxcomposite-devel
BuildRequires: libxdamage-devel
BuildRequires: libxtst-devel
BuildRequires: libmesaglu-devel
#gw for the broken intltool scripts
BuildRequires: perl-XML-Parser
BuildRequires: GConf2
BuildRequires: intltool

%description
Metacity is a simple window manager that integrates nicely with 
GNOME 2.

%package -n %{lib_name}
Summary:        Libraries for Metacity
Group:          System/Libraries

%description -n %{lib_name}
This package contains libraries used by Metacity.

%package -n %{lib_name}-devel
Summary:        Libraries and include files with Metacity
Group:          Development/GNOME and GTK+
Requires:       %name = %{version}
Requires:		%{lib_name} = %{version}
Provides:		%{name}-devel = %{version}-%{release}
Provides:		lib%{name}-private-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package provides the necessary development libraries and include 
files to allow you to develop with Metacity.


%prep
%setup -q
%setup -q -D -T -a2
%patch2 -p1 -b .defaulttheme
%patch3 -p1 -b .static-cm

#needed by patch3
aclocal
autoconf
automake -a -c

%build

cd libcm-%{libcm_version}
%configure2_5x
%make
make install DESTDIR="$PWD/prefix"
cd ..

LIBS="$LIBS -lGL -lGLU"
LIBS="$LIBS -lICE -lSM"
LIBS="$LIBS -lX11 -lXext -lXinerama -lXrandr"
LIBS="$LIBS -lXrender -lXcursor"
LIBS="$LIBS -lXdamage -lXtst -lXfixes -lXcomposite"
%ifnarch s390 s390x ppc64
LIBS="$LIBS $PWD/libcm-%{libcm_version}/prefix/%{_libdir}/libcm.a"
%endif
export LIBS

CPPFLAGS="-I$PWD/libcm-%{libcm_version}/prefix/%{_includedir}"
export CPPFLAGS


%configure2_5x --enable-compositor
%make 

%install
rm -rf $RPM_BUILD_ROOT

GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 %makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_datadir}/themes/Wonderland/metacity-1
tar -xjf %{SOURCE1} -C $RPM_BUILD_ROOT%{_datadir}/themes/Wonderland/metacity-1

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas metacity

%post
if [ ! -d %{_sysconfdir}/gconf/gconf.xml.local-defaults/apps/metacity/general -a "x$META_CLASS" != "x" ]; then
 case "$META_CLASS" in
  *server) METACITY_THEME="Ia Ora Gray" ;;
  *desktop) METACITY_THEME="Ia Ora Orange" ;;
  *download) METACITY_THEME="Ia Ora Free";;
 esac

  if [ "x$METACITY_THEME" != "x" ]; then 
  %{_bindir}/gconftool-2 --config-source=xml::/etc/gconf/gconf.xml.local-defaults/ --direct --type=string --set /apps/metacity/general/theme "$METACITY_THEME" > /dev/null
  fi
fi
%post_install_gconf_schemas %{schemas}

%preun
%preun_uninstall_gconf_schemas %{schemas}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc README COPYING NEWS HACKING 
%{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_libexecdir}/metacity-dialog
%{_datadir}/control-center/keybindings/50-metacity*.xml
%{_datadir}/gnome/wm-properties/*
%{_datadir}/metacity
%{_datadir}/themes/*
%{_mandir}/man1/*

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc ChangeLog
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*
%{_libdir}/pkgconfig/*
