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


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DDATA_INSTALL_DIR=%{tde_prefix}/share/apps
BuildOption:    -DMIME_INSTALL_DIR=%{tde_prefix}/share/mimelnk
BuildOption:    -DXDG_APPS_INSTALL_DIR=%{tde_prefix}/share/applications/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DDOC_INSTALL_DIR=%{tde_prefix}/share/doc/tde
BuildOption:    -DUSE_STRIGI=OFF
BuildOption:    -DUSE_MENUDRAKE=OFF
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

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
  -e "s|/usr/bin/uic-tqt|%{tde_prefix}/bin/uic-tqt|" \
  -e "s|/usr/bin/tmoc|%{tde_prefix}/bin/tmoc|" \
  -e "s|/usr/include/tqt||"
  
%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%files
%defattr(-,root,root,-)
%{tde_prefix}/bin/kbfxconfigapp
%{tde_prefix}/include/tde/kbfx/
%dir %{tde_prefix}/%{_lib}/kbfx
%dir %{tde_prefix}/%{_lib}/kbfx/plugins
%{tde_prefix}/%{_lib}/kbfx/plugins/libkbfxplasmadataplasmoid.la
%{tde_prefix}/%{_lib}/kbfx/plugins/libkbfxplasmadataplasmoid.so
%{tde_prefix}/%{_lib}/kbfx/plugins/libkbfxplasmadatasettings.la
%{tde_prefix}/%{_lib}/kbfx/plugins/libkbfxplasmadatasettings.so
%{tde_prefix}/%{_lib}/kbfx/plugins/libkbfxplasmadatastub.la
%{tde_prefix}/%{_lib}/kbfx/plugins/libkbfxplasmadatastub.so
%{tde_prefix}/%{_lib}/kbfx/plugins/libkbfxplasmarecentstuff.la
%{tde_prefix}/%{_lib}/kbfx/plugins/libkbfxplasmarecentstuff.so
%{tde_prefix}/%{_lib}/libkbfxcommon.la
%{tde_prefix}/%{_lib}/libkbfxcommon.so
%{tde_prefix}/%{_lib}/libkbfxdata.la
%{tde_prefix}/%{_lib}/libkbfxdata.so
%{tde_prefix}/%{_lib}/trinity/kbfxspinx.la
%{tde_prefix}/%{_lib}/trinity/kbfxspinx.so
%{tde_prefix}/share/applications/tde/kbfx_theme.desktop
%{tde_prefix}/share/applications/tde/kbfxconfigapp.desktop
%{tde_prefix}/share/apps/kbfx/
%dir %{tde_prefix}/share/apps/kbfxconfigapp
%{tde_prefix}/share/apps/kbfxconfigapp/kbfxconfigappui.rc
%{tde_prefix}/share/apps/kicker/applets/kbfxspinx.desktop
%{tde_prefix}/share/apps/konqueror/servicemenus/kbfx_install_theme.desktop
%{tde_prefix}/share/apps/konqueror/servicemenus/kbfx_prepare_theme.desktop
%{tde_prefix}/share/doc/tde/HTML/en/kbfxconfigapp/
%{tde_prefix}/share/doc/kbfx/
%{tde_prefix}/share/icons/hicolor/*/apps/kbfx.png
%{tde_prefix}/share/icons/hicolor/*/apps/kbfxconfigapp.png
%lang(bg) %{tde_prefix}/share/locale/bg/LC_MESSAGES/kbfxconfigapp.mo
%lang(de) %{tde_prefix}/share/locale/de/LC_MESSAGES/kbfxconfigapp.mo
%lang(hu) %{tde_prefix}/share/locale/hu/LC_MESSAGES/kbfxconfigapp.mo
%lang(it) %{tde_prefix}/share/locale/it/LC_MESSAGES/kbfxconfigapp.mo
%lang(nl) %{tde_prefix}/share/locale/nl/LC_MESSAGES/kbfxconfigapp.mo
%lang(ru) %{tde_prefix}/share/locale/ru/LC_MESSAGES/kbfxconfigapp.mo
%lang(zh_Hans) %{tde_prefix}/share//locale/zh_Hans/LC_MESSAGES/kbfxconfigapp.mo
%{tde_prefix}/share/mimelnk/application/x-kbfxtheme.desktop

