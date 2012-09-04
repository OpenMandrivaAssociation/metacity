%define _disable_ld_no_undefined 1

%define major 0
%define libname %mklibname %{name}-private %{major}
%define develname %mklibname -d %{name}-private

Summary: Metacity window manager
Name: metacity
Version: 2.34.8
Release: 1
License: GPLv2+
Group: Graphical desktop/GNOME
URL: http://ftp.gnome.org/pub/gnome/sources/metacity/
Source0: http://ftp.gnome.org/pub/GNOME/sources/metacity/%{name}-%{version}.tar.xz
Patch0: metacity-2.34.0-link.patch
# (fc) 2.21.3-2mdv enable compositor by default
Patch4: metacity-enable-compositor.patch
Patch5: metacity_low_resources.patch
# (fc) 2.30.1-2mdv ensure text is local encoded for Zenity (GNOME bug #617536)
Patch8: metacity-2.30.1-local-encoding-for-zenity.patch

BuildRequires: GConf2
BuildRequires: gnome-common
BuildRequires: intltool
BuildRequires: zenity
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires: pkgconfig(gnome-doc-utils)
BuildRequires: pkgconfig(gsettings-desktop-schemas)
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(ice)
BuildRequires: pkgconfig(libcanberra-gtk)
BuildRequires: pkgconfig(libgtop-2.0)
BuildRequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(pangoxft)
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xinerama)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xrender)

Requires: zenity

%description
Metacity is a simple window manager that integrates nicely with 
GNOME. 

%package -n %{libname}
Summary:	Libraries for Metacity
Group:		System/Libraries

%description -n %{libname}
This package contains libraries used by Metacity.

%package -n %{develname}
Summary:	Libraries and include files with Metacity
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname -d %{name}-private 0

%description -n %{develname}
This package provides the necessary development libraries and include 
files to allow you to develop with Metacity.

%prep
%setup -q
%patch0 -p1 -b .link
# don't enable compositor by default, too many drivers are buggy currently
#%patch4 -p1 -b .enable-compositor
%ifarch %mips
%patch5 -p1 -b .lowres
%endif
%patch8 -p1 -b .local-encoding

%build
NOCONFIGURE=yes gnome-autogen.sh
%configure \
	--disable-static \
	--disable-scrollkeeper

%make

%install
%makeinstall_std

%find_lang %{name} 

%files -f %{name}.lang
%doc README COPYING NEWS HACKING 
%{_bindir}/*
%{_datadir}/applications/metacity.desktop
%{_datadir}/GConf/gsettings/metacity-schemas.convert
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/gnome-control-center/keybindings/50-metacity*.xml
%{_datadir}/gnome/wm-properties/metacity-wm.desktop
%{_datadir}/metacity
%dir %_datadir/gnome/help/creating-metacity-themes
%_datadir/gnome/help/creating-metacity-themes/C
%lang(de) %_datadir/gnome/help/creating-metacity-themes/de
%{_datadir}/themes/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%doc ChangeLog
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

