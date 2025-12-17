%bcond clang 1
%bcond gamin 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kbfx
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		0.4.9.3.1
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:		An alternative to K-Menu for TDE
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DCMAKE_SKIP_INSTALL_RPATH=OFF
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_RPATH="%{tde_libdir}"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir}
BuildOption:    -DDATA_INSTALL_DIR=%{tde_datadir}/apps
BuildOption:    -DMIME_INSTALL_DIR=%{tde_datadir}/mimelnk
BuildOption:    -DXDG_APPS_INSTALL_DIR=%{tde_tdeappdir}
BuildOption:    -DSHARE_INSTALL_PREFIX="%{tde_datadir}"
BuildOption:    -DDOC_INSTALL_DIR=%{tde_tdedocdir}
BuildOption:    -DLIB_INSTALL_DIR=%{tde_libdir}
BuildOption:    -DUSE_STRIGI=OFF
BuildOption:    -DUSE_MENUDRAKE=OFF
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_ALL=ON

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires: libtool

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig

# IDN support
BuildRequires:	pkgconfig(libidn)

# GAMIN support
%{?with_gamin:BuildRequires:	pkgconfig(gamin)}

# PCRE2 support
BuildRequires:  pkgconfig(libpcre2-posix)

# ACL support
BuildRequires:  pkgconfig(libacl)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
KBFX is an alternative to the classical K-Menu button and its menu.
It improves the user experience by enabling him to set a bigger (and thus more
visible) start button and by finally replacing the Win95-like K-Menu.
If you still want the old menu, because you're used to it, it is still
available as an option in kbfx. We recommend, however, that you give the Spinx
bar a try.

Homepage: http://www.kbfx.org


%prep -a
# Fix TDE executable path in 'CMakeLists.txt' ...
%__sed -i "CMakeLists.txt" \
  -e "s|/usr/bin/uic-tqt|%{tde_bindir}/uic-tqt|" \
  -e "s|/usr/bin/tmoc|%{tde_bindir}/tmoc|" \
  -e "s|/usr/include/tqt||"
  
%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"


%files
%defattr(-,root,root,-)
%{tde_bindir}/kbfxconfigapp
%{tde_tdeincludedir}/kbfx/
%dir %{tde_libdir}/kbfx
%dir %{tde_libdir}/kbfx/plugins
%{tde_libdir}/kbfx/plugins/libkbfxplasmadataplasmoid.la
%{tde_libdir}/kbfx/plugins/libkbfxplasmadataplasmoid.so
%{tde_libdir}/kbfx/plugins/libkbfxplasmadatasettings.la
%{tde_libdir}/kbfx/plugins/libkbfxplasmadatasettings.so
%{tde_libdir}/kbfx/plugins/libkbfxplasmadatastub.la
%{tde_libdir}/kbfx/plugins/libkbfxplasmadatastub.so
%{tde_libdir}/kbfx/plugins/libkbfxplasmarecentstuff.la
%{tde_libdir}/kbfx/plugins/libkbfxplasmarecentstuff.so
%{tde_libdir}/libkbfxcommon.la
%{tde_libdir}/libkbfxcommon.so
%{tde_libdir}/libkbfxdata.la
%{tde_libdir}/libkbfxdata.so
%{tde_tdelibdir}/kbfxspinx.la
%{tde_tdelibdir}/kbfxspinx.so
%{tde_tdeappdir}/kbfx_theme.desktop
%{tde_tdeappdir}/kbfxconfigapp.desktop
%{tde_datadir}/apps/kbfx/
%dir %{tde_datadir}/apps/kbfxconfigapp
%{tde_datadir}/apps/kbfxconfigapp/kbfxconfigappui.rc
%{tde_datadir}/apps/kicker/applets/kbfxspinx.desktop
%{tde_datadir}/apps/konqueror/servicemenus/kbfx_install_theme.desktop
%{tde_datadir}/apps/konqueror/servicemenus/kbfx_prepare_theme.desktop
%{tde_tdedocdir}/HTML/en/kbfxconfigapp/
%{tde_docdir}/kbfx/
%{tde_datadir}/icons/hicolor/*/apps/kbfx.png
%{tde_datadir}/icons/hicolor/*/apps/kbfxconfigapp.png
%lang(bg) %{tde_datadir}/locale/bg/LC_MESSAGES/kbfxconfigapp.mo
%lang(de) %{tde_datadir}/locale/de/LC_MESSAGES/kbfxconfigapp.mo
%lang(hu) %{tde_datadir}/locale/hu/LC_MESSAGES/kbfxconfigapp.mo
%lang(it) %{tde_datadir}/locale/it/LC_MESSAGES/kbfxconfigapp.mo
%lang(nl) %{tde_datadir}/locale/nl/LC_MESSAGES/kbfxconfigapp.mo
%lang(ru) %{tde_datadir}/locale/ru/LC_MESSAGES/kbfxconfigapp.mo
%lang(zh_Hans) %{tde_datadir}//locale/zh_Hans/LC_MESSAGES/kbfxconfigapp.mo
%{tde_datadir}/mimelnk/application/x-kbfxtheme.desktop

