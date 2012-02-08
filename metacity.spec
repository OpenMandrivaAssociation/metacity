%define _disable_ld_no_undefined 1

%define lib_major 0
%define libname %mklibname %{name}-private %{lib_major}
%define develname %mklibname -d %{name}-private

Summary: Metacity window manager
Name: metacity
Version: 2.34.2
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
BuildRequires: gsettings-desktop-schemas-devel >= 3.3.0
BuildRequires: startup-notification-devel
BuildRequires: intltool gnome-doc-utils
BuildRequires: zenity
BuildRequires: gnome-common
BuildRequires: pkgconfig(pangoxft)

Requires: zenity

%description
Metacity is a simple window manager that integrates nicely with 
GNOME 2.

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
rm -rf %{buildroot} %name.lang
%makeinstall_std

%find_lang %{name} 


%files -f %{name}.lang
%doc README COPYING NEWS HACKING 
%{_bindir}/*
%{_datadir}/gnome-control-center/keybindings/50-metacity*.xml
%{_datadir}/applications/metacity.desktop
%{_datadir}/gnome/wm-properties/metacity-wm.desktop
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/metacity
%dir %_datadir/gnome/help/creating-metacity-themes
%_datadir/gnome/help/creating-metacity-themes/C
%lang(de) %_datadir/gnome/help/creating-metacity-themes/de
%{_datadir}/themes/*
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/*.so.%{lib_major}*

%files -n %{develname}
%doc ChangeLog
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

