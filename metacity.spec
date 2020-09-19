%define url_ver %(echo %{version}|cut -d. -f1,2)
%define _disable_ld_no_undefined 1

%define major	1
%define libname %mklibname %{name}-private %{major}
%define devname %mklibname -d %{name}-private

Summary:	Metacity window manager
Name:		metacity
Version:	3.37.1
Release:	1
License:	GPLv2+
Group:		Graphical desktop/GNOME
Url:		http://ftp.gnome.org/pub/gnome/sources/metacity/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/metacity/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	gnome-common
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	yelp-tools
BuildRequires:	zenity
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gsettings-desktop-schemas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libcanberra-gtk3)
BuildRequires:	pkgconfig(libgtop-2.0)
BuildRequires:	pkgconfig(libstartup-notification-1.0)
BuildRequires:	pkgconfig(pangoxft)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)
BuildRequires:  pkgconfig(xres)

Requires:	zenity

%description
Metacity is a simple window manager that integrates nicely with
GNOME.

%package -n %{libname}
Summary:	Libraries for Metacity
Group:		System/Libraries

%description -n %{libname}
This package contains libraries used by Metacity.

%package -n %{devname}
Summary:	Libraries and include files with Metacity
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package provides the necessary development libraries and include
files to allow you to develop with Metacity.

%prep
%setup -q

%build
%configure --disable-static \
               --disable-schemas-compile

%make_build

%install
%make_install

%find_lang %{name} --with-gnome --all-name

%files -f %{name}.lang
%doc README COPYING NEWS HACKING
%{_bindir}/*
%{_datadir}/applications/metacity.desktop
#{_datadir}/GConf/gsettings/metacity-schemas.convert
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/gnome-control-center/keybindings/50-metacity*.xml
#{_datadir}/gnome/wm-properties/metacity-wm.desktop
%{_datadir}/metacity
#{_datadir}/themes/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%doc ChangeLog
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

