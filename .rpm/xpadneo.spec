Name:       {{{ git_dir_name }}}
# The git_dir_version macro is quite a mis-match for our use-case
# since using a 3-component version number requires updating
# the 'lead' parameter, anyways
# cf. https://pagure.io/rpkg-util/issue/21#comment-601077
Version:    {{{ git_dir_version }}}
#Version:    0.8
Release:    1%{?dist}
Summary:    Advanced Linux Driver for Xbox One Wireless Gamepad
URL:        https://github.com/atar-axis/xpadneo
License:    GPLv3
VCS:        {{{ git_dir_vcs }}}
Source:     {{{ git_dir_pack }}}
BuildArch:  noarch
Requires:   dkms, bluez, bluez-tools
BuildRequires: make, kernel-devel, kernel-headers

%description
This is the first driver for the Xbox One Wireless Gamepad (which is shipped
with the Xbox One S). I wrote it for a student project at fortiss GmbH and it is
fully functional but does only support the connection via Bluetooth as yet -
more will follow.
Many thanks to Kai Krakow who sponsored me a Xbox One Wireless Controller
(including Wireless Adapter) and a pack of mouthwatering guarana cacao

%prep
{{{ git_dir_setup_macro }}}

%build
# nothing to do here

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -a * %{buildroot}
source %{buildroot}/lib/verbose.sh
source %{buildroot}/lib/installer.sh
DESTDIR=%{buildroot}/%{_prefix}/src/hid-xpadneo-%{Version}-%{Release}
echo "* copying module to '${DESTDIR}'"
cp --recursive "hid-xpadneo" "${DESTDIR}"
echo "* replacing version string if necessary"
(cd "${DESTDIR}" && sed -i 's/"@DO_NOT_CHANGE@"/"'"%{Version}-%{Release}"'"/g' dkms.conf src/version.h)
set -e
echo "* adding module to DKMS"
dkms add "${V[*]}" "hid-xpadneo/%{Version}-%{Release}" || cat_dkms_make_log
echo "* installing module (using DKMS)"
dkms install "${V[*]}" "hid-xpadneo/%{Version}-%{Release}" || cat_dkms_make_log

%files
%{_prefix}/src/hid-xpadneo-%{Version}-%{Release}/*

%changelog
* Tue Nov 17 2020 Akos Balla <akos.balla@sirc.hu> - 0.8-1
- create RPM specification
