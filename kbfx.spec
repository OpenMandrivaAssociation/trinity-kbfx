#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
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

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		0.4.9.3.1
Release:		%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:		An alternative to K-Menu for TDE
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires: libtool
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# IDN support
BuildRequires:	pkgconfig(libidn)

# GAMIN support
#  Not on openSUSE.
%if 0%{!?suse_version}
%define with_gamin 1
BuildRequires:	pkgconfig(gamin)
%endif

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


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

# Fix TDE executable path in 'CMakeLists.txt' ...
%__sed -i "CMakeLists.txt" \
  -e "s|/usr/bin/uic-tqt|%{tde_bindir}/uic-tqt|" \
  -e "s|/usr/bin/tmoc|%{tde_bindir}/tmoc|" \
  -e "s|/usr/include/tqt||"
  
%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

# Shitty hack for RHEL4 ...
if [ -d "/usr/X11R6" ]; then
  export CMAKE_INCLUDE_PATH="${CMAKE_INCLUDE_PATH}:/usr/X11R6/include:/usr/X11R6/%{_lib}"
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX=%{tde_prefix} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DDATA_INSTALL_DIR=%{tde_datadir}/apps \
  -DMIME_INSTALL_DIR=%{tde_datadir}/mimelnk \
  -DXDG_APPS_INSTALL_DIR=%{tde_tdeappdir} \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}"\
  -DDOC_INSTALL_DIR=%{tde_tdedocdir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  \
  -DUSE_STRIGI=OFF \
  -DUSE_MENUDRAKE=OFF \
  -DBUILD_DOC=ON \
  -DBUILD_ALL=ON \
  ..

# Not SMP safe !
%__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build VERBOSE=1

# Updates applications categories for openSUSE
%if 0%{?suse_version}
%suse_update_desktop_file -G "KBFX Configuration Utility" kbfxconfigapp -r KDE Utility DesktopUtility
%suse_update_desktop_file %{buildroot}%{tde_datadir}/apps/konqueror/servicemenus/kbfx_prepare_theme.desktop
%suse_update_desktop_file %{buildroot}%{tde_datadir}/apps/konqueror/servicemenus/kbfx_install_theme.desktop
%suse_update_desktop_file %{buildroot}%{tde_datadir}/apps/kicker/applets/kbfxspinx.desktop
%suse_update_desktop_file %{buildroot}%{tde_datadir}/mimelnk/application/x-kbfxtheme.desktop
%suse_update_desktop_file %{buildroot}%{tde_datadir}/applications/tde/kbfx_theme.desktop
%endif


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

